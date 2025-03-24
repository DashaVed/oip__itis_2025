import re
from collections import defaultdict

from inverted_index_hw3 import build_inverted_index


def boolean_search(query: str, inverted_index: defaultdict[set]) -> set:
    """
    Реализация булевого поиска.

    :param query: запрос пользователя
    :param inverted_index: список терминов с id документов
    :return: документы, которые удовлетворяют запросу
    """
    stack = []  # хранит множества id документов для терминов
    operators = []  # хранит список неиспользованных операторов

    def apply_operator():
        op = operators.pop()
        if op == "NOT":
            term_set = stack.pop()
            all_docs = set([str(i) for i in range(2, 121)])
            stack.append(all_docs - term_set)
        else:
            right = stack.pop()
            left = stack.pop()
            if op == "AND":
                stack.append(left & right)
            elif op == "OR":
                stack.append(left | right)

    tokens = re.findall(r'\w+|AND|OR|NOT|[()]', query)  # регулярное выражение для поиска слов и операторов

    for token in tokens:
        if token == "(":
            operators.append(token)
        elif token == ")":
            while operators and operators[-1] != "(":  # применяем операторы до открывающихся скобок
                apply_operator()
            operators.pop()  # удаляем операторы с открывающейся скобкой
        elif token in {"AND", "OR", "NOT"}:
            while operators and operators[-1] != "(":
                apply_operator()  # применяет предыдущие операторы AND | OR | NOT
            operators.append(token)  # добавляет текущий оператор AND | OR | NOT
        else:
            stack.append(inverted_index.get(token, set()))

    while operators:
        apply_operator()

    return stack.pop() if stack else set()


if __name__ == "__main__":
    index = build_inverted_index()
    while True:
        query = input("Введите булевый запрос (для завершения напишите 'stop'): ")
        if query == "stop":
            break
        result = boolean_search(query, index)
        print("Найденные документы:", result)

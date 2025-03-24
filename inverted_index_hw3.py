import json
import os
from collections import defaultdict

from constants import TOKENS_DIR


def build_inverted_index():
    """
    Построение инвертированного индекса.

    - Проходимся по папке с токенами
    - Для каждого из токена находим документы, где он есть
    - Собираем словарь {"токен": {plant_id1, plant_id2, ...}}
    """
    inverted_index = defaultdict(set)

    for filename in os.listdir(TOKENS_DIR):
        doc_id = filename.split("_")[1]
        token_path = os.path.join(TOKENS_DIR, filename)

        with open(token_path, "r", encoding="utf-8") as file:
            for token in file:
                inverted_index[token.strip()].add(doc_id)

    return inverted_index


if __name__ == "__main__":
    index = build_inverted_index()
    index_new = {key: list(value) for key, value in index.items()}

    with open("inverted_index_tokens.json", "w", encoding="utf8") as file:
        json.dump(index_new, file, ensure_ascii=False)

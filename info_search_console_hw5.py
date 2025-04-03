import os
from collections import defaultdict
from typing import Any

import pymorphy3
from sklearn.metrics.pairwise import cosine_similarity

from constants import OUTPUT_TF_IDF_RESULT_DIR, EPSILON, URL_FOR_PARSE

morph = pymorphy3.MorphAnalyzer()


def load_index() -> dict[str, dict[str, tuple[float, float]]]:
    """
    Загружает индекс документов из файлов с tf-idf

    Читает файлы в указанной директории, игнорируя файлы с "tokens" в названии
    Для каждого документа создает словарь, где ключи - леммы, а значения - кортежи (idf, tf-idf)

    """
    index = {}  # {doc_id: {lemma: (idf, tf-idf)}}

    for filename in os.listdir(OUTPUT_TF_IDF_RESULT_DIR):
        if filename.split("_")[2] == "tokens":
            continue
        doc_id = filename.split("_")[1]
        index[doc_id] = {}

        with open(os.path.join(OUTPUT_TF_IDF_RESULT_DIR, filename), "r", encoding="utf-8") as f:
            for line in f:
                lemma, idf, tfidf = line.strip().split()
                index[doc_id][lemma] = (float(idf), float(tfidf))

    return index


def compute_query_vector(query: str, index: dict[str, dict[str, tuple[float, float]]]) -> dict[str, float]:
    """
    Преобразует поисковый запрос в вектор tf-idf

    - Лемматизирует запрос
    - Вычисляет частоту термов
    - Умножает на idf, полученный из индекса

    Возвращается вектор запроса в формате {lemma: tf-idf}
    """
    lemmatized_query = [morph.parse(word)[0].normal_form for word in query.split()]
    query_tf = defaultdict(int)

    for lemma in lemmatized_query:
        query_tf[lemma] += 1

    query_vector = {}
    for lemma, tf in query_tf.items():
        idf = next((index[doc][lemma][0] for doc in index if lemma in index[doc]), EPSILON)
        query_vector[lemma] = tf * idf

    return query_vector


def search(query: str, index: dict[str, dict[str, tuple[float, float]]]) -> list[tuple[Any, Any]]:
    """
    Выполняет векторный поиск документов, релевантных запросу

    - Вычисляет косинусное сходство между вектором запроса и документами в индексе
    - Возвращает список id документов, у которых сходство больше 0
    """
    query_vector = compute_query_vector(query, index)
    doc_vectors = []
    doc_ids = []

    for doc_id, doc_vector in index.items():
        doc_vector_tf_idf = {lemma: tfidf for lemma, (_, tfidf) in doc_vector.items()}
        doc_vectors.append([doc_vector_tf_idf.get(lemma, 0) for lemma in query_vector])
        doc_ids.append(doc_id)

    if not doc_vectors:
        return []

    query_vector_list = [[query_vector.get(lemma, 0) for lemma in query_vector]]
    similarities = cosine_similarity(query_vector_list, doc_vectors)[0]

    return [(doc_id, score) for doc_id, score in zip(doc_ids, similarities)]


if __name__ == "__main__":
    index = load_index()

    while True:
        query = input("Введите поисковой запрос (для выхода напишите stop): ")
        if query.lower() == "stop":
            break

        results = search(query, index)

        if len(results) == 0:
            print("Релевантных документов нет")
        else:
            for doc_id in sorted(results):
                print(f"{URL_FOR_PARSE}/{doc_id}")

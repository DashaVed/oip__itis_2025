import os
import math
from collections import Counter

from constants import TOKENS_DIR, LEMMAS_DIR, OUTPUT_DIR


def compute_idf(documents: dict[str, list]) -> dict[str, float]:
    """Подсчет IDF"""
    count_of_docs = len(documents)

    df_counts = Counter()
    for words in documents.values():
        df_counts.update(words)
    return {word: math.log(count_of_docs / df) for word, df in df_counts.items()}


def save_tfidf(
        file_id: str,
        word_list: list[str],
        idf_dict: dict[str, float],
        output_type: str) -> None:
    """Сохранение файла с рассчитанными IDF, TF-IDF"""
    word_counts = Counter(word_list)
    total_words = len(word_list)
    tf = {word: count / total_words for word, count in word_counts.items()}  # Подсчет tf
    tfidf = {word: tf[word] * idf_dict[word] for word in word_counts}  # Подсчет tf-idf

    with open(os.path.join(OUTPUT_DIR, f"plant_{file_id}_{output_type}_tfidf.txt"), "w") as f:
        for word, tfidf_score in sorted(tfidf.items()):
            f.write(f"{word} {idf_dict[word]:.4f} {tfidf_score:.4f}\n")


def main():
    # Словари для хранения всех документов
    all_tokens = {}
    all_lemmas = {}

    for filename in os.listdir(TOKENS_DIR):
        doc_id = filename.split("_")[1]
        if not os.path.exists(os.path.join(TOKENS_DIR, filename)):
            print(f"Ошибка: файл {filename} не найден!")
        else:
            with open(os.path.join(TOKENS_DIR, filename), "r") as f:  # Собираем токены для каждого файла
                tokens = f.read().split("\n")
                all_tokens[doc_id] = tokens

        with open(os.path.join(LEMMAS_DIR, f"plant_{doc_id}_lemmas.txt")) as f:  # Собираем леммы для каждого файла
            lemmas = [line.split()[0] for line in f]
            all_lemmas[doc_id] = lemmas

    # Подсчет IDF
    idf_tokens = compute_idf(all_tokens)
    idf_lemmas = compute_idf(all_lemmas)

    # Обработка документов
    for doc_id in all_tokens.keys():
        save_tfidf(doc_id, all_tokens[doc_id], idf_tokens, "tokens")
        save_tfidf(doc_id, all_lemmas[doc_id], idf_lemmas, "lemmas")


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)  # Создание выходной папки
    main()

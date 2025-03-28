import os
import math
from collections import Counter

from constants import TOKENS_DIR, LEMMAS_DIR, OUTPUT_TF_IDF_RESULT_DIR


def compute_token_idf(documents: dict[str, list[str]]) -> dict[str, float]:
    """
    Вычисление IDF для токенов

    :param documents: Словарь, где ключ — ID документа, значение — список токенов
    :return: Словарь с IDF значениями для каждого токена
    """
    count_of_docs = len(documents)
    df_counts = Counter()
    for words in documents.values():
        df_counts.update(set(words))
    return {word: math.log(count_of_docs / df) for word, df in df_counts.items()}


def compute_lemma_idf(documents: dict[str, list[list[str]]]) -> dict[str, float]:
    """
    Вычисление IDF для лемм

    :param documents: Словарь, где ключ — ID документа, значение — список списков, содержащих основную лемму и её формы
    :return: Словарь с IDF значениями для каждой леммы
    """
    count_of_docs = len(documents)
    df_counts = Counter()
    for words_list in documents.values():
        for words in words_list:
            df_counts.update(set(words[1:]))

    idf_dict = {}
    for words_list in documents.values():
        for words in words_list:
            df = sum(df_counts[word] for word in words[1:])
            idf_dict[words[0]] = math.log(count_of_docs / min(count_of_docs, df))
    return idf_dict


def main():
    """
    Основной процесс вычисления TF-IDF для токенов и лемм
    - Читаем входные файлы с токенами и леммами
    - Вычисляем IDF
    - Вычисляем TF-IDF
    - Сохраняем результаты в папку OUTPUT_TF_IDF_RESULT_DIR
    """
    all_tokens = {}
    all_lemmas = {}

    for filename in os.listdir(TOKENS_DIR):  # Достаем токены и леммы
        doc_id = filename.split("_")[1]

        with open(os.path.join(TOKENS_DIR, filename), "r", encoding="utf-8") as f:
            tokens = f.read().strip().split("\n")
            all_tokens[doc_id] = tokens

        with open(os.path.join(LEMMAS_DIR, f"plant_{doc_id}_lemmas.txt"), "r", encoding="utf-8") as f:
            lemmas: list[str] = f.read().strip().split("\n")
            all_lemmas[doc_id] = [lemma.split() for lemma in lemmas]

    idf_tokens = compute_token_idf(all_tokens)
    idf_lemmas = compute_lemma_idf(all_lemmas)

    for doc_id in all_tokens.keys():
        word_counts = Counter(all_tokens[doc_id])
        total_words = len(all_tokens[doc_id])
        tf_token = {word: count / total_words for word, count in word_counts.items()}  # Подсчет TF для токенов
        tfidf_tokens = {word: tf_token[word] * idf_tokens[word] for word in word_counts}  # Подсчет TF IDF для токенов

        tf_lemma = {}
        with open(os.path.join(TOKENS_DIR, f"plant_{doc_id}_tokens.txt"), "r", encoding="utf-8") as f:
            content_list = f.read().strip().split("\n")
            for lemma_list in all_lemmas[doc_id]:  # Подсчет TF для лемм
                lemma_key = lemma_list[0]
                if lemma_key not in tf_lemma:
                    tf_lemma[lemma_key] = 0
                for lemma in lemma_list[1:]:
                    tf_lemma[lemma_key] += content_list.count(lemma)
            for word, count in tf_lemma.items():
                tf_lemma[word] /= len(content_list)

        tfidf_lemmas = {word: tf_lemma[word] * idf_lemmas[word] for word in tf_lemma}  # Подсчет TF IDF для лемм

        # Сохраняем результаты TF-IDF в файлы
        with open(os.path.join(OUTPUT_TF_IDF_RESULT_DIR, f"plant_{doc_id}_tokens_tfidf.txt"), "w", encoding="utf-8") as f:
            for word, tfidf_score in sorted(tfidf_tokens.items()):
                f.write(f"{word} {idf_tokens[word]:.4f} {tfidf_score:.4f}\n")

        with open(os.path.join(OUTPUT_TF_IDF_RESULT_DIR, f"plant_{doc_id}_lemmas_tfidf.txt"), "w", encoding="utf-8") as f:
            for word, tfidf_score in sorted(tfidf_lemmas.items()):
                f.write(f"{word} {idf_lemmas[word]:.4f} {tfidf_score:.4f}\n")


if __name__ == "__main__":
    os.makedirs(OUTPUT_TF_IDF_RESULT_DIR, exist_ok=True)
    main()

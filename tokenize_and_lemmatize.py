import os
import re

import pymorphy3
from bs4 import BeautifulSoup
from stopwordsiso import stopwords

from constants import OUTPUT_FOLDER

# Загружаем полный список русских стоп-слов
STOP_WORDS = stopwords("ru")

# Инициализируем pymorphy3 для лемматизации
morph = pymorphy3.MorphAnalyzer()


def get_tokens_and_lemmas():
    """
    Токенизирует и лемматизирует текст для каждого из скачанных HTML-файлов.
    - Убирает стоп-слова, числа и мусор
    - Записывает уникальные токены в tokens/plant_{id}_tokens.txt
    - Группирует их по леммам в lemmas/plant_{id}_lemmas.txt
    """
    for file_name in os.listdir(OUTPUT_FOLDER):
        if file_name.endswith(".html"):
            tokens = set()
            lemmas = {}
            file_path = os.path.join(OUTPUT_FOLDER, file_name)
            with open(file_path, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")
                text = soup.get_text()
                words = re.findall(r"\b[а-яА-ЯёЁ]{2,}\b", text.lower())  # Регулярное выражения для поиска русских слов

                for word in words:
                    if word not in STOP_WORDS and not re.search(r"\d", word):  # Проверяем, что слова не из списка слов и не содержат цифры
                        tokens.add(word)
                        lemma = morph.parse(word)[0].normal_form  # Лемматизация

                        if lemma in lemmas:
                            lemmas[lemma].add(word)
                        else:
                            lemmas[lemma] = {word}

            # Записываем токены в файл
            with open(f"tokens/{file_name.split('.')[0]}_tokens.txt", "w", encoding="utf-8") as f:
                for token in sorted(tokens):
                    f.write(f"{token}\n")

            # Записываем леммы в файл
            with open(f"lemmas/{file_name.split('.')[0]}_lemmas.txt", "w", encoding="utf-8") as f:
                for lemma, words in sorted(lemmas.items()):
                    f.write(f"{lemma} {' '.join(sorted(words))}\n")


if __name__ == "__main__":
    get_tokens_and_lemmas()

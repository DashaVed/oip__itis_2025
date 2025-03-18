import os
import requests

from constants import OUTPUT_FOLDER, URL_FOR_PARSE


def download_pages():
    """
    Загружает HTML-страницы с указанного сайта и сохраняет их в локальную папку.

    - Проходит по `plant_id` от 1 до 120, формируя URL
    - Отправляет HTTP-запрос
    - Если статус-код 200, сохраняет HTML-страницу в файл
    - Записывает информацию о скачанных страницах в `index.txt`
    """
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    index_file = os.path.join(OUTPUT_FOLDER, "index.txt")
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }

    with open(index_file, "w", encoding="utf-8") as index:
        plant_id = 1
        while plant_id < 121:

            url = f"{URL_FOR_PARSE}/{plant_id}"
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                file_name = f"plant_{plant_id}.html"
                file_path = os.path.join(OUTPUT_FOLDER, file_name)

                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(response.text)

                index.write(f"{file_name}: {url}\n")
                print(f"Скачана страница - {url}")
            else:
                print(f"Не удалось скачать страницу - {url} (статус {response.status_code})")

            plant_id += 1


if __name__ == "__main__":
    download_pages()

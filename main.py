import time

import requests
from bs4 import BeautifulSoup

from config import BASE_URL, KEYWORDS, HEADERS


def scraping_habr(pages):
    """ Парсит сайт habr.com и выбирает свежие статьи, в которых встречается хотя бы одно из ключевых слов списка
    KEYWORDS """

    for n in range(1, pages):
        print(f"Страница {n}")
        response = requests.get(BASE_URL + f"/ru/all/page{n}/", headers=HEADERS)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        results = soup.find(class_="tm-articles-list").find_all(class_="tm-articles-list__item")

        count = 0

        for el in results:

            date_time = ""
            if el.find("span", class_="tm-article-snippet__datetime-published"):
                date_time = el.find("span", class_="tm-article-snippet__datetime-published").text

            link = ""
            if el.find("a", class_="tm-article-snippet__title-link"):
                link = "https://habr.com" + el.find("a", class_="tm-article-snippet__title-link").get('href')

            title = ""
            if el.find("a", class_="tm-article-snippet__title-link"):
                title = el.find("a", class_="tm-article-snippet__title-link").text

            article_text = ""
            if el.find(class_="tm-article-body tm-article-snippet__lead"):
                article_text = el.find(class_="tm-article-body tm-article-snippet__lead").text

            article_text_splited = [el.strip("«()/_-\\*+?!».,") for el in article_text.split()]
            title_splited = [el.strip("«()/_-\\*+?!».,") for el in title.split()]

            found_word = list(set(article_text_splited) & set(KEYWORDS) | set(title_splited) & set(KEYWORDS))

            if found_word:
                print("\nНайдено ключевое слово: ", "".join(found_word))
                to_print = f"Заголовок: {title}\nДата: {date_time}\nСсылка: {link}\n"
                print(to_print)
                count += 1

        if not count:
            print("Нет совпадений!\n")
        time.sleep(1)


def main():
    while True:
        pages = input("Введите количество страниц которое хотите пролистать (Макс. 50): ")
        if pages.isdigit() and int(pages) in range(1, 51):
            pages_to_scrab = int(pages) + 1
            break
    print()
    scraping_habr(pages_to_scrab)


if __name__ == "__main__":
    main()

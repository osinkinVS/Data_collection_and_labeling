import requests
from lxml import html
from pprint import pprint
import csv


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36"
}

url = "https://www.chitai-gorod.ru"
response = requests.get(
    url + "/catalog/books/farmakologiya-toksikologiya-110216", headers=headers
)
dom = html.fromstring(response.text)

books_list = []
# Ищем все элементы, представляющие собой карточки книг
items = dom.xpath("//div[@class='products-list']")
for item in items:
    books_info = {}
    # Извлекаем название книги
    name = item.xpath(".//div[@class='product-title__head']/text()")
    books_info["Название"] = name[0].strip() if name else "Название не указано"
    # Извлекаем имя автора
    author = item.xpath(".//div[@class='product-title__author']/text()")
    books_info["Автор"] = author[0].strip() if author else "Автор не указан"
    # Извлекаем цену
    price = item.xpath(
        ".//div[@class='product-price__value product-price__value--discount']/text()"
    )
    if not price:
        price = item.xpath(".//div[@class='product-price__value']/text()")
    books_info["Цена"] = price[0].strip() if price else "Цена не указана"

    books_list.append(books_info)


pprint(books_list)

# Сохраняем данные в CSV-файл
with open("books.csv", mode="w", newline="", encoding="utf-8") as file:
    fieldnames = ["Название", "Автор", "Цена"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for book in books_list:
        writer.writerow(book)

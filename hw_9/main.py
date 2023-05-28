import re
from random import randint
from time import sleep, time
from threading import current_thread
import os
import concurrent.futures
import json
import requests
from bs4 import BeautifulSoup
from login import get_session

max_page_url = "https://quotes.toscrape.com/page/10/"
min_page_url = "https://quotes.toscrape.com/page/1/"
base_url = 'http://quotes.toscrape.com'
page_link_template = f"/page/{1}/"
base_book_url = "https://www.goodreads.com"

session = get_session()  # GLOBAL session


def get_book_dicts(pag_link):
    print(f"Getting books info {pag_link}")
    books_dicts = []
    response = session.get(pag_link)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="tableList")
    if table:
        tr_list = table.find_all("tr")
        for tr in tr_list:
            book_dict = {}
            book_title = tr.find("a", class_="bookTitle").get_text()
            book_dict["book_title"] = book_title
            img = tr.find("img", class_="bookCover").get("src")
            book_dict["img"] = img
            authors = tr.find_all("div", class_="authorName__container")
            co_authors = []
            for author_ in authors:
                author = author_.find("span").get_text()
                co_authors.append(author)
            book_dict["co_authors"] = co_authors
            rating = tr.find("span", class_="minirating").get_text()
            book_dict["rating"] = rating
            books_dicts.append(book_dict)
    return books_dicts


def get_books_result(link):
    print(f"Entry to AUTHOR {link}")

    data_dicts = []
    pagination_list = []
    response = session.get(link)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", class_="stacked tableList")

    if table:
        table_action_link = table.find_next_sibling("a", class_="actionLink")
        book_pagination = base_book_url + table_action_link.get("href")
        page = 1
        while True:
            current_page = f"{book_pagination}?page={page}&per_page=100"
            pagination_list.append(current_page)
            print(current_page)
            page += 1
            response = session.get(current_page)
            print(response.status_code)
            if response.status_code != 200 or page > 15:
                print("break", page)
                break

    for pag_link in pagination_list:
        book_dicts = get_book_dicts(pag_link)
        data_dicts.extend(book_dicts)

    return data_dicts


def scrap_books():
    start = time()
    response = session.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    pages = soup.find("ul", attrs={"class": "pager"})
    pages_list_urls = []
    books_list = []
    books_urls = set()

    try:
        for page in range(1, 11):
            link = f"{base_url}/page/{page}/"
            pages_list_urls.append(link)
            print(f"PAGINATOR {link}")
    except ValueError:
        print("The amount of pages was changed by service owner!")

    for page in pages_list_urls:
        response = session.get(page)

        soup = BeautifulSoup(response.text, 'html.parser')
        all_authors = soup.find_all('small', attrs={'class': 'author'})
        for author in all_authors:
            link = author.find_next("a").find_next_sibling("a")
            books_urls.add(link.get("href"))
    print(len(books_urls), books_urls)

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        books = executor.map(get_books_result, list(books_urls))

        books_list.extend(books)
        print(f"Thread number {os.getpid()}")
    print(f"Books time = {time() - start}")
    return books_list


if __name__ == '__main__':
    # get_books_result("https://www.goodreads.com/author/show/656983.J_R_R_Tolkien")
    # get_book_dicts("https://www.goodreads.com/author/list/656983.J_R_R_Tolkien?page=7&per_page=100")

    books = scrap_books()
    print(len(books))
    one_list_books = []
    for book in books:
        one_list_books.extend(book)
    print(len(one_list_books))
    with open("books.json", "w") as file:
        json.dump(one_list_books, file, indent=4, ensure_ascii=False)

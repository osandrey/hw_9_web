from random import randint
from time import sleep, time
from threading import current_thread
import os
import concurrent.futures
import json
import requests
from bs4 import BeautifulSoup

max_page_url = "https://quotes.toscrape.com/page/10/"
min_page_url = "https://quotes.toscrape.com/page/1/"
base_url = 'http://quotes.toscrape.com'
page_link_template = f"/page/{1}/"

# def parse_every_page():
#     """ max_page_url = "https://quotes.toscrape.com/page/10/"
#         min_page_url = "https://quotes.toscrape.com/page/1/"""
#
#     # url = 'http://quotes.toscrape.com'
#     #page_link_template = f"/page/{1}/"
#
#     response = requests.get(base_url)
#     soup = BeautifulSoup(response.text, 'html.parser')
#
#     pages = soup.find("ul", attrs={"class":"pager"})
#     page_link = pages.find("a").get("href")
#     pages_list_urls = []
#
#     # response_pages = requests.get()
#     # soup = BeautifulSoup(response_pages.text, 'html.parser')
#     try:
#         for page in range(1, 11):
#             pages_list_urls.append(f"{base_url}/page/{page}/")
#     except ValueError:
#         print("The amount of pages was changed by service owner!")
#
#     return pages_list_urls

def get_author_result(author):
    print(f"Thread number {os.getpid()} {current_thread().name}{current_thread().native_id}")
    authors_list = []
    author_dict = {"fullname": None, "born_date": None, "born_location": None, "description": None}
    author.get("href")
    author_url = author.find_next_sibling("a").get("href")
    # print(f'{author_name}-{author_url}')
    response_author = requests.get(base_url + author_url)
    soup = BeautifulSoup(response_author.text, 'html.parser')

    author_title = soup.find('h3', class_='author-title')
    burn_date = author_title.find('span', attrs={'class': 'author-born-date'}).text
    location = author_title.find("span", attrs={"class": "author-born-location"}).text
    description = author_title.find('div', class_='author-description').text.strip()
    author_name = author_title.text.strip().split("\n")[0].replace("-", " ")

    author_dict["fullname"] = author_name
    author_dict["born_date"] = burn_date
    author_dict["born_location"] = location
    author_dict["description"] = description
    # print(f'{author_name}\nBorn: {burn_date} in: {location}\nDescription:\n{description}\n\n\n')
    # if author_dict not in authors_list:
    #     authors_list.append(author_dict)
    print("added author")
    return author_dict


def scrap_authors():
    start = time()
    response = requests.get(base_url)
    # sleep(randint(1, 5))
    soup = BeautifulSoup(response.text, 'html.parser')

    pages = soup.find("ul", attrs={"class": "pager"})
    page_link = pages.find("a").get("href")
    pages_list_urls = []
    authors_list = []
    # response_pages = requests.get()
    # soup = BeautifulSoup(response_pages.text, 'html.parser')
    try:
        for page in range(1, 11):
            pages_list_urls.append(f"{base_url}/page/{page}/")
    except ValueError:
        print("The amount of pages was changed by service owner!")

    for page in pages_list_urls:
        response = requests.get(page)

        # with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        #     future = executor.submit(requests.get, page)
        #     response = future.result()
        #     print(f"Thread number {str(future)}")
        soup = BeautifulSoup(response.text, 'html.parser')
        # authors_list = []

        all_authors = soup.find_all('small', attrs={'class': 'author'})
        # for author in soup.find_all('small', attrs={'class': 'author'}):
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            authors = executor.map(get_author_result, all_authors)
            authors_list.extend(authors)
            print(f"Thread number {os.getpid()}")
    print(f"Authors time = {time() - start}")
    return authors_list



def get_quotes_result(page):
    print(f"Thread number {os.getpid()} {current_thread().name}{current_thread().native_id}")
    quotes_page = []
    response = requests.get(page)
    soup = BeautifulSoup(response.text, 'html.parser')

    # response = requests.get(page_url)
    # soup = BeautifulSoup(response.text, 'html.parser')

    quotes = soup.find_all("span", class_="text")

    # sleep(randint(1, 5))
    authors = soup.find_all('small', class_='author')
    # sleep(randint(1, 5))
    tags = soup.find_all('div', class_='tags')
    # quotes_list = []
    for i in range(0, len(quotes)):
        quotes_dict = {"tags": None, "author": None, "quote": None}
        # print(f"Now looking for quote {i + 1}\n")
        quote = quotes[i].text
        author = authors[i].text
        tags_for_quote = tags[i].find_all('a', class_='tag')
        tags_list = []

        for tag in tags_for_quote:
            # sleep(randint(1, 5))
            text_tag = tag.get_text()

            tags_list.append(text_tag)
            # print(f'{text_tag} -- {url}{tag.get("href")}')
        # print(f"Quote: {quote}, Author: {author}, Tags-list: {tags_list}")
        quotes_dict["author"] = author
        quotes_dict["quote"] = quote
        quotes_dict["tags"] = tags_list
        print("added quote")
        quotes_page.append(quotes_dict)

    return quotes_page

def scrap_quotes():
    start = time()
    print(f"Thread number {os.getpid()}{current_thread().name}")
    response = requests.get(base_url)
    # sleep(randint(1, 5))
    soup = BeautifulSoup(response.text, 'html.parser')

    pages = soup.find("ul", attrs={"class": "pager"})
    page_link = pages.find("a").get("href")
    pages_list_urls = []
    quotes_list = []

    # response_pages = requests.get()
    # soup = BeautifulSoup(response_pages.text, 'html.parser')


    try:
        for page in range(1, 11):
            pages_list_urls.append(f"{base_url}/page/{page}/")
    except ValueError:
        print("The amount of pages was changed by service owner!")

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        quotes = list(executor.map(get_quotes_result, pages_list_urls))
        print(quotes, type(quotes))
        # quotes_list.extend(quotes)
        [quotes_list.extend(quote) for quote in quotes]
        print(f"Thread number {os.getpid()}")


    print(f"Quotes time = {time() - start}")
    return quotes_list

if __name__ == '__main__':
    authors = scrap_authors()
    quotes = scrap_quotes()
    # scrap_quotes()

    # with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    #     authors = executor.submit(scrap_authors)
    #     print(f"Thread number {os.getpid()}")

    with open("authors.json", "w") as file:
        json.dump(authors, file, indent=4)

    # with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    #     quotes = executor.submit(scrap_quotes)
    #     print(f"Thread number {os.getpid()}")

    with open("quotes.json", "w") as fh:
        json.dump(quotes, fh, indent=4)


# print(len(scrap_authors()))
# print(len(scrap_quotes()))
# print(parse_every_page())
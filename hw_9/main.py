from random import randint
from time import sleep

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


def scrap_authors():
    response = requests.get(base_url)
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
        soup = BeautifulSoup(response.text, 'html.parser')
        # authors_list = []

        for author in soup.find_all('small', attrs={'class': 'author'}):
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
            author_name = author_title.get_text(strip=True).split(':')[0]

            author_dict["fullname"] = author_name
            author_dict["born_date"] = burn_date
            author_dict["born_location"] = location
            author_dict["description"] = description
            # print(f'{author_name}\nBorn: {burn_date} in: {location}\nDescription:\n{description}\n\n\n')
            if author_dict not in authors_list:
                authors_list.append(author_dict)
                print("added author")
    return authors_list

def scrap_quotes():
    response = requests.get(base_url)
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

    for page in pages_list_urls:
        response = requests.get(page)
        soup = BeautifulSoup(response.text, 'html.parser')

        # response = requests.get(page_url)
        # soup = BeautifulSoup(response.text, 'html.parser')

        quotes = soup.find_all("span", class_="text")

        # sleep(randint(1, 5))
        authors = soup.find_all('small', class_='author')
        # sleep(randint(1, 5))
        tags = soup.find_all('div', class_='tags')
        # sleep(randint(1, 5))
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
            quotes_list.append(quotes_dict)
    return quotes_list

if __name__ == '__main__':
    with open("authors.json", "w") as file:
        json.dump(scrap_authors(), file, indent=4)

    with open("quotes.json", "w") as fh:
        json.dump(scrap_quotes(), fh, indent=4)
print(len(scrap_authors()))
print(len(scrap_quotes()))
# print(parse_every_page())
import re
import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup


url = "https://quotes.toscrape.com"
def scrapper():
    response = requests.get(url)
    print(response.text)
    soup = BeautifulSoup(response.text, "lxml")
    print(soup.prettify())
    print(soup.title.string)

    """Добратись до данних"""
    quotes_spans = soup.find_all("span", attrs={"class": "text"})
    for q_s in quotes_spans:
        text = q_s.string
        print(text)

    # content = soup.select("div[class=row] div[class=col-md-4 tags-box]  a")

def get_author_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    quotes_divs = soup.find_all("div", {"class": "quote"})
    for q_d in quotes_divs:
        author_name = q_d.find("small", attrs={"class": "author"}).string
        author_url = q_d.find("a")["href"]
        print(f"Authors: {author_name} - {author_url}")
    # quotes_spans = soup.find_all("small", attrs={"class": "author"})
    # authors_urls = soup.find_all("a")


if __name__ == '__main__':
    scrapper()
    get_author_url(url)
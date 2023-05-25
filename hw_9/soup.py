import requests
from bs4 import BeautifulSoup

"""
Authors
fullname, born_location, born_date, description

Quotes
quote, tags, authors
"""

url = 'http://quotes.toscrape.com'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

quotes = soup.find_all("span", class_="text")
authors = soup.find_all('small', class_='author')
tags = soup.find_all('div', class_='tags')


for i in range(0, len(quotes)):
    print(f"\nNow looking for quote {i+1}\n")
    quote = quotes[i].text
    author = authors[i].text
    tags_for_quote = tags[i].find_all('a', class_='tag')
    tags_list = []

    for tag in tags_for_quote:
        text_tag = tag.get_text()
        tags_list.append(text_tag)
        # print(f'{text_tag} -- {url}{tag.get("href")}')

    print(f"Quote: {quote}, Author: {author}, Tags-list: {tags_list}")
    # break\

#
# fullname, born_location, born_date, description
for i in range(0, len(quotes)):
    # author_urls = soup.select("[href^='/author/']")

    # soup = BeautifulSoup(response.text, 'html.parser')
    # print(author_url)
    author_name = authors[i].text
    for author in soup.find_all('small', attrs={'class': 'author'}):
        author.get("href")
        author_url = author.find_next_sibling("a").get("href")
        # print(f'{author_name}-{author_url}')
        response_author = requests.get(url + author_url)
        soup = BeautifulSoup(response_author.text, 'html.parser')

        author_title = soup.find('h3', class_='author-title')
        burn_date = author_title.find('span', attrs={'class': 'author-born-date'}).text
        location = author_title.find("span", attrs={"class": "author-born-location"}).text
        description = author_title.find('div', class_='author-description').text.strip()
        author_name = author_title.get_text(strip=True).split(':')[0]

        print(f'{author_name}\nBorn: {burn_date} in: {location}\nDescription:\n{description}\n\n\n')
#
#
# for page in range(0, len(quotes)):
#     pass
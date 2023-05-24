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

# for i in range(0, len(quotes)):
#     print(f"Now looking for quote {i+1}\n")
#     print(quotes[i].text)
#     print('--' + authors[i].text)
#     tags_for_quote = tags[i].find_all('a', class_='tag')
#     for tag_for_quote in tags_for_quote:
#         print(f'{tag_for_quote.text} -- {url}{tag_for_quote.get("href")}')
#     # break


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
        """
                fullname = 1
                born_date = 2
                born_location = 3
                description = 4"""

        author_title = soup.find('h3', class_='author-title')
        burn_date = author_title.find('span', attrs={'class': 'author-born-date'}).text
        location = author_title.find("span", attrs={"class": "author-born-location"}).text
        description = author_title.find('div', class_='author-description').text.strip()
        author_name = author_title.get_text(strip=True).split(':')[0]

        print(f'{author_name}\nBorn: {burn_date} in: {location}\nDescription:\n{description}\n\n\n')

import requests
from bs4 import BeautifulSoup

url = 'http://quotes.toscrape.com'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

quotes = soup.find_all("span", class_="text")
authors = soup.find_all('small', class_='author')
tags = soup.find_all('div', class_='tags')


def get_quotes(url):

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
    # break


def get_author(page_link):
    # fullname, born_location, born_date, description
    url = page_link
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    quotes = soup.find_all("span", class_="text")
    authors = soup.find_all('small', class_='author')

    for i in range(0, len(quotes)):
        # author_urls = soup.select("[href^='/author/']")
        # print(author_url)
        author_name = authors[i].text
        for author in soup.find_all('small', attrs={'class': 'author'}):
            author.get("href")
            author_url = author.find_next_sibling("a").get("href")
            # print(f'{author_name}-{author_url}')
            # response_author = requests.get(url + author_url)
            # soupe = BeautifulSoup(response_author.text, 'html.parser')

            author_title = author.find('h3', class_='author-title')
            burn_date = author.find('span', attrs={'class': 'author-born-date'}).text
            location = author_title.find("span", attrs={"class": "author-born-location"}).text
            description = author_title.find('div', class_='author-description').text.strip()
            author_name = author_title.get_text(strip=True).split(':')[0]

            print(f'{author_name}\nBorn: {burn_date} in: {location}\nDescription:\n{description[0:20]}\n\n\n')


def parse_every_page():
    #max_page_url = "https://quotes.toscrape.com/page/10/"
    #min_page_url = "https://quotes.toscrape.com/page/1/"
    url = 'http://quotes.toscrape.com'
    #page_link_template = f"/page/{1}/"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    pages = soup.find("ul", attrs={"class":"pager"})
    page_link = pages.find("a").get("href")
    pages_list_urls = []

    # response_pages = requests.get()
    # soup = BeautifulSoup(response_pages.text, 'html.parser')
    try:
        for page in range(1, 11):
            pages_list_urls.append(f"{url}/page/{page}/")
    except ValueError:
        print("The amount of pages was changed by service owner!")

    for page_url in pages_list_urls:
        print(page_url)
        # get_quotes(page_url)
        # get_author(page_link=page_url)



if __name__ == '__main__':
    parse_every_page()

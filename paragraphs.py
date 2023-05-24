import requests
from bs4 import BeautifulSoup


url = "http://quotes.toscrape.com/"
page = requests.get(url)

soup = BeautifulSoup(page.text, "html.parser")

all_paragraphs = soup.find_all("p")

for paragraph in all_paragraphs:
    # print(f'Paragraph text = {paragraph.get_text().strip()}')
    # print(f'Paragraph get_text = {paragraph.text.strip()}')
    body_children = list(paragraph.children)
    # print(body_children)

# знайти перший тег <a> всередині першого тега <div> на сторінці
first_div = soup.find("div")
first_div_link = first_div.find("a")
# print(first_div_link.text)

# Щоб отримати батьківський елемент першого тега <p> на сторінці ми можемо використовувати властивість parent
first_paragraph = soup.find("p")
first_paragraph_parent = first_paragraph.parent
# print(first_paragraph_parent.prettify())

# можна використовувати методи find_parent і find_parents для пошуку батьківських елементів:

container = soup.find("div", attrs={"class": "quote"}).find_parent("div", class_="col-md-8")
# print(container)

# Ви можете отримати доступ до сусідніх елементів за допомогою атрибутів next_sibling та previous_sibling.
#
# Наприклад, щоб отримати наступний сусідній елемент першого тега <span>, з класом "tag-item" на сторінці:
next_sibling = soup.find("span", attrs={"class": "tag-item"}).find_next_sibling("span")
# print(next_sibling)


# Пошук за CSS-селекторами
# Знайдемо всі теги <p> на сторінці
p = soup.select("p")
# print(p)

# Знайдемо всі елементи з класом "text"
text = soup.select(".text")

# Комбіновані селектори
a = soup.select("div.container a")

# Атрибути
# Можна шукати елементи за значенням атрибутів. Знайдемо всі елементи, у яких атрибут href починається з "https://"
href = soup.select("[href^='https://']")
# print(href)

# Знайдемо всі елементи, у яких атрибут class містить слово "text":
ctext = soup.select("[class*='text']")
print(ctext)
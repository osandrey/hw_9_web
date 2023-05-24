import re
import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup

base_url = "https://index.minfin.com.ua/russian-invading/casualties"


def get_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    content = soup.select("div[class=ajaxmonth] h4[class=normal] a")
    # print(content)
    # print(content[0]["href"].split('/'))
    url_list = ["/"]
    prefix = "/month.php?month="
    for tag_a in content:
        url_list.append(prefix + re.search(r"\d{4}-\d{2}", tag_a["href"]).group())

    return url_list


def spider(urls):
    data = []
    for url in urls:
        response = requests.get(base_url + url)
        soup = BeautifulSoup(response.text, "lxml")
        content = soup.select("ul[class=see-also] li[class=gold]")

        for elem in content:
            elem_data = {}
            date = elem.find("span", attrs={"class": "black"}).text
            try:
                date = datetime.strptime(date, "%d.%m.%Y").isoformat()
            except ValueError:
                print(f"Error appeared for {date}")
                continue
            elem_data.update({"date": date})
            enamy_losses = elem.find("div").find("div").find("ul")

            for loss in enamy_losses:
                title, quantity, *other = loss.text.split("—")
                title = title.strip()
                # print(title, quantity)
                quantity = re.search(r"\d+", quantity).group()
                elem_data.update({title: quantity})
            data.append(elem_data)
    return data


def load_json_author_to_database(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        for item in data:
            print(item)



if __name__ == '__main__':
    # urls_for_parse = get_url(base_url)
    # result = spider(urls_for_parse)
    # for r in result:
    #     with open("Moskali.json", "w", encoding="utf-8") as file:
    #         json.dump(result, file, ensure_ascii=False, indent=4)

    load_json_author_to_database("Moskali.json")
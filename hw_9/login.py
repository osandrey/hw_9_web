import requests
from requests import Session


cookies = {
    'session': 'eyJjc3JmX3Rva2VuIjoic2V3TnFqTEl4VFd2YUhTWE1KR1ZCbWxaY3lremdFckNuYktGcGhpWURkT1VSZlB0b3VBUSJ9.ZHNYVw.1ox1HXWTDAj4CFtMU8Rx7PuxSfI',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ar;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    # 'Cookie': 'session=eyJjc3JmX3Rva2VuIjoic2V3TnFqTEl4VFd2YUhTWE1KR1ZCbWxaY3lremdFckNuYktGcGhpWURkT1VSZlB0b3VBUSJ9.ZHNYVw.1ox1HXWTDAj4CFtMU8Rx7PuxSfI',
    'Origin': 'http://quotes.toscrape.com',
    'Referer': 'http://quotes.toscrape.com/login',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
}

data = {
    'csrf_token': 'sewNqjLIxTWvaHSXMJGVBmlZcykzgErCnbKFphiYDdOURfPtouAQ',
    'username': 'admin',
    'password': 'admin',
}


def get_session():
    session = Session()
    response = session.post('http://quotes.toscrape.com/login', cookies=cookies, headers=headers, data=data,
                            verify=False)
    return session



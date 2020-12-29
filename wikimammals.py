import requests
from bs4 import BeautifulSoup
import csv

URL = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
HOST = 'https://ru.wikipedia.org'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/85.0.4183.102 YaBrowser/20.9.3.189 (beta) Yowser/2.5 Safari/537.36',
    'accept': '*/*'
}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('a', class_='mw-category')
    print(items)

    mammals = []
    for item in items:
        mammals.append({
            'title': item.find('div', class_="mw-category").get_text(strip=True),
            'link': HOST + item.find('div', class_="mw-category").get('href')
        })
    print(mammals)


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print('Error')
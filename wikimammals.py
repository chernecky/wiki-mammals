import requests
from bs4 import BeautifulSoup
import csv
import os

URL = "https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту"
HOST = 'https://ru.wikipedia.org'
FILE = 'cars.csv'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/85.0.4183.102 YaBrowser/20.9.3.189 (beta) Yowser/2.5 Safari/537.36',
    'accept': '*/*'
}


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages(html):
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find_all('div', class_='mw-category')
    print(pages)


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='mw-category')
    print(items)

    mammals = []
    for item in items:
        mammals.append({
            'title': item.find('div', class_="mw-category").get_text(strip=True),
            'link': HOST + item.find('div', class_="mw-category").get('href')
        })
    return mammals


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';' )
        writer.writerow(['title', 'link'])
        for item in items:
            writer.writerow([item['title'], item['link']])



def parse():
    URL = input('Введите url: ')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        mammals = []
        pages_count = get_pages(html.text)
        for page in range(1, pages_count + 1):
            print(f'Парсинг страницы {page} из {pages_count}...')
            html = get_html(URL, params={'page': page})
            mammals.extend(get_content(html.text))
            save_file(mammals, FILE)
        print(f'Получено {len(mammals)} автомобилей')
        os.startfile(FILE)
    else:
        print('Error')


import json

import requests
from bs4 import BeautifulSoup

URL = 'https://quotes.toscrape.com/'


def scrape_page(page_url):
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('span', class_='text')
    authors = soup.find_all('small', class_='author')
    tags = soup.find_all('div', class_='tags')
    result = []
    for i in range(0, len(quotes)):
        res = {}
        res.update({'author': authors[i].text})
        res.update({'quote': quotes[i].text})
        tags_for_quote = tags[i].find_all('a', class_='tag')
        tags_list = []
        for tag in tags_for_quote:
            tags_list.append(tag.text)
        res.update({'tags': tags_list})
        result.append(res)
    return result


def next_page_url(current_url, root_url=URL):
    response = requests.get(current_url)
    soup = BeautifulSoup(response.text, 'lxml')
    find_nav = soup.find_all('li', class_='next')
    for i in find_nav:
        if i.find('a')['href']:
            return f"{root_url}{i.find('a')['href'][1:]}"


if __name__ == '__main__':
    scrape_url = URL
    res_quotes = []
    while True:
        print(scrape_url)
        res_quotes.extend(scrape_page(scrape_url))
        scrape_url = next_page_url(scrape_url)
        if not scrape_url:
            break
    print(len(res_quotes))
    with open('quotes.json', 'w', encoding='utf-8') as fh:
        json.dump(res_quotes, fh)
        print('Write to "quotes.json" completed')
    # with open('quotes.json', 'r') as fh:
    #     result = json.load(fh)
    #     print(result[99])








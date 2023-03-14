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
    result_quotes = scrape_quotes(quotes, authors, tags)
    result_author = scrape_author_from_quotes(soup)
    return result_quotes, result_author


def scrape_quotes(quotes, authors, tags):
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


def scrape_author_from_quotes(soup):
    href_s = soup.find_all('a', href=True)
    res_urls = []
    for i in href_s:
        if 'authors' in i['href']:
            continue
        if 'author' in i['href']:
            author_url = f'{URL}{i["href"][1:]}'
            if author_url not in res_urls:
                res_urls.append(author_url)
    return res_urls


def scrape_authors_url(author_url):
    response = requests.get(author_url)
    soup = BeautifulSoup(response.text, 'lxml')
    name_ = soup.find('h3', class_='author-title').text
    born_date_ = soup.find('span', class_='author-born-date').text
    born_location_ = soup.find('span', class_='author-born-location').text
    description_ = soup.find('div', class_='author-description').text
    return name_.strip(), born_date_.strip(), born_location_.strip(), description_.strip()


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
    res_authors_urls = []
    res_authors = []

    while True:
        print(scrape_url)
        quotes_res, authors_res = scrape_page(scrape_url)
        res_quotes.extend(quotes_res)
        for url in authors_res:
            if url not in res_authors_urls:
                res_authors_urls.append(url)
        scrape_url = next_page_url(scrape_url)
        if not scrape_url:
            break
    for url in res_authors_urls:
        print(url)
        name, born_date, born_location, descriptions = scrape_authors_url(url)
        res_authors.append({"fullname": name,
                            "born_date": born_date,
                            "born_location": born_location,
                            "description": descriptions})

    with open('quotes.json', 'w', encoding='utf-8') as fh:
        json.dump(res_quotes, fh)
        print(f'Write {len(res_quotes)} quotes to "quotes.json" successful')
    with open('authors.json', 'w', encoding='utf-8') as fh:
        json.dump(res_authors, fh)
        print(f'Write {len(res_authors)} authors to "authors.json" successful')

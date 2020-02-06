import csv
import re
import requests
from bs4 import BeautifulSoup
from langdetect import detect
from pprint import pprint


def get_max_pages(soup):
    pagination_info_string = soup.find(
        'p', {'class': 'pagination-info'}).string.replace(" ", "")
    max_pages = int(re.search('of(.*)\\|', pagination_info_string).group(1))

    return max_pages


def get_soup(url):
    html_page_source_code_string = requests.get(url).text
    soup = BeautifulSoup(html_page_source_code_string, 'html.parser')

    return soup


def save_articles_csv(article_list):
    with open("output.csv", "w") as csvfile:
        writer = csv.writer(csvfile)
        for article in article_list:
            writer.writerow(article)


def scrape_specific_journal(url, separator, article_list):
    current_page_num = 1

    soup = get_soup(url)
    max_pages = get_max_pages(soup)
    article_title = soup.find(
        'div', {'class': 'j-meta-title'}).string.strip().encode('ascii', 'ignore')

    while current_page_num <= max_pages:
        soup = get_soup(url)

        for xmp in soup.findAll('xmp', {'class': 'abstract-article'}):
            article_abstract = xmp.string

            if article_abstract is None:
                continue

            article_abstract = article_abstract.encode('ascii', 'ignore')
            is_period_exist = "." in article_abstract

            if is_period_exist is False:
                continue

            article_abstract_first_sentence = article_abstract[:article_abstract.index(
                ".")]

            if article_abstract_first_sentence is None:
                continue

            article_abstract_language = detect(article_abstract_first_sentence)

            if article_abstract_language != 'id':
                continue

            article = [article_title, article_abstract]
            article_list.append(article)

        current_page_num += 1

        if current_page_num == 2:
            url += separator + str(current_page_num)
        else:
            url = url.split(separator, 1)[0]
            url += separator + str(current_page_num)


def scrape_main_page(base_url, separator, article_list):
    current_page_num = 1
    url = base_url + '/journal'

    soup = get_soup(url)
    max_pages = get_max_pages(soup)

    while current_page_num <= max_pages:
        soup = get_soup(url)

        for a in soup.findAll('a', {'class': 'title-journal'}):
            journal_endpoint = a.get('href')
            journal_url = base_url + journal_endpoint
            scrape_specific_journal(
                journal_url, separator, article_list)

        current_page_num += 1


def main():
    base_url = 'http://garuda.ristekdikti.go.id'
    separator = '?page='
    article_list = []

    scrape_main_page(base_url, separator, article_list)

    # print article_list in a pretty manner
    # pprint(article_list)

    save_articles_csv(article_list)


if __name__ == "__main__":
    main()

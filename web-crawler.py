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
    journal_title = soup.find(
        'div', {'class': 'j-meta-title'}).string.strip().encode('ascii', 'ignore')

    while current_page_num <= max_pages:
        soup = get_soup(url)

        for div in soup.findAll('div', {'class': 'article-item'}):
            article_title_div = div.find('a', {'class': 'title-article'})
            article_title = article_title_div.find('xmp').string
            article_abstract = div.find(
                'xmp', {'class': 'abstract-article'}).string

            if article_abstract is None or article_title is None:
                continue

            article_title = article_title.encode('ascii', 'ignore')
            article_abstract = article_abstract.encode('ascii', 'ignore')

            try:
                article_abstract_language = detect(
                    article_abstract)
            except:
                article_abstract_language = 'error'

            if article_abstract_language != 'id':
                continue

            is_period_exist = "." in article_abstract

            if is_period_exist is False:
                continue

            article = [journal_title, article_title, article_abstract]
            article_list.append(article)

        current_page_num += 1

        if current_page_num == 2:
            url += separator + str(current_page_num)
        else:
            url = url.split(separator, 1)[0]
            url += separator + str(current_page_num)


def scrape_main_page(base_url, separator, article_list):
    current_page_num = 1
    main_page_url = base_url + '/journal'

    soup = get_soup(main_page_url)
    max_pages = get_max_pages(soup)

    while current_page_num <= max_pages:
        soup = get_soup(main_page_url)

        for a in soup.findAll('a', {'class': 'title-journal'}):
            journal_endpoint = a.get('href')
            journal_page_url = base_url + journal_endpoint
            scrape_specific_journal(
                journal_page_url, separator, article_list)

        current_page_num += 1

        if current_page_num == 2:
            main_page_url += separator + str(current_page_num)
        else:
            main_page_url = main_page_url.split(separator, 1)[0]
            main_page_url += separator + str(current_page_num)


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

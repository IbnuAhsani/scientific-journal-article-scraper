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
    is_articles_saved = True

    try:
        with open("output.csv", "w") as csvfile:
            writer = csv.writer(csvfile)

            for article in article_list:
                writer.writerow(article)
    except:
        is_articles_saved = False

    return is_articles_saved


def set_new_url_endpoint(current_page_num, url, separator):
    if current_page_num == 2:
        url += separator + str(current_page_num)
    else:
        url = url.split(separator, 1)[0]
        url += separator + str(current_page_num)

    return url


def scrape_specific_journal(url, separator, article_list, journal_id):
    is_journal_scraped = False
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

            article_abstract = article_abstract.replace("\n", " ")
            article = [journal_id, journal_title,
                       article_title, article_abstract]

            article_list.append(article)
            is_journal_scraped = True

        current_page_num += 1

        url = set_new_url_endpoint(
            current_page_num, url, separator)

    print('| Scraped journal ' + journal_title)

    return is_journal_scraped


def scrape_main_page(base_url, separator, article_list):
    is_main_page_scraped = False
    journal_id = 1
    current_page_num = 1
    main_page_url = base_url + '/journal'

    soup = get_soup(main_page_url)
    max_pages = get_max_pages(soup)

    while current_page_num <= max_pages:
        print('+--------------------------------------------------------------+')  # \t\t
        print('| Scraping page ' + main_page_url + '\t|')
        print('+--------------------------------------------------------------+')  # \t\t

        soup = get_soup(main_page_url)

        for a in soup.findAll('a', {'class': 'title-journal'}):
            journal_endpoint = a.get('href')
            journal_page_url = base_url + journal_endpoint
            is_journal_scraped = scrape_specific_journal(
                journal_page_url, separator, article_list, journal_id)

            if is_journal_scraped is True:
                is_main_page_scraped = True
                journal_id += 1

        current_page_num += 1

        main_page_url = set_new_url_endpoint(
            current_page_num, main_page_url, separator)

    return is_main_page_scraped


def main():
    base_url = 'http://garuda.ristekdikti.go.id'
    separator = '?page='
    csv_header = ['JOURNAL_ID', 'JOURNAL_TITLE',
                  'ARTICLE_TITLE', 'ARTICLE_ABSTRACT']
    article_list = []

    article_list.append(csv_header)

    is_main_page_scraped = scrape_main_page(base_url, separator, article_list)

    print('+--------------------------------------------------------------+')  # \t\t

    if is_main_page_scraped is True:
        print('| Web pages have been scraped')
    else:
        print('| No web page has been scraped')

    # print article_list in a pretty manner
    # pprint(article_list)

    is_articles_saved = save_articles_csv(article_list)

    if is_articles_saved is True:
        print('| Articles have been saved as .csv')
    else:
        print('| Failed to save articles as .csv')

    print('+--------------------------------------------------------------+')  # \t\t


if __name__ == "__main__":
    main()

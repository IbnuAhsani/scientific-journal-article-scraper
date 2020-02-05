import re
import requests
from bs4 import BeautifulSoup


def get_soup(url):
    html_page_source_code_string = requests.get(url).text
    soup = BeautifulSoup(html_page_source_code_string, 'html.parser')

    return soup


def get_max_pages(soup):
    pagination_info_string = soup.find(
        'p', {'class': 'pagination-info'}).string.replace(" ", "")
    max_pages = int(re.search('of(.*)\\|', pagination_info_string).group(1))

    return max_pages


def scrape_specific_journal(url, separator):
    current_journal_page_num = 1

    soup = get_soup(url)
    max_pages = get_max_pages(soup)

    while current_journal_page_num <= max_pages:
        soup = get_soup(url)

        for xmp in soup.findAll('xmp', {'class': 'abstract-article'}):
            print(xmp.string)
            print('\n')

        current_journal_page_num += 1

        if current_journal_page_num == 2:
            url += separator + str(current_journal_page_num)
        else:
            url = url.split(separator, 1)[0]
            url += separator + str(current_journal_page_num)


def scrape_main_page(base_url, separator):
    current_main_page_num = 1
    url = base_url + '/journal'

    soup = get_soup(url)
    max_pages = get_max_pages(soup)

    while current_main_page_num <= max_pages:
        soup = get_soup(url)

        for a in soup.findAll('a', {'class': 'title-journal'}):
            journal_endpoint = a.get('href')
            specific_journal_url = base_url + journal_endpoint
            scrape_specific_journal(specific_journal_url, separator)

        current_main_page_num += 1


def main():
    base_url = 'http://garuda.ristekdikti.go.id'
    separator = '?page='

    scrape_main_page(base_url, separator)


if __name__ == "__main__":
    main()

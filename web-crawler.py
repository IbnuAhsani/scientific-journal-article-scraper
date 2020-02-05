import re
import requests
from bs4 import BeautifulSoup


def abstract_spider(url):
    current_page = 1
    separator = '?page='

    html_page_source_code_string = requests.get(url).text
    soup = BeautifulSoup(html_page_source_code_string, 'html.parser')
    pagination_info_string = soup.find(
        'p', {'class': 'pagination-info'}).string.replace(" ", "")

    max_pages = int(re.search('of(.*)\\|', pagination_info_string).group(1))

    while current_page <= max_pages:
        html_page_source_code_string = requests.get(url).text
        soup = BeautifulSoup(html_page_source_code_string, 'html.parser')

        for xmp in soup.findAll('xmp', {'class': 'abstract-article'}):
            print(xmp.string)
            print('\n')

        current_page += 1

        if current_page == 2:
            url += separator + str(current_page)
        else:
            url = url.split(separator, 1)[0]
            url += separator + str(current_page)


def journal_spider():
    current_page = 1
    base_url = 'http://garuda.ristekdikti.go.id'
    main_journal_url = base_url + '/journal'
    separator = '?page='

    html_page_source_code_string = requests.get(main_journal_url).text
    soup = BeautifulSoup(html_page_source_code_string, 'html.parser')
    pagination_info_string = soup.find(
        'p', {'class': 'pagination-info'}).string.replace(" ", "")

    max_pages = int(re.search('of(.*)\\|', pagination_info_string).group(1))

    while current_page <= max_pages:
        html_page_source_code_string = requests.get(main_journal_url).text
        soup = BeautifulSoup(html_page_source_code_string, 'html.parser')

        for a in soup.findAll('a', {'class': 'title-journal'}):
            journal_endpoint = a.get('href')
            specific_journal_url = base_url + journal_endpoint
            abstract_spider(specific_journal_url)

        current_page += 1


journal_spider()

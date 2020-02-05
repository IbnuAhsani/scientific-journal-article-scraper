import requests
from bs4 import BeautifulSoup


def abstract_spider(max_pages):
    page = 1
    url = 'http://garuda.ristekdikti.go.id/journal/view/11578'
    separator = '?page='

    while page <= max_pages:
        html_page_source_code = requests.get(url)
        html_page_plain_text = html_page_source_code.text
        soup = BeautifulSoup(html_page_plain_text, "html.parser")

        for xmp in soup.findAll('xmp', {'class': 'abstract-article'}):
            print(xmp.string)
            print('\n')

        page += 1

        if page == 2:
            url += separator + str(page)
        else:
            url = url.split(separator, 1)[0]
            url += separator + str(page)


abstract_spider(3)

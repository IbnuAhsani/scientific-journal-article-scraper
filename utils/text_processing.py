import requests
from bs4 import BeautifulSoup


def get_soup(url):
    html_page_source_code_string = requests.get(url).text
    soup = BeautifulSoup(html_page_source_code_string, 'html.parser')

    return soup


def set_new_url_endpoint(current_page_num, url, separator):
    if current_page_num == 2:
        url += separator + str(current_page_num)
    else:
        url = url.split(separator, 1)[0]
        url += separator + str(current_page_num)

    return url

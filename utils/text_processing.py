import requests
from bs4 import BeautifulSoup
from time import sleep


def get_soup(url):
    is_request_successful = False

    while is_request_successful is False:
        try:
            html_page_source_code_string = requests.get(url).text
            is_request_successful = True
            break
        except:
            print('connection refused by the server')
            print('taking a break for 5 seconds')
            sleep(5)
            continue

    soup = BeautifulSoup(html_page_source_code_string, 'html.parser')

    return soup


def set_new_url_endpoint(current_page_num, url, separator, sort_by):
    if current_page_num == 2:
        url += separator + str(current_page_num) + sort_by
    else:
        url = url.split(separator, 1)[0]
        url += separator + str(current_page_num) + sort_by

    return url

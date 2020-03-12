import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from time import sleep


def get_soup(url):
    is_request_successful = False
    session = requests.Session()

    while is_request_successful is False:
        try:
            retry = Retry(total=500, connect=3, backoff_factor=0.7)
            adapter = HTTPAdapter(max_retries=retry)

            session.mount('http://', adapter)
            session.mount('https://', adapter)

            html_page_source_code_string = session.get(url).text
            is_request_successful = True
            break
        except:
            print('connection refused by the server')
            print('taking a break for 3 seconds')
            sleep(3)
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

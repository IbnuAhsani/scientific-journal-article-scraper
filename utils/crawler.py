import re
import text_processing as tp
from langdetect import detect
from pprint import pprint


def scrape_specific_journal(url, separator, article_list, journal_id, article_id):
    is_journal_scraped = False
    current_page_num = 1

    soup = tp.get_soup(url)
    pagination_info_string = soup.find(
        'p', {'class': 'pagination-info'}).string.replace(" ", "")
    max_pages = int(re.search('of(.*)\\|', pagination_info_string).group(1))

    journal_title = soup.find(
        'div', {'class': 'j-meta-title'}).string.strip().encode('ascii', 'ignore')

    while current_page_num <= max_pages:
        soup = tp.get_soup(url)

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
            article = [journal_id, journal_title, article_id,
                       article_title, article_abstract]

            article_id += 1

            article_list.append(article)
            is_journal_scraped = True

        current_page_num += 1

        url = tp.set_new_url_endpoint(
            current_page_num, url, separator)

    print('| Scraped journal ' + journal_title)

    return is_journal_scraped, article_id


def scrape_main_page(journal_id, article_id, start_page, end_page, base_url, separator, article_list):
    is_main_page_scraped = False
    main_page_url = base_url + '/journal'
    current_page_num = start_page

    soup = tp.get_soup(main_page_url)

    while current_page_num <= end_page:
        if start_page != 1:
            main_page_url = tp.set_new_url_endpoint(
                current_page_num, main_page_url, separator)

        print('+--------------------------------------------------------------+')  # \t\t
        print('| Scraping page ' + main_page_url + '\t|')
        print('+--------------------------------------------------------------+')  # \t\t

        soup = tp.get_soup(main_page_url)

        for a in soup.findAll('a', {'class': 'title-journal'}):
            journal_endpoint = a.get('href')
            journal_page_url = base_url + journal_endpoint
            is_journal_scraped, article_id = scrape_specific_journal(
                journal_page_url, separator, article_list, journal_id, article_id)

            if is_journal_scraped is True:
                is_main_page_scraped = True
                journal_id += 1

        current_page_num += 1

        main_page_url = tp.set_new_url_endpoint(
            current_page_num, main_page_url, separator)

    return is_main_page_scraped

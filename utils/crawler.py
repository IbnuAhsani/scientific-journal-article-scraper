import re
import text_processing as tp
from langdetect import detect
from pprint import pprint


def crawl_specific_journal(url, separator, article_list, journal_id, article_id):
    is_journal_crawled = False
    current_page_num = 1
    sort_by = ''

    soup = tp.get_soup(url)
    article_item = soup.find('div', {'class': 'article-item'})

    if article_item is None:
        return is_journal_crawled, article_id

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

            is_period_exist = "." in article_abstract

            if is_period_exist is False:
                continue

            try:
                article_abstract_first_sentence = article_abstract.partition('.')[
                    2]

                article_title_language = detect(
                    article_title)
                article_abstract_language = detect(
                    article_abstract_first_sentence)
            except:
                article_title_language = 'error'
                article_abstract_language = 'error'

            if article_title_language != 'id' or article_abstract_language != 'id':
                continue

            article_abstract = article_abstract.replace("\n", " ")
            article = [journal_id, journal_title, article_id,
                       article_title, article_abstract]

            article_id += 1

            article_list.append(article)
            is_journal_crawled = True

        current_page_num += 1

        url = tp.set_new_url_endpoint(
            current_page_num, url, separator, sort_by)

    if is_journal_crawled is True:
        print('| crawled journal ' + journal_title)

    return is_journal_crawled, article_id


def crawl_main_page(journal_id, article_id, start_page, end_page, base_url, separator, sort_by, article_list):
    main_page_url = base_url + '/journals'
    current_page_num = start_page

    while current_page_num <= end_page:
        is_main_page_crawled = False

        if start_page != 1:
            main_page_url = tp.set_new_url_endpoint(
                current_page_num, main_page_url, separator, sort_by)

        soup = tp.get_soup(main_page_url)

        print('+--------------------------------------------------------------+')  # \t\t
        print('| crawling page ' + main_page_url + '\t|')
        print('+--------------------------------------------------------------+')  # \t\t

        for span in soup.findAll('span', {'class': 'index-val-small'}):
            is_journal_crawled = False
            a_tag = span.find('a', href=True)

            if a_tag is None:
                continue

            journal_page_url = a_tag['href']
            is_journal_crawled, article_id = crawl_specific_journal(
                journal_page_url, separator, article_list, journal_id, article_id)

            if is_journal_crawled is True:
                is_main_page_crawled = True
                journal_id += 1

        current_page_num += 1

        main_page_url = tp.set_new_url_endpoint(
            current_page_num, main_page_url, separator, sort_by)

    return is_main_page_crawled

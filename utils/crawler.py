import re
import text_processing as tp
from langdetect import detect
from pprint import pprint


class Crawler:

    def __init__(self, journal_id, article_id, start_page, end_page, base_url, journal_url, separator, sort_by):
        self.journal_id = journal_id
        self.article_id = article_id
        self.start_page = start_page
        self.end_page = end_page
        self.base_url = base_url
        self.journal_url = journal_url
        self.separator = separator
        self.sort_by = sort_by

    def crawl_specific_journal(self, article_list):
        is_journal_crawled = False
        current_page_num = 1
        sort_by = ''

        soup = tp.get_soup(self.journal_url)
        article_item = soup.find('div', {'class': 'article-item'})

        if article_item is None:
            return is_journal_crawled, self.article_id

        pagination_info_string = soup.find(
            'p', {'class': 'pagination-info'}).string.replace(" ", "")
        max_pages = int(
            re.search('of(.*)\\|', pagination_info_string).group(1))
        journal_title = soup.find(
            'div', {'class': 'j-meta-title'}).string.strip().encode('ascii', 'ignore')

        while current_page_num <= max_pages:
            soup = tp.get_soup(self.journal_url)

            for div in soup.findAll('div', {'class': 'article-item'}):
                article_title_div = div.find('a', {'class': 'title-article'})
                article_title = article_title_div.find('xmp').string
                article_abstract = div.find(
                    'xmp', {'class': 'abstract-article'}).string

                if article_abstract is None or article_title is None:
                    continue

                article_title = article_title.encode('ascii', 'ignore')
                article_abstract = article_abstract.encode('ascii', 'ignore')
                article_abstract = article_abstract.replace("\n", " ")

                is_period_exist = "." in article_abstract

                if is_period_exist is False:
                    continue

                try:
                    article_title_language = detect(
                        article_title)
                    article_abstract_sentences = article_abstract.split('.')
                    article_abstract_first_sentence = article_abstract_sentences[1]
                    article_abstract_last_sentence = article_abstract_sentences[-2]

                    article_abstract_first_sentence_language = detect(
                        article_abstract_first_sentence)
                    article_abstract_last_sentence_language = detect(
                        article_abstract_last_sentence)
                except:
                    article_title_language = 'error'
                    article_abstract_first_sentence_language = 'error'
                    article_abstract_last_sentence_language = 'error'

                if article_title_language != 'id' or article_abstract_first_sentence_language != 'id' or article_abstract_last_sentence_language != 'id':
                    continue

                article = [self.journal_id, journal_title, self.article_id,
                           article_title, article_abstract]

                self.article_id += 1

                article_list.append(article)
                is_journal_crawled = True

            if current_page_num > 100:
                break

            current_page_num += 1

            self.journal_url = tp.set_new_url_endpoint(
                current_page_num, self.journal_url, self.separator, sort_by)

        if is_journal_crawled is True:
            print('| crawled journal ' + journal_title)

        return is_journal_crawled, self.article_id

    def crawl_main_page(self, article_list):

        main_page_url = self.base_url + '/journals'
        current_page_num = self.start_page

        while current_page_num <= self.end_page:
            is_main_page_crawled = False

            if self.start_page != 1:
                main_page_url = tp.set_new_url_endpoint(
                    current_page_num, main_page_url, self.separator, self.sort_by)

            soup = tp.get_soup(main_page_url)

            # \t\t
            print('+--------------------------------------------------------------+')
            print('| crawling page ' + main_page_url + '\t|')
            # \t\t
            print('+--------------------------------------------------------------+')

            for span in soup.findAll('span', {'class': 'index-val-small'}):
                is_journal_crawled = False
                a_tag = span.find('a', href=True)

                if a_tag is None:
                    continue

                journal_page_url = a_tag['href']
                self.journal_url = journal_page_url
                is_journal_crawled, self.article_id = self.crawl_specific_journal(
                    article_list)

                if is_journal_crawled is True:
                    is_main_page_crawled = True
                    self.journal_id += 1

            current_page_num += 1

            main_page_url = tp.set_new_url_endpoint(
                current_page_num, main_page_url, self.separator, self.sort_by)

        return is_main_page_crawled

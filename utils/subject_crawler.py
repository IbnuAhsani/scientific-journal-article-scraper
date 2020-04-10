import re
import text_processing as tp
from langdetect import detect
from pprint import pprint


class SubjectCrawler:

    def __init__(self, start_page, end_page, page_limit, base_url, journal_url, separator, sort_by):
        self.start_page = start_page
        self.end_page = end_page
        self.page_limit = page_limit
        self.base_url = base_url
        self.journal_url = journal_url
        self.separator = separator
        self.sort_by = sort_by

    def crawl_specific_journal(self, article_list):
        is_journal_crawled = False
        sort_by = ''

        soup = tp.get_soup(self.journal_url)
        article_item_tag = soup.find('div', {'class': 'article-item'})

        if article_item_tag is None:
            return is_journal_crawled

        journal_title = soup.find(
            'div', {'class': 'j-meta-title'}).string.strip().encode('ascii', 'ignore')
        journal_subjects_tag = soup.find(
            'div', {'class': 'j-meta-subject'})

        if journal_subjects_tag is None:
            print('| journal ' + journal_title + ' was not crawled')
            return is_journal_crawled

        journal_subjects_text = journal_subjects_tag.text.strip().encode('ascii', 'ignore')
        journal_subjects = journal_subjects_text.splitlines(False)
        searched_subjects = ['Computer Science & IT', 'Mathematics']
        is_subjects_included = False

        for searched_subject in searched_subjects:
            if searched_subject in journal_subjects:
                is_subjects_included = True
                break

        if is_subjects_included is True:
            journal_subjects_concat = ''

            for journal_subject in journal_subjects:
                if journal_subject == journal_subjects[-1]:
                    journal_subjects_concat += journal_subject
                else:
                    journal_subjects_concat += journal_subject + ', '

            journal = [journal_title, journal_subjects_concat]
            article_list.append(journal)

            is_journal_crawled = True
            print('| crawled journal ' + journal_title)
        else:
            print('| journal ' + journal_title + ' was not crawled')

        return is_journal_crawled

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

            url_list = list()

            for span in soup.findAll('span', {'class': 'index-val-small'}):
                is_journal_crawled = False
                a_tag = span.find('a', href=True)

                if a_tag is None:
                    continue

                journal_page_url = a_tag['href']
                url_list.append(journal_page_url)

            unique_url_list = list()

            for x in url_list:
                if x not in unique_url_list:
                    unique_url_list.append(x)

            for url in unique_url_list:
                self.journal_url = url
                is_journal_crawled = self.crawl_specific_journal(article_list)

                if is_journal_crawled is True:
                    is_main_page_crawled = True

            current_page_num += 1

            main_page_url = tp.set_new_url_endpoint(
                current_page_num, main_page_url, self.separator, self.sort_by)

        return is_main_page_crawled

import csv
from utils import subject_crawler, file_system as fs

SAVE_PATH = "./data/subject/journal-subject.csv"


def main():
    start_page = 101
    end_page = 150
    page_limit = 0
    base_url = 'http://sinta2.ristekdikti.go.id'
    journal_url = ''
    separator = '?page='
    sort_by = '&sort=impact'

    web_crawler = subject_crawler.SubjectCrawler(
        start_page,
        end_page,
        page_limit,
        base_url,
        journal_url,
        separator,
        sort_by,
    )

    with open(SAVE_PATH) as f:
        reader = csv.reader(f)
        csv_data = list(reader)

    journal_list = []
    csv_data_length = len(csv_data)

    if csv_data_length == 0:
        csv_header = ['JOURNAL_TITLE', 'JOURNAL_SUBJECTS']
        journal_list.append(csv_header)

    is_main_page_crawled = web_crawler.crawl_main_page(journal_list)

    print('+--------------------------------------------------------------+')  # \t\t

    if is_main_page_crawled is True:
        print('| web pages have been crawled')
    else:
        print('| no web page has been crawled')

    if csv_data_length == 0:
        is_articles_saved = fs.save_articles_csv(SAVE_PATH, journal_list)
    else:
        for journal in journal_list:
            csv_data.append(journal)
        is_articles_saved = fs.save_articles_csv(SAVE_PATH, csv_data)

    if is_articles_saved is True:
        print('| articles have been saved as .csv')
    else:
        print('| failed to save articles as .csv')

    print('+--------------------------------------------------------------+')  # \t\t


if __name__ == '__main__':
    main()

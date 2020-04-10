from utils import subject_crawler, file_system as fs

SAVE_PATH = "./output/journal-subject.csv"


def main():
    start_page = 1
    end_page = 1
    page_limit = 2
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

    csv_header = ['JOURNAL_TITLE', 'JOURNAL_SUBJECTS']
    journal_list = []

    journal_list.append(csv_header)

    is_main_page_crawled = web_crawler.crawl_main_page(journal_list)

    print('+--------------------------------------------------------------+')  # \t\t

    if is_main_page_crawled is True:
        print('| web pages have been crawled')
    else:
        print('| no web page has been crawled')

    is_articles_saved = fs.save_articles_csv(SAVE_PATH, journal_list)

    if is_articles_saved is True:
        print('| articles have been saved as .csv')
    else:
        print('| failed to save articles as .csv')

    print('+--------------------------------------------------------------+')  # \t\t


if __name__ == '__main__':
    main()

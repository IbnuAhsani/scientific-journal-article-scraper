from utils import crawler, file_system as fs

SAVE_PATH = "./output/output.csv"


def main():
    start_page = 1
    end_page = 1
    page_limit = 1
    base_url = 'http://sinta.ristekbrin.go.id'
    journal_url = ''
    separator = '?page='
    sort_by = '&sort=impact'

    web_crawler = crawler.Crawler(
        start_page,
        end_page,
        page_limit,
        base_url,
        journal_url,
        separator,
        sort_by,
    )

    csv_header = ['JOURNAL_TITLE', 'ARTICLE_TITLE', 'ARTICLE_ABSTRACT']
    article_list = []

    article_list.append(csv_header)

    is_main_page_crawled = web_crawler.crawl_main_page(article_list)

    print('+--------------------------------------------------------------+')  # \t\t

    if is_main_page_crawled is True:
        print('| web pages have been crawled')
    else:
        print('| no web page has been crawled')

    is_articles_saved = fs.save_articles_csv(SAVE_PATH, article_list)

    if is_articles_saved is True:
        print('| articles have been saved as .csv')
    else:
        print('| failed to save articles as .csv')

    print('+--------------------------------------------------------------+')  # \t\t


if __name__ == '__main__':
    main()

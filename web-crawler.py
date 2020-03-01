from utils import crawler, file_system as fs


def main():
    start_page = 16
    end_page = 20
    base_url = 'http://sinta2.ristekdikti.go.id'
    journal_url = ''
    separator = '?page='
    sort_by = '&sort=impact'

    web_crawler = crawler.Crawler(
        start_page,
        end_page,
        base_url,
        journal_url,
        separator,
        sort_by,
    )

    csv_header = ['JOURNAL_ID', 'JOURNAL_TITLE', 'ARTICLE_ID',
                  'ARTICLE_TITLE', 'ARTICLE_ABSTRACT']
    article_list = []

    article_list.append(csv_header)

    is_main_page_crawled = web_crawler.crawl_main_page(article_list)

    print('+--------------------------------------------------------------+')  # \t\t

    if is_main_page_crawled is True:
        print('| web pages have been crawled')
    else:
        print('| no web page has been crawled')

    # print article_list in a pretty manner
    # pprint(article_list)

    save_path = "./output/output.csv"

    is_articles_saved = fs.save_articles_csv(save_path, article_list)

    if is_articles_saved is True:
        print('| articles have been saved as .csv')
    else:
        print('| failed to save articles as .csv')

    print('+--------------------------------------------------------------+')  # \t\t


if __name__ == '__main__':
    main()

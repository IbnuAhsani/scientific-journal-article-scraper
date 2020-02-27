from utils import crawler


def main():
    first_journal_id = 1
    first_article_id = 1
    start_page = 1
    end_page = 1
    base_url = 'http://garuda.ristekdikti.go.id'
    separator = '?page='
    csv_header = ['JOURNAL_ID', 'JOURNAL_TITLE', 'ARTICLE_ID',
                  'ARTICLE_TITLE', 'ARTICLE_ABSTRACT']
    article_list = []

    article_list.append(csv_header)

    is_main_page_scraped = crawler.scrape_main_page(
        first_journal_id, first_article_id, start_page, end_page, base_url, separator, article_list)

    print('+--------------------------------------------------------------+')  # \t\t

    if is_main_page_scraped is True:
        print('| Web pages have been scraped')
    else:
        print('| No web page has been scraped')

    # print article_list in a pretty manner
    # pprint(article_list)

    is_articles_saved = crawler.save_articles_csv(article_list)

    if is_articles_saved is True:
        print('| Articles have been saved as .csv')
    else:
        print('| Failed to save articles as .csv')

    print('+--------------------------------------------------------------+')  # \t\t


if __name__ == '__main__':
    main()

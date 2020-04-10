from operator import itemgetter
from utils import file_system as fs

DATASET_DIR = "./output/dataset-test.csv"
SAVE_PATH = "./output/output-trimmed.csv"


def main():
    csv_data_list = fs.read_csv_list(DATASET_DIR)
    minimum_article = 150
    i = 0

    while i < len(csv_data_list):
        is_next_row_journal_title_same = True
        j = i + 1
        num_article = 1

        current_row = csv_data_list[i]
        current_journal_title = itemgetter('JOURNAL_TITLE')(current_row)

        while is_next_row_journal_title_same and j < len(csv_data_list):
            next_row = csv_data_list[j]
            next_journal_title = itemgetter('JOURNAL_TITLE')(next_row)

            if next_journal_title != current_journal_title:
                is_next_row_journal_title_same = False
                break

            num_article += 1
            j += 1

        if num_article < minimum_article:
            del csv_data_list[i:j]
        else:
            i = j

    article_list = []

    csv_header = ['JOURNAL_ID', 'JOURNAL_TITLE', 'ARTICLE_ID',
                  'ARTICLE_TITLE', 'ARTICLE_ABSTRACT']

    article_list.append(csv_header)

    for i in range(len(csv_data_list)):
        row = csv_data_list[i]

        sinta_index, journal_title, article_title, article_abstract = itemgetter(
            'SINTA_INDEX', 'JOURNAL_TITLE', 'ARTICLE_TITLE', 'ARTICLE_ABSTRACT')(row)
        article = [0, journal_title, 0, article_title, article_abstract]

        article_list.append(article)

    fs.save_articles_csv(SAVE_PATH, article_list)


if __name__ == '__main__':
    main()

from operator import itemgetter
from utils import file_system as fs

DATASET_DIR = "./output/dataset-master-sinta.csv"
SAVE_PATH = "./output/output-indexed.csv"


def main():
    csv_data_list = fs.read_csv_list(DATASET_DIR)
    article_id = 0
    journal_id = 0
    article_list = []

    csv_header = ['JOURNAL_ID', 'JOURNAL_TITLE', 'ARTICLE_ID',
                  'ARTICLE_TITLE', 'ARTICLE_ABSTRACT']

    article_list.append(csv_header)

    for i in range(len(csv_data_list) - 1):
        current_row = csv_data_list[i]
        next_row = csv_data_list[i + 1]

        current_journal_title, current_article_title, current_article_abstract = itemgetter(
            'JOURNAL_TITLE', 'ARTICLE_TITLE', 'ARTICLE_ABSTRACT')(current_row)
        next_journal_title = itemgetter('JOURNAL_TITLE')(next_row)

        article = [journal_id, current_journal_title, article_id,
                   current_article_title, current_article_abstract]

        article_list.append(article)

        if next_journal_title != current_journal_title:
            journal_id += 1

        article_id += 1

    fs.save_articles_csv(SAVE_PATH, article_list)


if __name__ == '__main__':
    main()
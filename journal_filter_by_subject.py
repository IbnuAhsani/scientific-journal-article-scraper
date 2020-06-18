from operator import itemgetter
from utils import file_system as fs


DATASET_PATH = "./output/dataset-test.csv"
JOURNAL_SUBJECTS_PATH = "./output/journal-subject-cs-math.csv"
SAVE_PATH = "./output/output-filtered-by-subject.csv"


def main():

    subject_list = []
    csv_subject_data = fs.read_csv_list(JOURNAL_SUBJECTS_PATH)

    for i in range(len(csv_subject_data)):
        row = csv_subject_data[i]

        journal_title, journal_subjects = itemgetter(
            'JOURNAL_TITLE', 'JOURNAL_SUBJECTS')(row)

        subject_list.append(journal_title)

    journal_list = []
    csv_header = ['JOURNAL_TITLE', 'ARTICLE_TITLE', 'ARTICLE_ABSTRACT']

    journal_list.append(csv_header)

    csv_journal_data = fs.read_csv_list(DATASET_PATH)

    for i in range(len(csv_journal_data)):
        row = csv_journal_data[i]

        journal_title, article_title, article_abstract = itemgetter(
            'JOURNAL_TITLE', 'ARTICLE_TITLE', 'ARTICLE_ABSTRACT')(row)

        is_journal_included = journal_title in subject_list

        if is_journal_included is True:
            journal = [journal_title, article_title, article_abstract]
            journal_list.append(journal)

    is_articles_saved = fs.save_articles_csv(SAVE_PATH, journal_list)


if __name__ == '__main__':
    main()

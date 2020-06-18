import os
from operator import itemgetter
from utils import file_system as fs
from langdetect import detect


DATASET_DIR = "./output/dataset-test.csv"
SAVE_PATH = "./output/output-english-sentence-removed.csv"


def main():
    csv_data_list = fs.read_csv_list(DATASET_DIR)
    article_id = 0
    journal_id = 0
    article_list = []

    csv_header = ['JOURNAL_ID', 'JOURNAL_TITLE', 'ARTICLE_ID',
                  'ARTICLE_TITLE', 'ARTICLE_ABSTRACT']

    article_list.append(csv_header)

    for i in range(len(csv_data_list)):
        row = csv_data_list[i]

        sinta_index, journal_title, article_title, article_abstract = itemgetter(
            'SINTA_INDEX', 'JOURNAL_TITLE', 'ARTICLE_TITLE', 'ARTICLE_ABSTRACT')(row)

        if article_abstract[-1] != '.':
            article_abstract += '.'

        article_abstract_sentences = article_abstract.split('.')

        j = 0
        article_english_sentence_removed = ''

        while article_abstract_sentences[j]:
            article_sentence = article_abstract_sentences[j]

            try:
                article_sentence_language = detect(article_sentence)
            except:
                article_sentence_language = 'error'

            if(article_sentence_language == 'en'):
                article_abstract_sentences.remove(article_sentence)
                continue

            if j == 0:
                article_english_sentence_removed += article_sentence
            else:
                article_english_sentence_removed += '. ' + article_sentence

            j += 1

        article = [journal_id, journal_title,
                   article_id, article_title, article_english_sentence_removed]

        article_list.append(article)

    fs.save_articles_csv(SAVE_PATH, article_list)

    duration = 0.5
    freq = 440
    os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))


if __name__ == '__main__':
    main()

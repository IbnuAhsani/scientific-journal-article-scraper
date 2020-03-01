import csv
import io


def save_articles_csv(path, article_list):
    is_articles_saved = True

    try:
        with open(path, "w") as csvfile:
            writer = csv.writer(csvfile)

            for article in article_list:
                writer.writerow(article)
    except:
        is_articles_saved = False

    return is_articles_saved


def read_csv_list(file_dir):
    with io.open(file_dir, mode="r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        dictionary_list = list(reader)

    return dictionary_list

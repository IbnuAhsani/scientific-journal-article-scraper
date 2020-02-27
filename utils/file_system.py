import csv


def save_articles_csv(article_list):
    is_articles_saved = True

    try:
        with open("output.csv", "w") as csvfile:
            writer = csv.writer(csvfile)

            for article in article_list:
                writer.writerow(article)
    except:
        is_articles_saved = False

    return is_articles_saved

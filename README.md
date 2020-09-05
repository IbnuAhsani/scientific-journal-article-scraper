# Scientific Journal Web Scraper

A web crawler that scrapes Indonesian scientific journal and article data from [SINTA - Science and Technology Index](http://sinta.ristekbrin.go.id/) and [GARUDA - Garda Rujukan Digital](http://garuda.ristekbrin.go.id/), built using [Python3](https://www.python.org/download/releases/3.0/) and [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/). 

## How To Run

```
$ python scrape_web
```

## Features

A single agent will traverse the table in `http://sinta.ristekbrin.go.id/journals` and check each row for the `<img>` tag with the class `stat-garuda-small`. If the tag exists, the agent will go deeper by accessing the `url` listed in the `href` property that's anchored to the `<a>` tag in that specific row. The agent will then traverse the table in said `url`, scraping text data from the `<xmp>` tag with the class `abstract-article`. The script will append `"?page=2"` to the `url` and increment the page number to continue traversing the following pages. Only after the pages have run out will the agent exit the nested traversal process and continue the main traversal process.

Since this program is targeted to collect **Indonesian** scientific journal and article data, the library [langdetect](https://pypi.org/project/langdetect/) is utilized to make sure that the text data that's scraped is Indonesian. The language checking process is done by splitting the first two sentences of the paragraph and checking the language of both sentences. If the language of one of the two sentences is not Indonesian, then the paragraph would not be scraped. 

The data that's scraped is saved in a `.csv` file with the `csv header` being `JOURNAL_TITLE`, `ARTICLE_TITLE`, and `ARTICLE_ABSTRACT`. The scraped data is saved in `/data/master` directory and the last time the data is scraped is on April 1st, 2020. The amount of data scraped thus far is 157,687 rows, consisting of 2,527 journals. 

## Library Used

- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [langdetect](https://pypi.org/project/langdetect/)
- [requests](https://requests.readthedocs.io/en/master/)

## Demo

![](https://media.giphy.com/media/QwyKOyo6te9BsTdAMk/giphy.gif)

## License

MIT © [ssentinull](https://github.com/ssentinull)
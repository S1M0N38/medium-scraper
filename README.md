# Medium Scraper

medium-scraper (*MS*) is a scraper build using [Scrapy](https://scrapy.org/)
framework for scrape [Medium](https://medium.com/) posts.

> :warning: If you need only the scraped data check out the kaggle dataset (NOT READY)

## :wrench: How it works

*MS* consist of two scrapy [spider](https://docs.scrapy.org/en/latest/topics/spiders.html):
**post_id** and **post**.

First *MS* the look for the *post_id* (a unique identifier of a post) inside the
Sitemap of medium website and store the found *post_id* in a
[SQLite](https://sqlite.org/index.html).

Then the second spider (**post**) takes the *post_id* from database and permform
a request for obstain the specific data for every post. Data about a post can
be divided in two groups: *posts*, and *paragraphs*. These are store in
different tables inside database.

## :books: Database structure

All scraped data are store in a SQLite file (.db).
To Create a new databese file create a duplicate of `example.db` and
then rename it to `medium.db`. If you want use a grafical interface for interact
with databese I suggest [DB Browser for SQLite](https://sqlitebrowser.org/).

As I said before database consists of two tables: *post* and *paragraph*.

### post

| post_id        | available | creator_id     | language | first_published_at | title      | word_count | claps  | tags      |
| :------------: |:---------:| :-------------:| :------: | :----------------: | :--------: | :--------: | :----: | :-------: |
| `316d066db3d6` | `1`       | `245c7224d0ce` | `en`     | `1577865630099`    | `Intro...` | `4231`     | `341`  | `cow,dog` |
| `5edbf9af44af` | `0`       | `NULL`         | `NULL`   | `NULL`             | `NULL`     | `NULL`     | `NULL` | `NULL`    |
| `fec8331faa9d` | `NULL`    | `NULL`         | `NULL`   | `NULL`             | `NULL`     | `NULL`     | `NULL` | `NULL`    |
| `...`          | `...`     | `...`          | `...`    | `...`              | `...`      | `...`      | `...`  | `...`     |

- **post_id**
  - a unique identifier for the post
- **available**
  - `NULL` the post spider never try to scrape this post_id
  - `1` the post spider scrape succesfully this post_id
  - `0` the post spider faild to scrape this post_id
- **creator_id**
  - a unique identifier for the creator of the post
- **language**
  - the language of the content of the post (detected by Medium)
- **first_published_at**
  - timestamp (milliseconds) of the first pubblication of the post
- **title**
  - the title of the post (can be not unique)
- **word_count**
  - the number of words contain in the post content
- **claps**
  - the total number of claps (on medium.com claps == likes)
- **tags**
  - the tags related to the post (comma separated)

### paragraph

| post_id        | index | name   | type  | text                                 |
| :------------: |:-----:|:------:| :----:| :----------------------------------: |
| `316d066db3d6` | `0`   | `6f86` | `3`   | `One important thing productful ...` |
| `316d066db3d6` | `1`   | `eabd` | `1`   | `Quality ≠ Money`                    |
| `3526667dacfb` | `0`   | `94db` | `1`   | `Income in Development ...`          |
| `...`          | `...` | `...`  | `...` | `...`                                |

- **post_id**
  - a unique identifier for the post
- **index**
  - the order of the paragraphs of a post (starting from 0)
- **name**
  - a unique identifier for the paragraph (inside post)
- **type**
  - `1` normal
  - `3` big bold header
  - `6` quote
  - `7` quote bigger and in the center
  - `9` bullet list
  - `10` ordered list
  - `13` small bold header
- **text**
  - the text inside the paragraph

*Information about italic, bold, code and link stored in the markup list,
currently not scraped by MS*

## :arrow_down: Installation

1. Clone this repo: `git clone https://github.com/S1M0N38/medium-scraper.git`
2. Move inside the cloned repo: `cd scraper-medium`
3. Install dependecies with [pipenv](https://pipenv.readthedocs.io/en/latest/):
   `pipenv install`
4. Enter the virtualenv: `pipenv shell`
5. Check the installation: `scrapy version`

## :zap: Usage

First you need ad .db where store data read
[Database Structure](https://github.com/S1M0N38/medium-scraper#books-database-structure).
Then be sure to be at the root level of medium-scraper repo and activate
the virtualenv with `pipenv shell`

### post_id spider

- **Description** this spider populate the post_id column of the post table

- **Arguments** if no arguemnt is provide, this spider start scraping the whole
  site starting from the foundation year of Medium. Otherwise you can specify
  the date you want to scrape.

- **Examples**
  - `scrapy crawl post_id`
    scarpe post_id of whole website (not recommended)
  - `scrapy crawl post_id -a year=2020`
    scarpe post_id of posts published in 2020
  - `scrapy crawl post_id -a year=2020 -a month=01`
    scarpe post_id of posts published in Jan 2020
  - `scrapy crawl post_id -a year=2020 -a month=01 -a day=01`
    scarpe post_id of posts published on 1st of Jan 2020

### post spider

- **Description** Look in the database for post_id with `NULL` available and
  collect more information saved in post and paragraph tables.

- **Arguments** no arguemnts can be passed

- **Examples**
  - `scrapy crawl post`

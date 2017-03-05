# Campus News Bot Scraper


Campus News Bots (CNB) is a daemon that scrapes UNITN website feeds for news
and sends the content to Telegram Channels.

### Terminology

* channel: A telegram channel
* feed: a page on the university website with some news feed
* news: a single announcement on a feed (e.g. "Class X is suspended tomorrow")
* scraping: visiting a feed in search of fresh news


## Channels

The relevant feeds and channels are the following:

* Disi:
  * Feed: [http://www.science.unitn.it/cisca/avvisi/avvisi.php](http://www.science.unitn.it/cisca/avvisi/avvisi.php)
  * Channel: [https://t.me/UnitnDisiNews](https://t.me/UnitnDisiNews)
* Dii-CIBIO:
  * Feed: [http://www.science.unitn.it/avvisiesami/dii-cibio/](http://www.science.unitn.it/avvisiesami/dii-cibio/)
  * Channel: [https://t.me/UnitnDiiCibioNews](https://t.me/UnitnDiiCibioNews)
* Dicam:
  * Feed: [http://www.science.unitn.it/avvisiesami/dicam/index_avvisi.php](http://www.science.unitn.it/avvisiesami/dicam/index_avvisi.php)
  * Channel: [https://t.me/UnitnDicamNews](https://t.me/UnitnDicamNews)
* Giuri:
  * Feed: [http://www.giurisprudenza.unitn.it/371/avvisi-dei-docenti](http://www.giurisprudenza.unitn.it/371/avvisi-dei-docenti)
  * Channel: [https://t.me/UnitnGiuriNews](https://t.me/UnitnGiuriNews)
* Lettere:
  * Feed: [http://web.unitn.it/lettere/6419/avvisi](http://web.unitn.it/lettere/6419/avvisi)
  * Channel: [https://t.me/UnitnLettereNews](https://t.me/UnitnLettereNews)
* Economia:
  * Feed: [http://www.economia.unitn.it/68/avvisi-dei-docenti](http://www.economia.unitn.it/68/avvisi-dei-docenti)
  * Channel: [https://t.me/UnitnEconomiaNews](https://t.me/UnitnEconomiaNews)
* Cogsci:
  * Feed: [http://webmagazine.unitn.it/news/cogsci](http://webmagazine.unitn.it/news/cogsci)
  * Channel: [https://t.me/UnitnCogsciNews](https://t.me/UnitnCogsciNews)
* Sociologia:
  * Feed: [http://webmagazine.unitn.it/news/sociologia](http://webmagazine.unitn.it/news/sociologia)
  * Channel: [https://t.me/UnitnSociologiaNews](https://t.me/UnitnSociologiaNews)

## News and deduplication

Scraping the feeds for content is not a trivial problem: since the individual
news do not have an `id` provided by their sources, an algorithm had to be
devised to *deduplicate* the content; that is, to determine which of the scraped
news are new to the system and which ones have already been sent to the channels.

To solve this problem, one cannot just compare every scraped news with **all**
the previously obtained ones, doing so would mistakenly silence those messages
that are sent periodically.

Our current solution compares a scraped news with the last `N` news (in
descending cronological order) where `N` is determined as follows:
`constant_factor * len(scraped_feed)`.
`constant_factor` is defined in config as `old_news_factor`.

## Architecture

The introduction of Telegram channels notably simplified the CNB architecture;
it now consist of a single Telegram bot that post once per news to the appropriate channel.

As opposed to the legacy system (pre-channels) where a separate service written
in `golang` had to send the messages to every subscriber on an individual chat.

The Architecture now comprises the following systems:

### Data (`models.py`, `config.json`)

CNB relies on a json file (`config.json`) for configuration,
while the scraped news are saved in a `sqlite` database whose schema is defined
in `models.py`.


### Scrapers (`scrapers.py`)

The scrapers visit the university websites at regular intervals, looking for new
content.

The `Scraper` class defines a generic scraper, while its subclasses encompass
the custom logic needed to parse each particular page.


### Sender (`telegram.py`)

The `Sender` queries the database for messages whose `send_date` is `null`
and sends them to the appropriate Telegram Channels.

The function `send_admin` is used to report errors to the admin via a Telegram
group.


### Utilities

The repo also contains two utilities:

* `stats.py`: prints the amount of subscribers per channel
* `announcement.py`: sends an admin defined message to all channels


## Packaging

The project is packaged for production using [Docker](https://www.docker.com/).


## Run

In order to run CNB:
  * install `docker` and `docker-compose` on the production server (instructions on the docker site)
  * clone the git on the production server
  * Update `config.json` with the secret data (keep out of the public repo!!):
    * the bot secret key
    * the admin chat id
  * set bot enabled to `false` in `config.json` to prevent a flood of old messages to the channels
  * run `docker-compose up -d` to start the server
  * wait for all the scrapers to complete one scraping
  * set bot enabled to `true`

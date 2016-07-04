# Campus News Bot Scraper

## Deployment

The app is composed of two services:

* A RethinkDB database
* An instance of the scraper service

The `docker-compose.yml` file fully describes this architecture.

The database schema is automatically created by the application when no existing database is detected.

## DB Model
### news
```
{"text": "foobar",
 "author": "John Snow",
 "id": 123-456,
 "send_date": Mon Gen 01 2016 23:21:29 GMT+00:00,
 "chat": "lettere",
 "fetch_date": Mon Gen 01 2016 23:21:29 GMT+00:00}
 ```

### bots
```
{"id": "cnb",
 "bot_id": "2343409:LDAS78BNOOW-jfhewokj"}
 ```

### chats
```
{"id": "lettere",
 "url": "http://unitn.it/~lettere",
 "chat_id":"UnitnLettereNews"}
 ```

# CNB scraper

![Version 1.0.1](https://img.shields.io/badge/version-1.0.1-brightgreen.svg)

The scraper module of the Campus News Bot periodically checks a given set of
webpages for news and pushes them to the orchestrator on the appropriate channel.

# Architecture
The present repository contains the `scraper`, which should be imported as a module and used as follow:
* create an empty project directory, let's say `myuni-scraper`
* clone this repo in `myuni-scraper/scraper`
* copy the whole content of  `myuni-scraper/scraper/example` into `myuni-scraper`
* customize the configuration file (`myuni-scraper/config.yaml`) as needed
* create your scrapers subclassing `Scraper` as shown in `myuni-scraper/scraper_mydepartment.py`
* modify `myuni-scraper/manage.py` importing the newly created scrapers
* install the needed dependencies by issuing `pip install -r scraper/requirements.txt`


In the end the project should look as follows:
```
.
├── config.yaml
├── Dockerfile
├── manage.py
├── scraper
│   ├── app.py
│   ├── config.py
│   ├── Dockerfile
│   ├── example
│   a│   ├── config.yaml
│   │   ├── Dockerfile
│   │   ├── manage.py
│   │   └── scraper_mydepartment.py
│   ├── __init__.py
│   ├── logger.py
│   ├── README.md
│   ├── requirements.txt
│   ├── schema.py
│   ├── scraper.py
│   └── serializer.py
├── scraper_mydepartment1.py
├── scraper_mydepartment2.py
├── ...
└── scraper.log
```

# Run
* Issue `python manage.py init` to create the needed tables in the database
* Issue `python manage.py run` to run the app
* Issue `python manage.py run --stealth` to run the app without hitting the orchestrator, in case you just want to play around without flooding your users with messages

# Dockerization
In case you want to dockerize the scraper, a `Dockerfile` is already prepared.
All you have to do is:
* `docker build -t cnb/scraper .` to create the image
* `docker run --name cnb-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres` to create a postgres instance
* change the postgres host to `postgres` in `config.yaml`
* `docker run -t -i --link cnb-postgres:postgres -v config.yaml:/config.yaml cnb/scraper python /app/manage.py init` to init the database
* `docker run -t -i --link cnb-postgres:postgres -v config.yaml:/config.yaml -d cnb/scraper` to launch the container

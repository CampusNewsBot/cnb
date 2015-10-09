FROM debian:jessie
MAINTAINER Simone Accascina <simon@accascina.me>

ADD . /app

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
    libpq-dev \
    libxml2-dev \
    libxslt-dev \
    python2.7 \
    python-dev \
    python-pip \
    && apt-get -y autoremove \
    && apt-get clean \
    && pip install -r /app/scraper/requirements.txt

CMD ["python", "/app/manage.py", "run"]

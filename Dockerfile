FROM python:3.5-alpine
MAINTAINER Simone Accascina <simon@accascina.me>

ADD . /app/
WORKDIR /app/

RUN pip install -r requirements.txt

CMD ["python3", "/app/main.py", "-c", "/config.yaml"]

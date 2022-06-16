FROM python:3.10

ADD . /docker-app

WORKDIR /docker-app

RUN pip install --no-cache-dir -r requirements.txt

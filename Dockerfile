FROM python:3.10

WORKDIR /code-docker

COPY ./requirements.txt /code-docker/requirements.txt

RUN pip3 install -r requirements.txt

CMD [ "python3", "-m" , "flask", "run", ".0.0.0:5000", "main:app"]



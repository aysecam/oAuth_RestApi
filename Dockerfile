#Pulling required images 
FROM mongo:6.0  

FROM python:3.10

WORKDIR /python-docker

COPY ./requirements.txt /python-docker/requirements.txt

#pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install -r requirements.txt 

#Exposing the default ports
EXPOSE 27017
EXPOSE 5000

COPY . /python-docker

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]










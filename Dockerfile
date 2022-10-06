FROM python:3.10

RUN mkdir -m 777 -p /app
WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt update
RUN apt install postgresql -y

RUN pip3 install --no-cache-dir --requirement /app/requirements.txt;

COPY . .


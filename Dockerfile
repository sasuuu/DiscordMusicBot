# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN apt update
RUN apt -y install ffmpeg

COPY . .

CMD [ "python3", "main.py" ]
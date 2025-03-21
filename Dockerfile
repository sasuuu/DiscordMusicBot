# syntax=docker/dockerfile:1

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt update
RUN apt -y install ffmpeg

COPY . .

CMD [ "python", "main.py" ]
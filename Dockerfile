# syntax=docker/dockerfile:1

FROM python:3

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

RUN apt-get update \
  && apt-get install -y chromium chromium-driver

EXPOSE 8000
USER 1000

CMD ["python", "BotTelegram_Kong.py"]
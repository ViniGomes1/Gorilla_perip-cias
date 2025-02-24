# syntax=docker/dockerfile:1

FROM python:3

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

RUN apt-get update && apt-get install -y wget unzip && \
  wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
	apt install -y ./google-chrome-stable_current_amd64.deb && \
	rm google-chrome-stable_current_amd64.deb && \ 
	apt-get clean

ENV FLASK_APP=BotTelegram_Kong.py

EXPOSE 5000

CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
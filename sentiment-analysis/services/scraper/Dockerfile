FROM python:3.9-slim

WORKDIR /app
COPY . /app

RUN apt-get update && \
    apt-get install -y build-essential libpq-dev && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["python", "scraper.py"]

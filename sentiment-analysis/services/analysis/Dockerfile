FROM python:3.9-slim

WORKDIR /app
COPY . /app

RUN apt-get update && \
    apt-get install -y build-essential && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["python", "sentiment_analysis.py"]

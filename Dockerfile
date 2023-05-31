FROM python:3.9-slim-buster

WORKDIR /app

COPY config.toml .
COPY main.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV INPUT_RELAY=wss://relay.nostr.band
ENV OUTPUT_RELAY=ws://localhost:9944
ENV KINDS=[0,1]

ENTRYPOINT [ "python", "-u", "./main.py" ]
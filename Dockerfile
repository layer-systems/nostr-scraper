FROM python:3.9-slim-buster

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV INPUT_RELAY=wss://relay.nostr.band
ENV OUTPUT_RELAY=ws://localhost:9944

ENTRYPOINT [ "python", "-u", "./main.py" ]
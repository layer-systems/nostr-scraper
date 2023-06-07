FROM python:3.12.0b1

WORKDIR /app

COPY main.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV DB_USER=nostr
ENV DB_PASSWORD=justasimplepassword
ENV DB_HOST=postgres
ENV DB_PORT=5432
ENV DB_DATABASE=nostr
ENV DEBUG=False

ENTRYPOINT [ "python", "-u", "./main.py" ]
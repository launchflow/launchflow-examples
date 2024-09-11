FROM python:3.11-slim

WORKDIR /code

RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -U pip setuptools wheel && pip install --no-cache-dir launchflow[gcp] flask gunicorn

COPY ./main.py /code/main.py
COPY ./infra.py /code/infra.py

ENV PORT=80
EXPOSE $PORT

CMD gunicorn  main:app -b 0.0.0.0:$PORT

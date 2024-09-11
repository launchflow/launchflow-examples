FROM python:3.11-slim

WORKDIR /code

RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -U pip setuptools wheel && pip install --no-cache-dir launchflow[gcp] django

COPY . /code/

ENV PORT=8080
EXPOSE $PORT

CMD python manage.py runserver 0.0.0.0:$PORT

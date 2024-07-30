# TODO(developer): Change the base image to match your Python version
FROM python:3.11-slim

WORKDIR /code

# Install common dependencies since we are using a slim image
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies defined in requirements.txt
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -U pip setuptools wheel && pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY ./app /code/app

# Expose the port for the Flask app 
ENV PORT=8080
EXPOSE $PORT

# Run the Flask app using Gunicorn
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app.main:app

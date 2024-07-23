# TODO(developer): Change the base image to match your Python version
FROM python:3.11-slim

WORKDIR /code

# Install common dependencies since we are using a slim image
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && apt-get clean && rm -rf /var/lib/apt/lists/*
# Install the required Python packages defined in the requirements.txt file
COPY requirements.txt .
RUN pip install --no-cache-dir -U pip setuptools wheel && pip install -r requirements.txt

# Copy the application code to the image
COPY ./app /code/app
# Set the environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

# Expose the port that the app runs on
EXPOSE $PORT

# Run the web service on container startup
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT

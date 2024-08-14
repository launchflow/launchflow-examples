# TODO(developer): Change the base image to match your Python version
FROM public.ecr.aws/docker/library/python:3.11-slim

WORKDIR /code

# Install common dependencies since we are using a slim image
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies defined in requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -U pip setuptools wheel && pip install -r requirements.txt

# Copy the application code to the image
COPY ./main.py /code/main.py

# Expose the port for the FastAPI app 
ENV PORT=80
EXPOSE $PORT

# Run the FastAPI app using Uvicorn
CMD uvicorn main:app --host 0.0.0.0 --port $PORT

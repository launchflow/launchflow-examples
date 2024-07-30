# TODO(developer): Change the base image to match your Python version
FROM public.ecr.aws/docker/library/python:3.11-slim

WORKDIR /code

# Install common dependencies since we are using a slim image
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python dependencies defined in requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -U pip setuptools wheel && pip install -r requirements.txt


# Copy the application code to the image
COPY ./manage.py /code/manage.py
COPY ./app /code/app
COPY ./django_backend /code/django_backend

# Expose the port for the Django app 
ENV PORT=80
EXPOSE $PORT

# Run the Django app using Gunicorn
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 django_backend.wsgi:application

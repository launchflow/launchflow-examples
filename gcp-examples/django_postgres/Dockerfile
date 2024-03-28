# NOTE: This Dockerfile uses multi-stage builds for efficient caching and smaller image sizes
# Learn more at https://docs.docker.com/build/building/multi-stage/

# Build Stage 1: Build stage for installing dependencies
FROM python:3.11-slim as builder

# Set a working directory for the build stage
WORKDIR /build

# Install system dependencies required for Python packages to build
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -U pip setuptools wheel \
    && pip install --no-cache-dir --target=/install -r requirements.txt

# Build Stage 2: Build a final slim image for running the application
FROM python:3.11-slim

# Create a non-root user for security purposes
RUN useradd --create-home appuser
USER appuser

# Set environment variables for Python to run in unbuffered mode and not write .pyc files
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8080

# Copy installed dependencies from the builder stage
COPY --from=builder /install /usr/local/lib/python3.11/site-packages
ENV PATH="${PATH}:/usr/local/lib/python3.11/site-packages/bin"

# Set the working directory and copy only the necessary application files
WORKDIR /code
COPY --chown=appuser:appuser ./manage.py /code/manage.py
COPY --chown=appuser:appuser ./app /code/app
COPY --chown=appuser:appuser ./django_postgres /code/django_postgres
COPY --chown=appuser:appuser ./launchflow.yaml /code/launchflow.yaml

# Expose the port the app runs on
EXPOSE $PORT

# Start the application
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 django_postgres.wsgi:application

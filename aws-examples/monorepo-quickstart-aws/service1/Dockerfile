# Use multi-stage builds for efficient caching and minimal final image size
# Stage 1: Build stage for installing dependencies
FROM public.ecr.aws/docker/library/python:3.11-slim as builder

# Set a working directory for the build stage
WORKDIR /build

# Install system dependencies required for Python packages to build
RUN apt-get update     && apt-get install -y --no-install-recommends gcc libpq-dev     && apt-get clean     && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install dependencies
COPY service1/requirements.txt .
RUN pip install --no-cache-dir -U pip setuptools wheel     && pip install --no-cache-dir --target=/install -r requirements.txt

# Stage 2: Final slim image for running the application
FROM public.ecr.aws/docker/library/python:3.11-slim

# Create a non-root user for security purposes
RUN useradd --create-home appuser
USER appuser

# Set environment variables for Python to run in unbuffered mode and not write .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8080 


# Copy installed dependencies from the builder stage
COPY --from=builder /install /usr/local/lib/python3.11/site-packages
ENV PATH="${PATH}:/usr/local/lib/python3.11/site-packages/bin"

# Set the working directory and copy only the necessary application files
WORKDIR /code
COPY --chown=appuser:appuser ./service1/app /code/app
COPY --chown=appuser:appuser ./launchflow.yaml /code/launchflow.yaml

# Expose the port the app runs on
EXPOSE $PORT

# Start the Uvicorn server
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT

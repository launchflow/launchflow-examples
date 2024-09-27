#!/bin/bash

# Define S3 bucket and model file
LOCAL_MODAL_PATH="/models/llama.gguf"
REMOTE_MODEL_FILE_NAME="meta-llama-8b-instruct-q4_K_M.gguf"



if [ "${LAUNCHFLOW_ENVIRONMENT}" = "lf-llama-aws" ]; then
    bucket_url="s3://launchflow-llama-demo"
    echo "Downloading model from ${S3_BUCKET_URL}/${MODEL_FILENAME}..."
    aws s3 cp ${bucket_url}/${REMOTE_MODEL_FILE_NAME} $LOCAL_MODAL_PATH
elif [ "${LAUNCHFLOW_ENVIRONMENT}" = "lf-llama-gcp" ]; then
    bucket_url="gs://launchflow-llama-demo"
    echo "Downloading model from ${bucket_url}/${REMOTE_MODEL_FILE_NAME}..."
    gsutil cp ${bucket_url}/${REMOTE_MODEL_FILE_NAME} $LOCAL_MODAL_PATH
fi

# Start the server with the downloaded model

cd llama.cpp
./llama-server --model $LOCAL_MODAL_PATH --ctx-size 5000 --port 80 --host 0.0.0.0

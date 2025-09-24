#!/bin/bash

# -----------------------------
# SEA-SEQ Docker Quick Start
# -----------------------------

# Optional: Default target site
TARGET_SITE_URL_DEFAULT="https://mlbam-park.b12sites.com/"

# Use existing environment variable or default
TARGET_SITE_URL="${TARGET_SITE_URL:-$TARGET_SITE_URL_DEFAULT}"

# Image and container naming
IMAGE_NAME="sea-seq-api"
CONTAINER_NAME="sea-seq-container"

# Step 1: Build the Docker image
echo "🔧 Building Docker image: $IMAGE_NAME"
docker build -t $IMAGE_NAME .

# Step 2: Run the container
echo "🚀 Running SEA-SEQ API in Docker container: $CONTAINER_NAME"
docker run --rm -it \
  -e TARGET_SITE_URL="$TARGET_SITE_URL" \
  -p 8000:8000 \
  --name $CONTAINER_NAME \
  $IMAGE_NAME \
  uvicorn app:app --reload --host 0.0.0.0 --port 8000
	

#!/bin/bash

CONTAINER_NAME="sea-seq-api"
IMAGE_NAME="sea-seq-api"
HOST_PORT=8080
CONTAINER_PORT=8000

echo "🔍 Checking for existing container named $CONTAINER_NAME..."
if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
    echo "🛑 Stopping existing container..."
    docker stop $CONTAINER_NAME > /dev/null
    echo "🧼 Removing existing container..."
    docker rm $CONTAINER_NAME > /dev/null
else
    echo "✅ No existing container found."
fi

echo "🐳 Building Docker image ($IMAGE_NAME)..."
docker build -t $IMAGE_NAME .

echo "🚀 Running container $CONTAINER_NAME on port $HOST_PORT..."
docker run -d --name $CONTAINER_NAME -p $HOST_PORT:$CONTAINER_PORT $IMAGE_NAME

echo "🌐 API is now running at: http://localhost:$HOST_PORT"
echo "📜 Container logs:"
docker logs -f $CONTAINER_NAME


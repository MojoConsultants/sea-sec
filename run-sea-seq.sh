```bash
#!/bin/bash
set -e

echo "🔄 Building SEA-SEC Docker image..."
docker compose build

echo "🚀 Starting SEA-SEC container..."
docker compose up

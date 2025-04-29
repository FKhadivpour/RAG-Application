#!/bin/bash

echo "Setting up RAG Knowledge Assistant environment..."

# Create necessary directories
mkdir -p data/raw
mkdir -p data/processed
mkdir -p data/vector_store

# Optionally create a .env if it doesn't exist
if [ ! -f .env ]; then
  echo "No .env file found. Copying .env.example to .env"
  cp .env.example .env
else
  echo ".env file already exists."
fi

echo "Setup complete. ✅"

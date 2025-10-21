#!/bin/bash
# Build script for Render

# Exit on error
set -e

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🌱 Running database seed..."
python -m scripts.seed_cevicheria_data

echo "✅ Build completed successfully!"

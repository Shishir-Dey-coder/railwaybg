#!/bin/bash

# Start build
echo "Starting build..."

# Install Python dependencies
echo "Installing Python dependencies..."
python3.9 -m pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python3.9 manage.py collectstatic --noinput --clear

# End build
echo "Build complete."

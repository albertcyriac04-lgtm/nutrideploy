#!/bin/bash

echo "BUILD START"

# Install dependencies
python3.12 -m pip install -r requirements.txt --break-system-packages

# Run migrations (optional during build, usually better to run in post-deployment)
# python3.12 manage.py migrate --noinput

# Collect static files
python3.12 manage.py collectstatic --noinput

echo "BUILD END"

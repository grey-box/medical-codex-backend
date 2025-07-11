#!/bin/bash
set -e

# Activate the virtual environment
source /home/site/wwwroot/env/bin/activate

# Install dependencies
pip install -r /home/site/wwwroot/requirements.txt

# Start the FastAPI application using Gunicorn
exec gunicorn main:app --bind 0.0.0.0:8000 --workers 4 --worker-class uvicorn.workers.UvicornWorker

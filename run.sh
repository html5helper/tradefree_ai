#!/bin/bash

# Activate virtual environment
source .venv/bin/activate

# Add current directory to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Start Celery worker
celery -A ai.tasks worker --loglevel=info 
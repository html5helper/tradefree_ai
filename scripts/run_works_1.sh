#!/bin/bash

# Set the project root directory
PROJECT_ROOT="/Users/marvin/Documents/tradefree/projects/tradefree_ai"

# Add the project root to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$PROJECT_ROOT

# Run the workflow workers
celery -A ai.core.event_broker.app worker \
  --queues social2product_total_tasks \
  --concurrency 1 \
  --loglevel info

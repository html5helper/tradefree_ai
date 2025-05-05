#!/bin/bash

# Set the project root directory
PROJECT_ROOT="/Users/marvin/Documents/tradefree/projects/tradefree_ai"

# Add the project root to PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$PROJECT_ROOT

# Run the workflow
python3 $PROJECT_ROOT/ai/business/social2product/run_workflow.py 
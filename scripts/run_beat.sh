#!/bin/bash

export PYTHONPATH=$(pwd)

# 启动周期性执行的任务
celery -A ai.core.celery_app beat --loglevel=info
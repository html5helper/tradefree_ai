#!/bin/bash
set -a
source /home/qinbinbin/ai_tools/web_server/.env
set +a

cd /home/qinbinbin/ai_tools/web_server
/home/qinbinbin/anaconda3/envs/py3/bin/gunicorn \
    -w 1 \
    -b 0.0.0.0:8080 \
    --log-level error \
    --access-logfile - \
    --error-logfile - \
    main:app
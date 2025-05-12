#!/bin/bash
cd /Users/qinbinbin/PycharmProjects/tradefree_ai/dify/backup/bbq/api_server
/usr/local/bin/gunicorn -w 4 -b 0.0.0.0:8080 main:app
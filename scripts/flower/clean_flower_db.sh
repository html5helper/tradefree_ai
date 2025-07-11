#!/usr/bin/env bash
# clean_flower_db.sh - 清理 Flower 30天前的历史任务数据

DB_PATH="$(dirname "$(dirname "$(dirname "${BASH_SOURCE[0]}")")")/data/flower/flower.db"

if [ ! -f "$DB_PATH" ]; then
  echo "[ERROR] Flower DB 文件不存在: $DB_PATH"
  exit 1
fi

echo "Start cleaning Flower DB: $DB_PATH"

sqlite3 "$DB_PATH" <<EOF
DELETE FROM task WHERE timestamp < datetime('now', '-30 days');
VACUUM;
EOF

echo "Flower DB clean done. 仅保留30天内数据。" 
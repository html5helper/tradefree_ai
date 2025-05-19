#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

usage() {
    cat <<EOF
Usage: $0 <process_name>
Example: $0 "uvicorn ai.core.celery_api:api"
EOF
    exit 1
}

if [[ $# -ne 1 ]]; then
    usage
fi

PROCESS_NAME="$1"

# 查找所有匹配的 PID，pgrep 每行输出一个 PID
# 如果 pgrep 返回非零，则用 || true 保证脚本不中断
PIDS=( $(pgrep -f -- "${PROCESS_NAME}" || true) )

if [[ ${#PIDS[@]} -eq 0 ]]; then
    echo "❌ No process found matching: ${PROCESS_NAME}"
    exit 1
fi

echo "🔍 Found process IDs: ${PIDS[*]}"

# 先尝试正常终止
echo "⚙️  Sending SIGTERM to: ${PIDS[*]}"
if kill "${PIDS[@]}"; then
    echo "⏳ Waiting for processes to exit..."
    sleep 3
else
    echo "⚠️  Failed to send SIGTERM, will try SIGKILL shortly."
fi

# 检查是否仍有存活
ALIVE=( $(pgrep -f -- "${PROCESS_NAME}" || true) )

if [[ ${#ALIVE[@]} -gt 0 ]]; then
    echo "🚨 Processes still alive: ${ALIVE[*]}"
    echo "🔪 Sending SIGKILL to: ${ALIVE[*]}"
    kill -9 "${ALIVE[@]}"
    sleep 1
    # 最后确认
    if pgrep -f -- "${PROCESS_NAME}" > /dev/null; then
        echo "❌ Failed to kill: ${PROCESS_NAME}"
        exit 1
    else
        echo "✅ Processes killed with SIGKILL."
    fi
else
    echo "✅ Processes exited cleanly."
fi
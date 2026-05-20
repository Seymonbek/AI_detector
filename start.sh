#!/usr/bin/env bash

set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

PORT="${PORT:-5000}"
VIDEO_SOURCE_VALUE="${1:-${VIDEO_SOURCE:-test_video.mp4}}"
SERVER_URL_VALUE="${SERVER_URL:-http://127.0.0.1:${PORT}/api/alert}"

if ! command -v python3 >/dev/null 2>&1; then
    echo "python3 topilmadi. Iltimos, Python 3 o'rnating."
    exit 1
fi

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source .venv/bin/activate

python3 -m pip install --upgrade pip >/dev/null
python3 -m pip install -r requirements.txt

mkdir -p static/images

cleanup() {
    if [ -n "${SERVER_PID:-}" ] && kill -0 "$SERVER_PID" 2>/dev/null; then
        kill "$SERVER_PID" 2>/dev/null || true
        wait "$SERVER_PID" 2>/dev/null || true
    fi
}

trap cleanup EXIT INT TERM

echo "Local server ishga tushmoqda..."
python3 -m uvicorn server:app --host 0.0.0.0 --port "$PORT" &
SERVER_PID=$!

sleep 3

echo "Dashboard: http://127.0.0.1:${PORT}"
echo "Docs: http://127.0.0.1:${PORT}/docs"
echo "Video source: ${VIDEO_SOURCE_VALUE}"
echo "To'xtatish uchun OpenCV oynasida q bosing yoki terminalda Ctrl + C bosing."

VIDEO_SOURCE="$VIDEO_SOURCE_VALUE" SERVER_URL="$SERVER_URL_VALUE" python3 detector.py

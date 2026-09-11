#!/bin/bash
# JOB 1 daily runner. Installed in crontab 2026-09-08.
cd "/Users/kwu/cprt" || exit 3
mkdir -p logs
TS=$(date -u +%Y%m%dT%H%M%SZ)
{
  echo "=== Job1 run $TS ==="
  "/Users/kwu/cprt/.venv/bin/python" "/Users/kwu/cprt/scripts/job1_snapshot.py"
  echo "exit=$?"
} >> "/Users/kwu/cprt/logs/job1_cron.log" 2>&1

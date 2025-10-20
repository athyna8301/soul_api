#!/usr/bin/env bash
set -e

echo "=== Current directory ==="
pwd
ls -la

echo "=== requirements.txt contents ==="
cat requirements.txt

echo "=== Upgrading pip ==="
.venv/bin/pip install --upgrade pip

echo "=== Installing requirements ==="
.venv/bin/pip install -r requirements.txt

echo "=== Installed packages ==="
.venv/bin/pip list

echo "=== Build complete ==="

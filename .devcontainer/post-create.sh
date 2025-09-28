#!/usr/bin/env bash
set -euo pipefail

cd /workspace/somint
echo "[post-create] Python: $(python --version)"
echo "[post-create] Poetry:  $(poetry --version)"
echo "[post-create] Moving to engine directory..."
cd engine

echo "[post-create] Checking for pyproject.toml..."
if [ ! -f "pyproject.toml" ]; then 
  echo "[post-create] No pyproject.toml found. Creating one and installing dependencies..."
  poetry init -n && poetry add opencv-python-headless numpy matplotlib scikit-image pydantic fastapi uvicorn
  echo "[post-create] pyproject.toml created and dependencies added."
fi

echo "[post-create] Configuring Poetry..."
bash -lc set -e # Ensure the shell is login to pick up environment variables
echo "[post-create] Virtual environments will be created."
poetry config virtualenvs.create true
echo "[post-create] Virtual environments will be created inside the project."
poetry config virtualenvs.in-project true
echo "[post-create] Installing dependencies..."
poetry install --no-interaction --no-ansi || true
echo "[post-create] Dependencies installed successfully."

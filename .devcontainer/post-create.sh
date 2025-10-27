#!/usr/bin/env bash
set -euo pipefail

cd /workspaces/somint/engine

# Force Poetry to create venvs in the project directory
export POETRY_VIRTUALENVS_CREATE=1
export POETRY_VIRTUALENVS_IN_PROJECT=1
# As an extra belt-and-suspenders, set an explicit path under the project
export POETRY_VIRTUALENVS_PATH="$PWD/.venvs"
# Keep caches writable inside the workspace
export POETRY_CACHE_DIR="$PWD/.cache/pypoetry"

echo "[post-create] Python:  $(python3 --version || true)"
echo "[post-create] Poetry:   $(poetry --version || true)"

# Configure Poetry locally
poetry config virtualenvs.create true --local
poetry config virtualenvs.in-project true --local
poetry config virtualenvs.path "$POETRY_VIRTUALENVS_PATH" --local

# Ensure we’re using the container’s python
poetry env use python3

# Initialize project if needed
if [ ! -f "pyproject.toml" ]; then
  echo "[post-create] No pyproject.toml found. Initializing…"
  poetry init -n
  echo "[post-create] Adding baseline dependencies…"
  poetry add opencv-python-headless "numpy<2" matplotlib scikit-image pydantic fastapi uvicorn
fi

echo "[post-create] Installing dependencies…"
poetry install --no-interaction --no-ansi

echo "[post-create] Verifying environment…"
poetry env info
poetry run python - <<'PY'
import sys, site
print("python:", sys.executable)
print("prefix:", sys.prefix)
print("site-packages:", site.getsitepackages())
if any(p.startswith("/usr/local") for p in site.getsitepackages()):
    raise SystemExit("ERROR: Using /usr/local site-packages; venv not active.")
PY

echo "[post-create] Done."

# Somint

AI-powered trading-card grading and analysis platform focused on computer vision pipelines for trading-card grading.

## Repository Layout
- `engine/` – Active Python 3.13 engine managed by Poetry; includes configs and data staging folders.
- `client/` – Holds forthcoming UI work. Currently empty.
- `server/` – Reserved for orchestration services that wrap the engine.
- `.devcontainer/` – VS Code Dev Container definition with Poetry preconfigured for in-project virtualenvs.

## Quick Start
### Dev Container (recommended)
1. Open the repository in VS Code.
2. Run **Dev Containers: Reopen in Container**.
3. The post-create script installs Poetry dependencies and exposes the app on port 8000.

### Local Setup
Ensure Python 3.13 and Poetry are available, then run:
```bash
cd engine
poetry install           # create in-project venv and install deps
poetry shell             # activate the environment
```
If you prefer not to spawn a shell, prefix commands with `poetry run`.

## Running the Engine
Populate `engine/data/raw` with input assets, then start your FastAPI entrypoint:
```bash
cd engine
poetry run uvicorn <module>:app --reload
```
Replace `<module>` with the module that exposes your `FastAPI` instance (for example `somint.api`).

## Testing
Add tests under `engine/tests/` and execute them before pushing:
```bash
cd engine
poetry run pytest --maxfail=1
```

## Additional Resources
- Contributor guide: [Repository Guidelines](AGENTS.md)
- Dev environment variables and cache paths are documented in `.devcontainer/post-create.sh`.

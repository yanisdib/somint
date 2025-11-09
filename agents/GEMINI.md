# Project Overview

This repository contains `somint`, an AI-powered trading-card grading and analysis platform. The project is structured as a monorepo with three main components:

*   **`engine/`**: A Python-based computer vision engine for grading trading cards. It uses FastAPI to expose its functionality as a web service.
*   **`client/`**: A placeholder for the user interface of the platform.
*   **`server/`**: A placeholder for orchestration services that will wrap the engine.

The core of the project is the `engine`, which uses a combination of `opencv-python-headless`, `numpy`, and `scikit-image` for image processing and analysis. The web service is built with `fastapi` and `uvicorn`.

# Building and Running

The recommended way to work on this project is by using the provided Dev Container, which sets up a consistent development environment.

## Dev Container (Recommended)

1.  Open the repository in VS Code.
2.  Run **Dev Containers: Reopen in Container**.
3.  The post-create script will automatically install all the necessary dependencies.

## Local Setup

If you prefer to set up the project locally, you will need Python 3.13 and Poetry.

1.  Navigate to the `engine` directory:
    ```bash
    cd engine
    ```
2.  Install the dependencies:
    ```bash
    poetry install
    ```
3.  Activate the virtual environment:
    ```bash
    poetry shell
    ```

## Running the Engine

To run the `engine`, first make sure you have populated the `engine/data/raw` directory with the images you want to grade. Then, run the following command from the `engine` directory:

```bash
poetry run uvicorn main:app --reload
```

This will start the FastAPI server on `http://localhost:8000`.

# Testing

Tests are located in the `engine/tests/` directory. To run the tests, execute the following command from the `engine` directory:

```bash
poetry run pytest --maxfail=1
```

# Development Conventions

*   **Python:** The `engine` uses Python 3.13 and follows the Black code style.
*   **Dependencies:** Dependencies are managed with Poetry.
*   **Virtual Environments:** The project is configured to create virtual environments within the `engine` directory.
*   **Dev Container:** A Dev Container is provided for a consistent development experience.

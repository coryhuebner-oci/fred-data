# fred-data

A project used to better understand and integrate with the Federal Reserve Economic Data (FRED) datasets.

## Prerequisites
Before beginning, you'll need the following on your machine
- Python (3.11.1 or greater)

## Local environment setup
To setup your local environment, run the following:
1. Initialize a virtual environment: `python -m venv .venv --copies`, The `--copies` value is used to ensure the Python binary is accessible
even when run as a container.
2. Activate that environment: `. .venv/bin/activate`
3. Install this project and its dependencies: `pip install -e .`
4. Install development dependencies: `pip install '.[dev]'`
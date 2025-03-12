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

## Using the Jupyter Notebook
Probably the most interesting entry-point is the [exploration notebook](./notebooks/exploration.ipynb). This is where learning about
how to consume the FRED API is being done. If you go to that notebook, you can:
1. Run through the setup cells at the top of the notebook. These steps are all in the "Setup" section of the notebook
2. After running through those cells, you can hit the FRED API in any of the cells in the "Data Exploration" section of the
notebook
3. Most of the data exploration cells output a summary of information. Then using the Data Wrangler VS Code plugin (or some other DataFrame
inspector), you can dive into underlying data for each dataset pulled
# kanon-api

<a href="https://codecov.io/gh/legau/kanon-api/branch/master"> <img src="https://codecov.io/gh/legau/kanon-api/branch/master/graph/badge.svg"></a>
<a href="https://github.com/legau/kanon-api/actions"> <img src="https://github.com/legau/kanon-api/workflows/CI/badge.svg"></a>
<a href="https://www.python.org/downloads/release/python-392/"> <img src="https://shields.io/badge/python-v3.10-blue"></a>
<a href="https://pypi.org/project/kanon/"> <img src="https://img.shields.io/pypi/v/kanon?color=blue&label=kanon&logoColor=white"></a>

Kanon features exposed through an API.

## Set up

1. Install dependencies with `poetry` ([Installing Poetry](https://python-poetry.org/docs/))

```bash
# if pre-commit is not already installed
sudo apt install pre-commit

git clone git@github.com:legau/kanon-api.git
cd kanon-api
poetry install
```

The changes you make in the code are reflected on your Python environment. Working with Python 3.10.

2. Activate pre-commit checks:

```bash
# if pre-commit is not already installed
sudo apt install pre-commit

pre-commit install
```

## Run tests

```bash
poetry run pytest --cov=kanon_api
```

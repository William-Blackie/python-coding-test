install:
		poetry install --no-root

dev:
	  poetry run fastapi dev src/main.py

test:
	  poetry run python -m unittest discover src.tests

.PHONY: install dev

run:
	poetry run python parsero

install:
	poetry install

format:
	poetry run black .
	poetry run isort .

test:
	poetry run pytest


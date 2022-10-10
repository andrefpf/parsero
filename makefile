run:
	python3 -m poetry run python parsero

install:
	python3 -m poetry install

format:
	python3 -m poetry run black .
	python3 -m poetry run isort .

test:
	python3 -m poetry run pytest


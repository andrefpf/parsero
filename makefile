format:
	poetry run black .
	poetry run isort .

test:
	poetry run pytest
.PHONY: 
makemigrations:
	(cd app && poetry run piccolo migrations new app_db --auto)

migrate:
	(cd app && poetry run piccolo migrations forwards all)

createuser:
	(cd app && poetry run piccolo user create)

createsuperuser:
	(cd app && poetry run piccolo user create --username=aadmin --password=aadmin --email=admin@gmail.com --is_admin=true --is_superuser=true --is_active=true)

dev_start:
	poetry run python -m app

env_setup:
	pip install poetry
	poetry install
	echo "installed environment! Use poetry shell to enter environment. Create a new .env"

pycheck:
	poetry run black app
	poetry run ruff check app tests --fix
	poetry run mypy app

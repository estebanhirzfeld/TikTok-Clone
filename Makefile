build:
	docker compose -f local.yml up --build -d --remove-orphans

up:
	docker compose -f local.yml up -d

down:
	docker compose -f local.yml down

show-logs:
	docker compose -f local.yml logs

show-logs-django:
	docker compose -f local.yml logs django

makemigrations:
	docker compose -f local.yml run --rm django python manage.py makemigrations

migrate:
	docker compose -f local.yml run --rm django python manage.py migrate

collectstatic:
	docker compose -f local.yml run --rm django python manage.py collectstatic --no-input --clear

superuser:
	docker compose -f local.yml run --rm django python manage.py createsuperuser

down-v:
	docker compose -f local.yml down -v

volume:
	docker volume inspect src_local_postgres_data

# TODO: Change "Core"
tiktok-clone-db:
	docker compose -f local.yml exec postgres psql --username=postgres_user --dbname=tiktok-clone-db

flake8:
	docker compose -f local.yml exec django flake8 .

black-check:
	docker compose -f local.yml exec django black --check --exclude=migrations .

black-diff:
	docker compose -f local.yml exec django black --diff --exclude=migrations .

black:
	docker compose -f local.yml exec django black --exclude=migrations .

isort-check:
	docker compose -f local.yml exec django isort . --check-only --skip venv --skip migrations

isort-diff:
	docker compose -f local.yml exec django isort . --diff --skip venv --skip migrations

isort:
	docker compose -f local.yml exec django isort . --skip venv --skip migrations


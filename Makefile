# =========================
# Project configuration
# =========================
PROJECT_NAME=django-app
SERVICE=app
COMPOSE=docker compose

DJANGO_MANAGE=python manage.py

.DEFAULT_GOAL := help

# =========================
# Help
# =========================
help:
	@echo ""
	@echo "Available commands:"
	@echo "  make build            Build docker images"
	@echo "  make up               Start containers"
	@echo "  make down             Stop containers"
	@echo "  make restart          Restart containers"
	@echo "  make logs             Tail logs"
	@echo ""
	@echo "  make migrate          Run Django migrations"
	@echo "  make makemigrations   Create new migrations"
	@echo "  make superuser        Create Django superuser"
	@echo "  make collectstatic    Collect static files"
	@echo ""
	@echo "  make shell            Django shell"
	@echo "  make bash             Container bash"
	@echo ""
	@echo "  make test             Run tests"
	@echo "  make lint             Run flake8"
	@echo "  make format           Run autopep8 + isort"
	@echo ""

# =========================
# Docker lifecycle
# =========================
build:
	$(COMPOSE) build

up:
	$(COMPOSE) up -d

down:
	$(COMPOSE) down

restart:
	$(COMPOSE) down
	$(COMPOSE) up -d

logs:
	$(COMPOSE) logs -f

ps:
	$(COMPOSE) ps

# =========================
# Django commands
# =========================
migrate:
	$(COMPOSE) exec $(SERVICE) $(DJANGO_MANAGE) migrate

makemigrations:
	$(COMPOSE) exec $(SERVICE) $(DJANGO_MANAGE) makemigrations

superuser:
	$(COMPOSE) exec $(SERVICE) $(DJANGO_MANAGE) createsuperuser

collectstatic:
	$(COMPOSE) exec $(SERVICE) $(DJANGO_MANAGE) collectstatic --noinput

shell:
	$(COMPOSE) exec $(SERVICE) $(DJANGO_MANAGE) shell

# =========================
# Container access
# =========================
bash:
	$(COMPOSE) exec $(SERVICE) bash

# =========================
# Quality / CI helpers
# =========================
test:
	$(COMPOSE) exec $(SERVICE) pytest

lint:
	$(COMPOSE) exec $(SERVICE) flake8 .

format:
	$(COMPOSE) exec $(SERVICE) autopep8 --in-place --recursive .
	$(COMPOSE) exec $(SERVICE) isort .

# =========================
# Cleanup
# =========================
clean:
	$(COMPOSE) down -v
	docker system prune -f

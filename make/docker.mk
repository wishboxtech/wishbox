.PHONY: up dev down logs status restart infra docker-test docker-shell docker-superuser
up: setup ## Build and start the complete stack at http://localhost:8080
	$(COMPOSE) up -d --build --wait --wait-timeout 180
	@echo 'Wishy is ready at http://localhost:8080 (see .env.local for custom ports).'

dev: setup ## Start full stack with React/Django hot reload on port 8080
	$(DEV_COMPOSE) up -d --build --wait --wait-timeout 180

down: setup ## Stop containers, preserving database and uploads
	$(COMPOSE) down --remove-orphans

logs: setup ## Follow container logs
	$(COMPOSE) logs -f --tail=100

status: setup ## Show service status and published ports
	$(COMPOSE) ps

restart: setup ## Restart running services
	$(COMPOSE) restart

infra: setup ## Start only PostgreSQL and Redis for local development
	$(COMPOSE) up -d --wait postgres redis

docker-test: setup ## Run architecture/unit/API checks in Docker with PostgreSQL
	$(COMPOSE) exec back python scripts/check_architecture.py
	$(COMPOSE) exec back python -m unittest discover -s tests/unit -v
	$(COMPOSE) exec -e STAGE=ci -e WISHBOX_TEST_DB=postgres back python manage.py test src.apps src.api --noinput

docker-shell: setup ## Open the backend container shell
	$(COMPOSE) exec back sh

docker-superuser: setup ## Create an admin account in the backend container
	$(COMPOSE) exec back python manage.py createsuperuser

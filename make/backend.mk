.PHONY: backend-install backend-run migrate superuser architecture unit-test api-test postgres-test gift-maintenance gift-worker
backend-install: setup ## Install Python dependencies into .venv
	@test -x $(PY) || $(PYTHON) -m venv $(VENV)
	$(PY) -m pip install -r $(BACKEND)requirements/all.txt

backend-run: setup ## Run local Django (start dependencies with make infra)
	cd $(BACKEND) && $(PY) scripts/run_backend.py

migrate: setup ## Apply database migrations locally
	cd $(BACKEND) && STAGE=local $(PY) manage.py migrate --noinput

superuser: setup ## Create a Django admin account locally
	cd $(BACKEND) && STAGE=local $(PY) manage.py createsuperuser

architecture: ## Validate architecture boundaries
	cd $(BACKEND) && $(PY) scripts/check_architecture.py

unit-test: ## Run framework-independent unit tests
	cd $(BACKEND) && $(PY) -m unittest discover -s tests/unit -v

api-test: ## Run Django tests with isolated SQLite/cache
	cd $(BACKEND) && STAGE=ci $(PY) manage.py test src.apps src.api --noinput

postgres-test: setup ## Run Django tests against local PostgreSQL
	cd $(BACKEND) && STAGE=ci WISHBOX_TEST_DB=postgres $(PY) scripts/test_postgres.py

gift-maintenance: setup ## Release expired gift holds and send due in-app reminders once
	cd $(BACKEND) && STAGE=local $(PY) manage.py maintain_gifts

gift-worker: setup ## Run gift reminders/expiry locally every minute (separate terminal)
	cd $(BACKEND) && STAGE=local $(PY) manage.py maintain_gifts --loop --interval 60

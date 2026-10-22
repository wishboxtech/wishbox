.DEFAULT_GOAL := help
ROOT := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))
BACKEND := $(ROOT)backend/
PYTHON ?= python3.14
VENV ?= $(ROOT).venv
PY := $(VENV)/bin/python
COMPOSE := docker compose --project-name wishbox --env-file $(ROOT).env.local -f $(ROOT)build/docker-compose.yaml
DEV_COMPOSE := $(COMPOSE) -f $(ROOT)build/docker-compose.dev.yaml

.PHONY: help setup check test
help: ## Show available commands
	@awk 'BEGIN {FS = ":.*## "; print "Wishbox development commands\n"} /^[a-zA-Z_-]+:.*## / {printf "  %-22s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Create .env.local without changing existing configuration
	@$(PYTHON) $(ROOT)scripts/setup_local.py

include $(ROOT)make/backend.mk
include $(ROOT)make/frontend.mk
include $(ROOT)make/docker.mk

check: architecture frontend-check ## Check architecture and TypeScript
test: unit-test api-test frontend-test ## Run backend and frontend tests locally

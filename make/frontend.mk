.PHONY: frontend-install frontend-run frontend-build frontend-check frontend-test
frontend-install: ## Install locked frontend dependencies (Node 22.12+)
	cd $(ROOT)frontend && npm ci

frontend-run: ## Run React with hot reload on port 5173
	cd $(ROOT)frontend && npm run dev

frontend-build: ## Type-check and build the React application
	cd $(ROOT)frontend && npm run build

frontend-check: ## Check frontend TypeScript
	cd $(ROOT)frontend && npm run check

frontend-test: ## Run API client and translation tests
	cd $(ROOT)frontend && npm test

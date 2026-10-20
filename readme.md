# Wishbox

An English/Persian React application and Django/DRF API for wishlists, wishes,
profiles, avatars, image uploads and gift reservation requests.

```text
wishbox/
  frontend/           Independent React + TypeScript application
    src/              Interface, translations and HTTP client
    package.json      Frontend dependencies and commands
    Dockerfile        Vite development and Nginx runtime images
  backend/            Independent Django/DRF application
    src/              Domains, services, repositories and API
    settings/         Django configuration
    requirements/     Python dependencies
    tests/            Framework-independent unit tests
    scripts/          Architecture checks and native backend runners
    templates/        Django templates
    openapi/          API documentation
    manage.py         Django CLI
    Dockerfile        Backend runtime image
  build/              Full-stack Docker Compose configuration
  make/               Backend, frontend and Docker Make targets
  docs/               Architecture and development guides
  scripts/            Repository setup helpers
  Makefile            Run and verify both applications together
```

## Run the complete application

```bash
make up
```

Open [Wishbox](http://localhost:8080). Local sign-in uses OTP `123456` and sends
no SMS. Save your profile before creating a wishlist. Choose English or Persian
from the header menu; Persian changes the page to RTL.

Use `make dev` for React/Django hot reload, `make down` to stop without deleting
data, and `make help` for all commands. The first run generates `.env.local` with
local signing keys. These are development settings, not a production deployment.
See the [full-stack guide](docs/full-stack.md) for configuration and limitations.

## Native development

Use Python 3.12 or 3.13 and Node 22.12+:

```bash
make backend-install frontend-install
make infra
make migrate
make backend-run        # Terminal 1
make frontend-run       # Terminal 2: http://localhost:5173
```

Each application owns its dependencies and Dockerfile. The repository-root
Makefile coordinates their execution. Python environment files `.env` and
`.env.test` belong to `backend/`; `.env.local` is the shared, ignored local stack
configuration at the repository root. An existing root `.venv` remains usable;
set `VENV` to use a different virtual environment.

## Verification

```bash
make check
make test
make frontend-build
make postgres-test      # Dedicated local PostgreSQL test database
make docker-test        # Backend checks in Docker, including PostgreSQL locking
```

Direct Django and Python test commands must run from `backend/`. Python module
paths (`src.apps`, `src.api`, `settings`) and existing HTTP routes are unchanged.
The frontend consumes the public API through a same-origin proxy.

Read [rule.md](rule.md), [the architecture map](docs/architecture.md),
[the development guide](docs/development.md) and [AGENTS.md](AGENTS.md) before
changing the application. Runtime dependencies are assembled exclusively in
`backend/src/core/composition.py`. Domains and services remain independent of
Django and concrete persistence implementations.

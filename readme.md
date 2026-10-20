# Wishbox

Django/DRF backend for profiles, avatars, media, wishlists and OTP authentication.

Business rules live in explicit domains and injected application services. Pydantic
DTOs carry data across boundaries; repositories own database/cache access. Runtime
dependencies are assembled in `src/core/composition.py`.

Read [rule.md](rule.md), [architecture](docs/architecture.md),
[development guide](docs/development.md) and [migration decisions](docs/decisions/0001-domain-boundaries.md)
before changing the application. Agent instructions are in [AGENTS.md](AGENTS.md).

```text
src/apps/<app>/domain/        entities, value objects and business policies
src/apps/<app>/dto/           explicit input/output data
src/apps/<app>/interfaces.py  contracts owned by the use case
src/apps/<app>/services/      framework-independent application logic
src/apps/<app>/repositories/  persistence and ORM mapping
src/apps/<app>/models/        Django schema
src/api/views/<group>/<endpoint>/
  view.py                    one APIView containing the route's HTTP methods
  serializer.py              endpoint input/output serializers
  __init__.py                view exports only
src/api/                     routes, shared serialization and error mapping
src/core/composition.py      dependency construction
src/shared/                  shared contracts and transaction binding
openapi/                     API documentation
```

## Development

Use Python 3.12 or 3.13 with the current pinned dependencies. The system Python
may be newer; select the interpreter explicitly when creating the environment.
Docker and CI currently use Python 3.13. See the development guide for setup troubleshooting.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements/all.txt
# Configure a local .env for PostgreSQL, Redis and other runtime settings.
STAGE=dev python manage.py migrate
STAGE=dev python manage.py runserver
```

## Verification

```bash
python scripts/check_architecture.py
python -m unittest discover -s tests/unit -v
STAGE=ci python manage.py test src.apps src.api --noinput
# PostgreSQL verification using dedicated test database credentials:
STAGE=ci WISHBOX_TEST_DB=postgres python manage.py test src.apps src.api --noinput
```

The inner-layer tests run without framework setup or a database. Django test settings
use SQLite and an in-memory cache by default. See the development guide for PostgreSQL
and external-integration verification. Deployment files live in `build/`.

Each API route has its own endpoint directory. For example, anonymous friend
creation lives in `src/api/views/wishlist/create_anonymous_friend/`, with the
view in `view.py` and its input/output serializers in `serializer.py`.
Documentation, docstrings and explanatory comments should be written in English.

# Development guide

Backend code paths in this document are relative to `backend/`. The independent
React application lives in `frontend/`. Run direct Python/Django commands from
`backend/`; root Make targets select the correct directory automatically.

Read [rule.md](../rule.md) and [architecture.md](architecture.md) first.

For the React interface and one-command Docker startup, see the
[full-stack guide](full-stack.md). Use `make up` for the complete application or
`make dev` for frontend/backend hot reload. `make help` lists all available targets.

## Adding a capability

1. Define the use case, actor, inputs/outputs and business errors.
2. Implement required entities, value objects or policies in the domain, independent of the ORM.
3. Define explicit InputDTOs and OutputDTOs. Preserve omitted fields for PATCH.
4. Define service contracts in `interfaces.py`. Repository outputs must be entities/DTOs,
   never lazy results.
5. Implement services with injected dependencies. Add transaction factories and
   after-commit capabilities to constructors when needed.
6. Test business behavior first with fake/mock contracts in `tests/unit`.
7. Implement concrete repositories and mappings, then wire them in the composition root.
8. Create `src/api/views/<group>/<endpoint>/` with `view.py`, `serializer.py` and
   `__init__.py`. Define input/output serializers in `serializer.py`. The view validates
   input, creates a DTO, invokes one use case and serializes the response. Keep all
   methods for a route in one APIView. URL configuration imports its `view.py` directly.
   Do not define serializers in `apps/` or views in `__init__.py`. Take actor/resource
   IDs from the authenticated user and URL, not from the body.
9. Update integration/API tests, routes and OpenAPI. Record new structural decisions in an ADR.
10. Write documentation, docstrings and explanatory comments in English.

## Calling a use case

```python
from src.apps.wishlist.dto import UpdateWishInputDTO
from src.core.composition import wishlist_service

dto = UpdateWishInputDTO(
    id=wish_id,
    wishlist_id=wishlist_id,
    profile_id=authenticated_user_id,
    name="New name",
)
result = wishlist_service().update_wish(dto)
```

This example belongs at the application execution boundary. Services must not
import `composition`; dependencies come from their constructors. Convert OutputDTOs
using the endpoint's output serializer in the API, not to dictionaries/JSON inside
business code. For example:

```python
# src/api/views/wishlist/get_wish_by_id/serializer.py
from src.api.serialization import DTOResponseSerializer


class WishOutputSerializer(DTOResponseSerializer):
    """Serialize this endpoint's wish output."""
```

```python
# src/api/views/wishlist/get_wish_by_id/view.py
from src.api.views.wishlist.get_wish_by_id.serializer import WishOutputSerializer

# Inside the endpoint handler, after invoking the use case:
data = WishOutputSerializer(result).data
```

Use `many=True` for lists. Errors, status codes, cookies and response envelopes
belong to the view. Serializers do not execute queries or business rules.

## Environment and tests

Use Python 3.12 or 3.13 with the current pinned dependencies. Docker and CI use
3.13, and the local project has been validated with 3.12. The system Python may
be 3.14; choose the interpreter explicitly when creating an environment.
Pydantic is already a dependency:

```bash
python3.12 -m venv ../.venv
source ../.venv/bin/activate
pip install -r requirements/all.txt
python scripts/check_architecture.py
python -m unittest discover -s tests/unit -v
STAGE=ci python manage.py test src.apps src.api --noinput
```

Unit tests do not need STAGE, `.env`, Django setup, PostgreSQL or Redis. Django
tests under `STAGE=ci` load defaults from `.env.test`, use SQLite, and use an
in-memory cache with the required Redis API. Test media defaults to
`/tmp/wishbox-test-media`; override it with `WISHBOX_TEST_MEDIA_ROOT`.
These settings are for tests only.

Run the same suite on PostgreSQL with:

```bash
STAGE=ci WISHBOX_TEST_DB=postgres python manage.py test src.apps src.api --noinput
```

Configure `DEFAULT_DATABASE_NAME/USER/PASSWORD/HOST/PORT` for a dedicated test
database. The database user needs permission to create test databases. The
in-memory test cache does not prove Redis/NATS network integration. Test those
integrations in a dedicated environment with development settings and suitable
delivery mocks.

Name new test files `test_*.py`. Re-export older tests with other names from the
test package's `__init__.py` so Django can discover them.

## Installing psycopg-binary

If installation reports `No matching distribution found for psycopg-binary==3.2.3`,
check `python --version` and the environment's `pyvenv.cfg`. This binary version
has no CPython 3.14 wheel, and Django 5.1 does not list Python 3.14 as supported.
References: [Psycopg 3.2.3 files](https://pypi.org/project/psycopg-binary/3.2.3/)
and [Django 5.1 compatibility](https://docs.djangoproject.com/en/5.1/faq/install/#what-python-version-can-i-use-with-django).

Create a fresh environment with a compatible interpreter. Installing Python 3.12
on the system does not change an existing virtual environment created with 3.14.
If the incompatible environment is `venv/`, you can keep it and activate a new
`.venv/`:

```bash
deactivate  # only if another virtual environment is active
python3.12 -m venv ../.venv
source ../.venv/bin/activate
python --version
python -m pip install -r requirements/all.txt
python -m pip check
```

For Python 3.13, create the environment with `python3.13 -m venv ../.venv`.
In VS Code, choose `${workspaceFolder}/.venv/bin/python` as the interpreter.
The `activate` file is a shell script, not an interpreter.

## Review checks

- Can services be imported and tested without frameworks?
- Are business rules also enforced for non-HTTP callers?
- Does PATCH preserve the distinction between omitted and null fields?
- Are rollback, missing records, unauthorized actors and resource-parent relationships tested?
- Do lists and media lookups use batch operations?
- Do HTTP contracts, errors and documentation match the implementation?

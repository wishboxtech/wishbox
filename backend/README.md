# Wishbox backend

This directory is the complete Django/DRF application: `src/`, `settings/`,
`requirements/`, migrations, tests, templates and OpenAPI definitions.
Python module names such as `src.apps.wishlist` remain unchanged.

Run the full application from the repository root with `make up`, or use
`make backend-install`, `make infra`, `make migrate` and `make backend-run` for
native development. The root Makefile selects this directory automatically.

When running Django or business checks directly, use this directory as the
working directory:

```bash
../.venv/bin/python scripts/check_architecture.py
../.venv/bin/python -m unittest discover -s tests/unit -v
STAGE=ci ../.venv/bin/python manage.py test src.apps src.api --noinput
```

Read [the architecture policy](../rule.md), [dependency map](../docs/architecture.md)
and [full-stack guide](../docs/full-stack.md) before changing application code.

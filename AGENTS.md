# Project development instructions

## Working directory

- For every Wishbox request, work directly in `/home/parsa/Desktop/wishbox`.
- Do not create, restore or develop in a worktree under `.codex` unless the user
  explicitly requests a worktree for that task.
- If a chat starts in a worktree, use the main project path as the working
  directory for all commands and file edits before beginning project work.

The repository has independent `frontend/` and `backend/` applications. Backend
paths below are relative to `backend/`. Run direct Python/Django commands from
`backend/`, or use root Make targets. Keep backend runtime dependencies and tests
inside `backend/` and frontend dependencies and code inside `frontend/`.

Read [rule.md](rule.md) before changing application code. It is the canonical
architecture policy. Read [docs/architecture.md](docs/architecture.md) for the
dependency map and [docs/development.md](docs/development.md) for the workflow.

- Keep domain, DTOs, interfaces, helpers and services independent of Django,
  DRF, settings and concrete persistence/integration implementations.
- Inject runtime dependencies through consumer-owned protocols. Construct
  implementations only in `src/core/composition.py`; do not add an adapter layer.
- Keep HTTP validation/serialization in `src/api` and all queries in repositories.
- Each API route has a package at `src/api/views/<group>/<endpoint>/` with
  `view.py`, `serializer.py` and `__init__.py`. Put input/output serializers in
  `serializer.py` and keep all HTTP methods for a route in its `view.py`. Import
  views directly from `view.py` in URL configuration. Write documentation in English.
- Do not define views in `__init__.py` or place serializers under `src/apps`.
- Enforce ownership and business invariants in use cases even for non-HTTP callers.
- Run `python scripts/check_architecture.py` and
  `python -m unittest discover -s tests/unit -v` for inner-layer changes.
- Run `STAGE=ci python manage.py test src.apps src.api --noinput` for persistence
  and API changes. Use PostgreSQL for transaction/locking verification as described
  in the development guide. Do not report unexecuted checks as passing.
- Preserve existing routes and response envelopes unless the requested feature
  changes their contract. Document intentional compatibility changes.

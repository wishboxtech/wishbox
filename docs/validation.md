# Redesign validation

Unit tests in `tests/unit` check business behavior and dependency direction without
Django setup. An independent import test loads all services with framework/settings
imports blocked. Django tests cover the API, repository mappings, rollback, DTO
serialization, batch queries and OTP/JWT cache behavior.

`AvatarLockingTests` runs only on PostgreSQL. It executes two concurrent patches,
checks that the second waits behind a lock and verifies that both changes survive
commit. SQLite skips this test.

## Previously recorded domain redesign checks

The original domain redesign recorded these results on 2026-10-02 with Python 3.12
and the project's current dependencies:

- 37 framework-independent unit tests passed.
- 151 unique Django/API tests passed on PostgreSQL, including concurrency testing.
- The same 151 tests passed on SQLite, with one PostgreSQL locking test skipped.
- Dependency checks, Python compilation and `git diff --check` passed.
- YAML parsing, local OpenAPI reference resolution, bundled routes and creation
  fields matching DTO requirements passed.

Discovery was corrected to avoid duplicate test cases and include repository and
website tests that previously had nonstandard filenames or package structure.
These are historical results recorded by the earlier redesign, not a claim that
PostgreSQL has been rerun for every subsequent file-layout change.

## Existing migration differences

`makemigrations --check --dry-run` reported the same two differences on the original
HEAD and the redesigned structure:

- `authentication.User.username`: the model uses `default=uuid.uuid4()` instead
  of a callable, unlike the UUID stored in the latest migration.
- `profile.Avatar.settings`: the model's `PrettyJSONEncoder` differs from the
  migration state.

The redesign does not change schema or add migrations. Resolve these differences
with a separate decision about the username default and encoder registration.
Generating a migration with a fresh UUID on every run is not a stable fix.

The in-memory cache does not prove Redis/NATS network integration or delivery
retries. Database transactions also do not guarantee file/cache rollback.
See [architecture.md](architecture.md) and the ADR for these limitations.

The pinned Flake8 version (`4.0.1`) does not start on Python 3.12 because the
`importlib.metadata.entry_points` API changed. Without changing dependencies,
check executable syntax/imports through compilation, the architecture checker
and test suites.

## Previously recorded endpoint module migration

The initial endpoint serializer migration recorded these results on 2026-10-02
in the main checkout at `/home/parsa/Desktop/wishbox`:

- 38 framework-independent unit tests and the architecture checker passed.
- 151 Django/API tests passed on SQLite, with one PostgreSQL locking test skipped.
- All 15 routes, including 13 JSON routes and two Swagger routes, preserved
  addresses, URL names, methods, permissions, authentication and throttling.
- All 13 JSON routes had local output serializers, and methods with request
  bodies also had local input serializers. Apps contained no serializer definitions/imports.
- Syntax, Pyflakes checks for changed files and `git diff --check` passed.

That migration moved only presentation code and architecture policy. Transaction
logic was unchanged, and PostgreSQL was not rerun. The PostgreSQL results above
belong to the earlier domain redesign.

## Endpoint directory layout

Each route now has `src/api/views/<group>/<endpoint>/view.py` and a sibling
`serializer.py`. Existing serializer classes and view handlers move without changes
to validation or behavior. Documentation is in English. The decision is recorded
in [ADR 0002](decisions/0002-endpoint-local-serializers.md).

Verified on 2026-10-02 in the main project at `/home/parsa/Desktop/wishbox`:

- Architecture dependency checks and 38 framework-independent unit tests passed.
- 151 Django/API tests completed on SQLite: 150 passed and the PostgreSQL-only
  locking test was skipped.
- All 15 routes retained their addresses, names, methods, permissions,
  authentication and throttling settings.
- All existing view handlers and serializer definitions match the original
  code after parsing, apart from their new file locations and imports.
- Black formatting checks and `git diff --check` passed.
- The rules, guides and decision records contain no Persian text.

PostgreSQL locking was not rerun for this file-layout change.

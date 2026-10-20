# Redesign validation

## Persian, guest identity and cat profiles (2026-10-20)

The [bilingual UI review](wishy-ui-review.md) supersedes the earlier English-only
interface and the earlier browser-access limitation below. It records actual
Chrome screenshots, two responsive review passes, accessibility checks, a real
API browser journey, current test totals and remaining browser/device limits.
Current suites pass: 50 framework-independent backend tests, 192 PostgreSQL API
and persistence tests, and 32 frontend unit/DOM tests. The SQLite suite passes
with four PostgreSQL-only checks skipped. Local `make up` is healthy at port 8080.

## Wishy UX, gifting and engagement (2026-10-20)

Verified in `/home/parsa/Desktop/wishbox` after the Wishy changes:

- Architecture checks and all 43 framework-independent unit tests passed.
- All 167 Django/API tests passed on PostgreSQL in the final Docker backend image,
  including simultaneous reservations (one success, one conflict), authorization,
  unique activity, inbox ownership/read state and transaction rollback.
- The 167-test SQLite run passed with two PostgreSQL-only locking checks skipped.
- TypeScript and Vite production builds passed. All 23 frontend tests passed
  natively and on Node 22 in the Docker development image. Five tests mount actual
  React components in an isolated DOM against a fake API: list/wish creation,
  guest reserve/purchase/cancel, owner receipt, reservation conflict and inbox read.
  Other coverage includes private guest key persistence, English-only branding,
  token refresh and sign-out during a pending refresh.
- `make up` built both applications, applied the gifting migration and started all
  four services healthy. Local Debug Toolbar middleware was excluded after a
  Docker-host DNS lookup was found blocking requests.
- HTTP checks through the real Nginx/backend stack passed for the Wishy index,
  built JavaScript, supplied cat image, shared deep-link fallback, private endpoint
  authorization, visitor validation, missing-resource responses and gifting schema.
- All OpenAPI YAML files parsed and all 33 local references resolved. Black,
  compilation and `git diff --check` passed.
- A previously flaky profile update test could randomly choose the existing name.
  It now uses guaranteed different values and verifies both response and database
  values, rather than comparing a response value with itself.

Browser access to `http://localhost:8080` was declined by the origin permission
gate. No visual browser QA, screenshots or real-browser responsive checks are
claimed. Isolated DOM tests do not replace visual browser verification.

See [gifting contracts and compatibility changes](wishy-gifting.md). In-app
notifications poll while visible; push/email/SMS, purchases and shipping are not
part of the gift lifecycle. Guest keys require keeping the original browser data.

## Full-stack application and application separation (2026-10-20)

The complete Django application has moved to `backend/`; the React application
is independent in `frontend/`. Shared Make/Compose orchestration remains at the
repository root. Python imports and HTTP contracts retain their existing names.

Verified after relocation:

- All 365 previously tracked backend files are present in their new locations.
  Content checks against HEAD found only the local settings selector and the two
  application files that were already modified before this work began.
- Architecture checks and all 38 framework-independent unit tests passed.
- The 151 Django/API tests passed with isolated SQLite settings (one PostgreSQL
  locking test skipped), and all 151 passed on PostgreSQL through Docker, including
  a final run in the image built from `backend/Dockerfile`.
- TypeScript checks, the Vite production build and all 13 frontend tests passed
  on both Node 22 in Docker and the native Node environment.
- Django's local-settings system check and both Compose configurations passed.
- Both images built from source. `make up` and `make dev` each started all four
  services with healthy status. The application was returned to the built
  frontend/Gunicorn configuration afterward.
- HTTP integration checks passed for the SPA index, JavaScript assets, shared
  deep links, authenticated API proxy behavior, admin CSRF and collected admin
  static files. The development runtime served the Vite HMR client and source
  modules and correctly proxied the API. The upload volume is writable by the
  non-root backend process.

The native PostgreSQL test command could not connect through the host's published
TCP port in this environment; PostgreSQL tests succeeded over the internal Docker
network. Browser access to the local preview origin was declined, so browser
interaction, visual appearance and responsive layouts have not been verified.
Server-rendering tests cover both interface languages, not visual layout.

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

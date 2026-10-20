# Architecture and development rules

This file is the project's canonical implementation policy. See
[architecture.md](docs/architecture.md) for the dependency map,
[development.md](docs/development.md) for the workflow, and
[0001-domain-boundaries.md](docs/decisions/0001-domain-boundaries.md) for migration decisions.

## Dependency direction

Code depends on contracts and the domain. Runtime flow and import direction are different:

```text
API → service → interface ← repository → Django model
         ↓          ↓          ↓
        DTO       domain      domain
```

1. `domain/` owns entities, value objects, policies and business errors. It does not
   depend on Django, the ORM, DRF, HTTP, settings or services.
2. `dto/` defines explicit input/output data. Pydantic DTOs use `frozen=True` and
   `extra="forbid"`. Do not pass Models, QuerySets, Requests, Serializers,
   UploadedFiles or callables through DTOs.
3. `interfaces.py` defines the service's requirements as `Protocol` contracts.
   The consumer owns the contract; the database implementation does not define it.
4. `services/` implements use cases and orchestration. Inject dependencies through
   constructors. Services must not import concrete repositories, models, settings,
   presentation code, JWT, Redis, NATS or Django, or construct runtime dependencies.
5. `repositories/` owns queries, record-to-entity/DTO mapping and persistence.
   Repositories must not invoke services or serializers or produce HTTP responses
   or permission decisions.
6. Presentation lives only in `src/api/`. Each API route has a package at
   `src/api/views/<group>/<endpoint>/` containing `view.py`, `serializer.py` and
   `__init__.py`. Define the route's input/output serializers in `serializer.py`
   and keep all its HTTP handlers together in one APIView in `view.py`.
   `__init__.py` only exports names and must not define views. URL configuration
   imports the endpoint's `view.py` directly. Defining or importing serializers in
   `src/apps/` is prohibited. Serializers handle syntax, initial validation and
   serialization; they must not call `save()` or execute queries. Each handler
   invokes one primary use case. Output serializers may inherit from the shared
   `DTOResponseSerializer` in `src/api/serialization.py`. HTML/YAML documentation
   endpoints do not need JSON serializers; their `serializer.py` documents this.
7. Assemble concrete dependencies only in `src/core/composition.py`. Do not add a
   separate `adapter` directory or layer.

## Business rules and communication between apps

- Enforce ownership, the existence of operation participants and business invariants
  in the domain/service. These rules must not depend on permissions or serializers.
- Updating or deleting a wish checks both wishlist ownership and the wish's
  membership in that wishlist.
- An app must not import another app's private models or repositories. Use that
  app's public service capability through an injected contract and DTOs/IDs.
- Service dependencies are explicit, one-way and free of cycles. Do not import or
  instantiate another app's concrete service inside a service.
- Preserve existing ORM foreign keys. A schema relationship does not authorize
  direct queries from the business layer.

## Transactions and side effects

- `TransactionBoundary` is an injected factory that creates a fresh context for
  each execution. Services must not call `transaction.atomic` directly.
- Stateful and multi-step writes need a transaction boundary. Acquire locks for
  checks and updates inside that same boundary.
- Schedule SMS and events associated with database changes through `AfterCommit`.
  Do not send them before commit.
- Cache and file storage do not roll back with the database. Durable delivery
  requires an outbox or independent compensation; `on_commit` does not guarantee retries.

## Data and API contracts

- Inputs use `*InputDTO`; outputs use `*OutputDTO`. Entities and response DTOs are distinct.
- PATCH uses `exclude_unset=True`: an omitted field differs from an explicit `null`.
  Allow `null` only for fields that are actually nullable.
- The authenticated user supplies the actor, and the URL supplies resource IDs.
  The request body must not override them.
- Business errors inherit from `DomainError`. Map status codes, translations and
  API error codes only in presentation code.
- Nested JSON in DTOs is a data snapshot. `frozen` restricts assignment but does not
  make dictionaries deeply immutable. Copy data before patching; do not mutate
  existing entities or domain values.
- List endpoints must not query separately for every cover/image. Use batch capabilities.

## Development checks

- Use absolute imports so dependencies remain explicit and checkable.
- Before finishing, run the architecture checker, relevant unit tests and relevant
  integration/API tests.
- Test business behavior with fake/mock contracts without Django. Test queries,
  mappings, rollback and HTTP behavior in Django tests.
- Verify locking and concurrency with PostgreSQL; SQLite does not prove lock correctness.
- Models and migrations describe the schema. Moving Python files does not require migrations.
- When endpoint behavior changes, update OpenAPI and the migration guide.
- Write documentation, docstrings and explanatory comments in English.
- Do not commit secrets, test media, virtual environments or test output.

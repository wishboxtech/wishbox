# ADR 0001: Domain boundaries and dependency direction

Status: Accepted and implemented — 2026-10-02

## Problem

The previous services imported serializers, the ORM, settings and JWT. Some wrote
data with `serializer.save()` and returned serialized dictionaries. Separating
services and selectors into directories alone did not make business logic independent.

## Decision

Use the Sodoor proposal to separate Presentation, Service and Repository.
Following the project's request, define explicit domains and Pydantic DTOs without
a separate adapter directory or layer. Inject runtime dependencies through
Protocols and construct concrete implementations in the composition root.
Repositories convert ORM records into entities.

Rename `UnitOfWork` to `TransactionBoundary` and make it a context factory.
Preserve models and migrations. Keep the API in its existing location; move
selectors and their tests into repositories.

## Compatibility and behavior changes

- Preserve existing endpoint addresses and successful response envelopes.
- Remove old service functions that accept dictionaries/Models and return
  tuples/dictionaries. Internal callers must use InputDTOs and service methods
  constructed in composition.
- Move input-format validation to serializers. Creation now validates every
  required field; incomplete payloads no longer reach database errors. Responses
  may contain multiple field error codes.
- Enforce ownership inside use cases. Updating/deleting a wish must establish
  both parent ownership and wish membership. PATCH cannot move a wish to another wishlist.
- Deleting a missing wishlist now returns 404; patching it returns 400 with a
  domain error. Previously permissions returned 403 for both missing resources and
  non-owners. Non-owners still receive 403; malformed UUIDs return 400.
- Respect the prefix during OTP verification. Align SMS sending with the existing
  function signature (`phone`, `otp`); do not add a new email sender.
- Business errors are independent of HTTP. Old exception imports from utils
  refer to domain errors; consumers must not expect HTTP `.message` and
  `.error_type` attributes on them.
- Map avatar images by ID so missing/duplicate widgets do not shift images.
  Reject unknown nested settings fields.
- `models/settings_schema.py` and `models/otp.py` only provide compatible exports
  for older schema/OTP imports; actual ownership is in the domain/repository.

## Limitations and separate future work

Worker/Celery redesign, outbox, delivery retries and financial schema changes
are outside this change. Cache and file storage are not atomic with the database.
The current schema/cache does not guarantee full concurrency safety for phone/email
uniqueness or one-time OTP consumption. Constraints or atomic consumption need
an independent decision and migration. SQLite does not guarantee row locking;
run write tests on PostgreSQL as well.

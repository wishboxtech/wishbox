# ADR 0002: Endpoint packages with separate views and serializers

Status: Accepted and implemented — 2026-10-02

## Problem

HTTP serializers previously lived in business apps. Views for routes with multiple
methods were assembled in `__init__.py` through multiple inheritance of operation
views. Reviewing a route's validation, response and permissions required several files.
An initial reorganization placed each route's view and serializers together in one
module. The requested layout instead gives each route a directory with separate
`view.py` and `serializer.py` files.

## Decision

Each API route uses `src/api/views/<group>/<endpoint>/` with:

```text
<endpoint>/
  __init__.py     # view exports only
  serializer.py   # this route's input/output serializers
  view.py         # one APIView with all handlers for this route
```

Methods with bodies have dedicated input serializers. GET/DELETE methods without
bodies do not need empty input serializers. Output serializers may use the shared
`DTOResponseSerializer` in `src/api/serialization.py`. The shared `input_dto`
helper converts validated input into DTOs and maps errors.

Keep serializers out of `src/apps/`; domains, DTOs, interfaces, services and
repositories must not depend on presentation code. URLs import the endpoint's
`view.py` directly; `__init__.py` only exports names. Swagger HTML/YAML routes use
the same package layout, but need no JSON serializer. Their `serializer.py` files
explain this distinction.

## Compatibility

Preserve addresses, URL names, HTTP methods, permissions, cookies and API data
contracts. The original migration removed `src.apps.<app>.serializers` imports
and views for individual methods. Current callers should import view implementations
from `src.api.views.<group>.<endpoint>.view` and serializers from the sibling
`.serializer` module. Endpoint packages also export their views for callers.
Business logic and database schema are unchanged by this file reorganization.

The route map is in [architecture.md](../architecture.md). The architecture checker
rejects serializers defined or imported in apps.

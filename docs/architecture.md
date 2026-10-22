# Wishy architecture

Backend code paths in this document are relative to `backend/`. The independent
React application lives in `frontend/`. Run direct Python/Django commands from
`backend/`; root Make targets select the correct directory automatically.

The browser application in `frontend/` communicates only through the public HTTP
API. It contains no persistence or backend business logic. Vite (development) and
Nginx (built application) proxy API and media requests to Django on the same origin.
See [the full-stack guide](full-stack.md) for runtime composition and startup.

This structure follows the Sodoor Architecture Proposal, with the project's decision
to define explicit domains and avoid a separate adapter layer. Django remains at
the outer boundaries. Binding rules are in [rule.md](../rule.md).

## Structure

```text
src/apps/<app>/
  domain/         # entities, value objects, policies, business errors
  dto/            # ORM-independent InputDTO / OutputDTO
  interfaces.py   # contracts consumed by use cases
  services/       # application use cases with injected dependencies
  repositories/   # Django/cache persistence and mapping to the domain
  models/         # Django schema
  tests/          # integration, repository and model tests
src/api/views/<group>/<endpoint>/
  view.py         # one APIView containing the route's HTTP handlers
  serializer.py   # this endpoint's input/output serializers
  __init__.py     # exports only
src/api/          # routes, permissions, shared serialization, error mapping
src/core/composition.py  # construction of concrete dependencies
src/shared/       # base DTOs, domain errors and transaction contracts
tests/unit/       # business tests without Django or a database
scripts/check_architecture.py  # import and cycle checks
```

Presentation lives only in `src/api/`; serializers do not belong in `apps/`.
Each API route has a directory containing its view and serializers in separate
files. Routes with multiple methods use one APIView, without combining separate
views through multiple inheritance. `__init__.py` only exports names.
`selectors/` has moved to `repositories/`; existing queries remain as `query_*`
functions for tests and database capabilities. New business code should consume
repository contracts. Django models are not business entities.

## Endpoint files

Paths below are relative to `/api/V0.0.0/`. Each listed `view.py` has a sibling
`serializer.py` containing that endpoint's serializers.

| Route | Methods | File under `src/api/views/` |
| --- | --- | --- |
| `auth/otp/` | POST | `authentication/send_otp/view.py` |
| `auth/otp/verify/` | POST | `authentication/verify_token/view.py` |
| `auth/otp/refresh/` | POST | `authentication/refresh_token/view.py` |
| `profile/` | GET, PUT | `profile/profile/view.py` |
| `profile/avatar/` | GET, PATCH | `profile/avatar/view.py` |
| `profile/wishlist/` | GET, POST | `wishlist/wishlist/view.py` |
| `wishlist/<id>/` | GET, POST, PATCH, DELETE | `wishlist/wishlist_action/view.py` |
| `wishlist/<id>/wish/<wishid>/` | PATCH, DELETE | `wishlist/wish_action/view.py` |
| `wish/<id>/` | GET | `wishlist/get_wish_by_id/view.py` |
| `wish/<id>/request/` | POST, PATCH | `wishlist/reserve/view.py` (legacy URL alias) |
| `wish/<id>/reservation/` | POST, PATCH | `wishlist/reserve/view.py` |
| `wish/<id>/activity/` | GET, POST | `wishlist/activity/view.py` |
| `wishlist/<id>/shared/` | GET | `wishlist/shared/view.py` |
| `gifts/` | GET | `wishlist/gifts/view.py` |
| `notifications/` | GET, PATCH | `wishlist/notifications/view.py` |
| `gifts/<id>/experience/` | GET, PATCH | `wishlist/experience/view.py` |
| `wish/create-anonymous-friend/` | POST | `wishlist/create_anonymous_friend/view.py` |
| `storage/upload/` | POST | `storage/upload_file/view.py` |
| `website/contact-us/` | GET | `website/contact_us/view.py` |
| `openapi/` | GET | `openapi/swagger_template/view.py` |
| `openapi/schema.yaml` | GET | `openapi/swagger_view/view.py` |

Define input serializers for methods with request bodies. Read/delete methods
without bodies do not need empty input serializers. Each route's output
serializers live in its `serializer.py`; generic DTO serialization remains shared
in `src/api/serialization.py`. Swagger's page and schema return HTML/YAML, so their
`serializer.py` files explain why JSON serialization is unnecessary. Existing
addresses and response envelopes are preserved except for the intentional secure
reservation migration documented in [Wishy gifting](wishy-gifting.md).

## Domain ownership

| App | Domain and business responsibilities | Public capabilities |
| --- | --- | --- |
| authentication | User identity, OTP requests/verification, login orchestration | `get_user` and identity DTOs |
| profile | Profile information, legacy avatar settings and versioned cat recipe value objects | `exists` and profile DTOs |
| storage | Media identity, file data, uploads and reads | `get_media` and `get_media_batch` |
| wishlist | Wishlists/wishes, ownership, gift lifecycle, single-use guest claims, unique activity and notifications | Wishlist and gifting use cases |
| website | Contact information | `list_contacts` |

Wishlist entities enforce ownership. Gifting policies enforce giver/owner roles
and the reserved → purchased → received lifecycle, including cancellation.
`GiftingService` locks the wish and writes notifications within the same transaction.
An injected clock governs planned holds, reminders and expiry. Recipient feedback
and giver-visible messages use separate output DTOs and explicit sharing actions.
Repository queries aggregate activity in batches. `gifting_interfaces.py` owns the
narrow protocols used by this use case; secure credential generation/hashing is
injected from composition. Avatar settings form a complete domain value
object: apply patches to a snapshot, then validate the whole value.

## Communication and injection

```text
GiftingService  → GiftRepository                ← DjangoGiftRepository
GiftingService  → GiftCredentials               ← SecureGiftCredentials
GiftingService  → WishlistReader                ← WishlistService
GiftingService  → ProfileServiceProtocol        ← ProfileService
WishlistService → ProfileServiceProtocol        ← ProfileService
WishlistService → StorageServiceProtocol        ← StorageService
ProfileService  → AuthenticationServiceProtocol ← AuthenticationService
ProfileService  → StorageServiceProtocol        ← StorageService
```

Service contracts use `<ServiceName>Protocol` so their corresponding provider
is clear. Each protocol exposes only capabilities needed by its consumers, not
every method of the concrete service. Implementations satisfy these protocols
structurally; explicit inheritance is unnecessary. Constructor parameters use
`authentication`, `profile` and `storage`, and composition passes them by keyword.

These are runtime relationships. Services import only Protocol contracts;
the composition root injects concrete instances. Repositories convert records
to dataclass entities or DTOs. Lazy QuerySets and Models do not enter services.

## Request flow

```text
request → input serializer → InputDTO → application service
        → injected repository / public capability → OutputDTO
        → response serializer → HTTP response
```

Views determine input format and response status. Services implement business
decisions and orchestration. DTOs contain UUIDs, Decimals, dates, bytes and JSON
data; the upload view converts uploaded files into bytes and a filename.

## Transactions and side effects

The transaction contract is `TransactionBoundary`. As a factory, it creates an
independent context for every call. The `atomic` implementation lives in
`src/shared/transactions.py`; only composition injects it.

Wishlist writes and avatar patches execute inside transactions with locks.
User lookup/creation during verification and login occurs inside a transaction;
tokens are created after successful exit. OTP notifications use `AfterCommit`.
Redis and SMS do not participate in database transactions. The current email
flow generates and verifies OTPs, but the project has no email sender yet.

FileFields also do not participate in database transactions; a database failure
may leave a file without a record. Uploads currently snapshot files in memory.
If upload sizes grow, introduce a streaming contract with defined cleanup.
This redesign does not add an outbox, worker redesign or guaranteed retries.

## Testing and architecture checks

The checker rejects outer imports in inner layers, direct presentation access to
persistence, private queries across apps, repository-to-service dependencies,
serializers defined/imported in apps, and cycles. A separate unit test imports
all services with Django/settings imports blocked. The checker complements code
review: it does not analyze dynamic imports or every business invariant.
See [development.md](development.md) for commands.

## Administrative reporting and media storage

The existing Unfold admin index calls a presentation callback in
`src/api/admin_dashboard.py`. The callback grants aggregate reporting only to
active superusers and delegates to `website.services.dashboard.DashboardService`.
That service combines framework-free DTO snapshots through consumer-owned
`UserMetricsReader` and `WishMetricsReader` protocols. Authentication and wishlist
repositories own their aggregate queries; composition constructs and injects both
readers. No ORM objects cross the boundary and no public metrics route is added.

The storage settings builder in `settings/storage.py` is shared by development
and production. S3 replaces only media storage; admin/static assets keep their
existing local storage. The existing-media copy command delegates to
`MediaMigrationService`, whose repository owns key enumeration and file transfer.
Source and destination storage implementations are assembled in composition.
See [storage and admin operations](storage-and-admin.md) for environment variables,
copying existing media, rate definitions and activity tracking limitations.


Guest signup linking crosses domains through authentication’s consumer-owned
`GuestClaims` protocol. Composition injects `GuestClaimService`, which consumes
`GuestRepository`, credential hashing and a transaction boundary. Authentication
owns first-signup eligibility; wishlist persistence owns one-time identity
consumption and effective gift ownership. No query or Django dependency enters
the authentication or wishlist service layers.

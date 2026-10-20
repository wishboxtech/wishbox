# Running the full Wishy application

Wishy has an independent React + TypeScript frontend in `frontend/`. The interface
supports English and Persian, with persisted language selection, RTL layout,
self-hosted Vazir text and a Lalezar Persian wordmark. It uses the supplied
purple/yellow Wishy cat identity, larger
text and a simple navigation: My wishlists, Gifts I’m giving, and Notifications.
It consumes Django at `/api/V0.0.0/`. Most existing routes and envelopes remain;
the intentional reservation contract change is documented in
[Wishy gifting](wishy-gifting.md).

The Django application is entirely contained in `backend/`, including its
`manage.py`, `src/`, `settings/`, Python requirements, tests, templates, OpenAPI
files, `.env` and `.env.test`. Each application owns its Dockerfile and dependency
manifest. Shared orchestration and local stack configuration live at the
repository root. Make commands below run from the root; direct Django and
backend Python commands run from `backend/`.

## One-command startup

Install Docker Engine with Compose v2+ and GNU Make. Python 3.12+ is needed for
the initial configuration helper; the application itself runs in containers.
If the compatible interpreter has a different name, set it explicitly, for
example `make up PYTHON=python3.13`.

```bash
cd /home/parsa/Desktop/wishbox
make up
```

The first run creates `.env.local` from `.env.example`, generates unique local
JWT/Django signing keys, builds both applications, starts PostgreSQL, Redis and a gift-maintenance worker,
waits for their health checks, applies migrations and collects static files.
It then waits for the backend before starting the frontend. Existing `backend/.env` and
`.env.local` files are never overwritten.

Open [Wishy](http://localhost:8080). The backend is available at
[the API documentation](http://localhost:8080/api/V0.0.0/openapi/) and
[Django admin](http://localhost:8080/admin/). The React application, API, media and
admin share an origin through Nginx; no extra CORS configuration is necessary.

Local settings explicitly enable `UNDER_DEVELOPMENT=True`. Sign in with any
valid Iranian mobile number (`09` followed by nine digits) and code **123456**.
No SMS is sent locally. Complete/save the profile before creating the first
wishlist. This follows the existing profile invariant in the backend.

These commands configure a **local development environment**, including debug
settings, fixed OTPs and local database credentials. They are not a production
deployment recipe. NATS/SMS credentials are unnecessary in this mode. The
existing production settings and delivery integrations remain separate.

```bash
make help                # List commands
make status              # Health and published ports
make logs                # Follow all service logs
make docker-superuser    # Create an administrator
make restart             # Restart services
make down                # Stop services without deleting data
```

Database data, Redis state and uploaded files use named Docker volumes. `make down`
preserves all volumes. If a default port is already occupied, change `WEB_PORT`,
`API_PORT`, `POSTGRES_PORT` or `REDIS_PORT` in `.env.local` before starting.
Published ports bind to `127.0.0.1`. Compose uses the project name `wishbox` and
does not use fixed container names.

## Development with hot reload

```bash
make dev
```

The same [local URL](http://localhost:8080) now serves Vite with React hot reload.
Django uses `runserver` and watches mounted backend files. API/media/admin/static
requests go through Vite's proxy. Run `make up` to return to built frontend assets
and Gunicorn. Both modes use the same data volumes. Re-run `make dev` after
dependency changes; `npm ci` runs while rebuilding the development image.

## Native frontend/backend processes

Use Python 3.12 or 3.13 and Node 22.12+ (Node 22 LTS is used in Docker).

```bash
make backend-install frontend-install
make infra
make migrate
make backend-run        # Terminal 1: Django at localhost:8000
make frontend-run       # Terminal 2: React at localhost:5173
```

Vite forwards `/api`, `/media`, `/admin` and `/static` to `127.0.0.1:8000`. Set
`API_PROXY_TARGET` when running Vite against a different local backend. Native
Django reads database/cache settings from `.env.local`; if infrastructure host
ports change, also update `DEFAULT_DATABASE_PORT` and `REDIS_URL` accordingly.

## Supported interface flows

- OTP sign-in, automatic access-token refresh and a per-tab session. The raw
  `Authorization` JWT contract remains. Signing out clears the session.
- A short profile setup: first name, optional surname and bio; choose a photo or
  build a cat from ten parts with 50 styles each, 16 fur colors and 12 backgrounds.
  Choosing a cat edits the draft; saving the profile persists it across devices.
- Create a named wishlist, add wishes with estimated whole-number prices, and
  optionally attach descriptions/images. New lists open immediately.
- Search list/wish names, edit, and permanently delete with a confirmation dialog.
- Share `/shared/<wishlist-id>` and `/wish/<wish-id>` links. Public lists show
  their real title, description, gift availability, likes and views.
- Reserve with a chosen purchase day, concrete next step and checked wish details,
  using either a guest nickname or registered profile. An unbought hold expires
  automatically, with a private in-app planning reminder and one optional date
  move. A private management token for guests is stored only in their browser.
- Follow the gift lifecycle: reserved → purchased → received. Only the giver
  can mark purchased/cancel; only the wishlist owner can confirm receipt.
  Cancellation/expiry releases the wish; received gifts record physical arrival.
  Recipients can save a private fit check-in, explicitly share/withdraw a personal
  note or practical request, and givers can acknowledge that request.
- View Gifts I’m giving, plus your own persistent notification inbox with
  unread badges and individual/all read actions. The header refreshes every 30
  seconds while the page is visible. Registered givers receive an arrival notice
  when receipt is confirmed, and
  a personal-note notice only if the recipient explicitly shares one.
- Like/unlike wishes and count one unique view per browser/account per wish.

Reservations do not purchase anything or transfer money. Prices use the owner's
currency; the existing schema does not contain a currency field. Guest keys are
not included in share links or public responses and cannot be recovered after
browser data is cleared. Original English/Persian user-written content remains
unchanged. Interface language never rewrites wishes or other user content.
Guest gifts can be linked once, with explicit consent during the first signup
in that browser. Existing-account logins never import guest activity. See
[the identity policy](wishy-gifting.md#one-time-browser-identity).

The visual direction combines light surfaces and rounded controls with Wishy’s
purple, warm yellow and the supplied `1-1.jpg` cat artwork. The original image is
included as `frontend/public/wishy-cat.jpg` and framed with CSS. Google Fonts have
system-font fallbacks; Persian fonts are bundled with their OFL licenses. The responsive layout adapts to narrow screens and honors
reduced-motion preferences. Avatar APIs remain available to existing clients;
the interface also stores a versioned `cat_avatar` recipe through the profile API.
See [the UI review](wishy-ui-review.md) for the review matrix, research and limits.

For native processes, `make gift-worker` starts the one-minute maintenance loop
in another terminal; `make gift-maintenance` runs it once. Compose starts it
automatically. Restart the worker after editing its Python code; its loop does
not use Django runserver’s code reloader. See [research and UX decisions](gifting-research.md).

## Validation

```bash
make check               # Architecture boundaries + frontend TypeScript
make test                # Unit tests, Django SQLite tests, frontend client tests
make frontend-build      # TypeScript + Vite production bundle
make postgres-test       # Native Django tests using local PostgreSQL
make docker-test         # Architecture, unit and PostgreSQL API tests in Docker
```

`make postgres-test` loads local database credentials before isolated test settings.
Use a development database role that may create test databases. Do not run these
commands against a production database. The PostgreSQL suite verifies profile locking and simultaneous gift reservations,
which SQLite cannot prove. Existing test media uses `/tmp/wishbox-test-media`.

The frontend tests cover actual React flows in an isolated DOM with a fake API,
the API's distinct response shapes, raw JWT header,
public requests, token refresh, rejected refresh, permission/network failures,
multipart upload, media URL handling, bilingual RTL branding, private guest management keys, gift action permissions
and rendering the actual dashboard. Native check/test commands require the
local Python and frontend dependencies to be installed first.

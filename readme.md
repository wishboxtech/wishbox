# Wishbox structure

A clean and structured python/Django template with OTP-Authenticatin

## Project Structure

```bash
.
├── build 
│   └── readme
├── certs
│   └── readme
├── manage.py
├── openapi # API documentations
│   ├── auth
│   │   ├── definitions.yaml
│   │   ├── otp.yaml
│   │   ├── refresh.yaml
│   │   └── verify.yaml
│   ├── readme
│   ├── schema.yaml # to build schema 
│   ├── swagger.yaml #‌ built swagger using schema
│   └── wallet
│       ├── create_card.yaml
│       └── definitions.yaml
├── requirements # requirements packages
│   ├── all.txt 
│   ├── common.in
│   ├── common.txt
│   ├── dev.in
│   ├── dev.txt
│   ├── production.in
│   └── readme
├── settings # settings directory for diffrent deployments
│   ├── common.py
│   ├── dev.py
│   ├── __init__.py
│   ├── production.py
│   ├── test.py
│   └── utils
│       ├── get_env.py
│       └── __init__.py
├── src
│   ├── api # HTTP layer
│   │   ├── apps.py
│   │   ├── exception_handler # HTTP layer exception handlers
│   │   │   ├── exception_handler.py
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── tests # E2E tests 
│   │   │   ├── __init__.py
│   │   │   └── views # Request handlers E2E tests
│   │   │       ├── authentication
│   │   │       │   ├── __init__.py
│   │   │       │   └── send_otp.py
│   │   │       ├── wallet
│   │   │       │   ├── create_card.py
│   │   │       │   └── __init__.py
│   │   │       └── website
│   │   │           └── test_api_contactUS.py
│   │   ├── throttling
│   │   │   └── throttling.py
│   │   ├── url_patterns_v0_0_0 # routes definitions
│   │   │   ├── authentication.py
│   │   │   ├── __init__.py
│   │   │   ├── openapi.py
│   │   │   ├── wallet.py
│   │   │   └── website.py
│   │   ├── urls.py
│   │   └── views # Request handlers
│   │       ├── authentication
│   │       │   ├── __init__.py
│   │       │   └── send_otp.py
│   │       ├── __init__.py
│   │       ├── openapi
│   │       │   ├── __init__.py
│   │       │   ├── swagger_template.py
│   │       │   └── swagger_view.py
│   │       ├── wallet
│   │       │   ├── create_card.py
│   │       │   └── __init__.py
│   │       └── website
│   │           ├── contact_us.py
│   │           └── __init__.py
│   ├── apps # application codes
│   │   └── authentication
│   │       ├── admin # admin panel codes
│   │       │   └── __init__.py
│   │       ├── backends
│   │       │   ├── __init__.py
│   │       │   └── jwt_auth.py
│   │       ├── functions
│   │       │   ├── __init__.py
│   │       │   └── jwt.py
│   │       ├── migrations # database migration files
│   │       │   ├── 0001_initial.py
│   │       │   ├── 0002_remove_user_username.py
│   │       │   └── __init__.py
│   │       ├── models # model files per app 
│   │       │   ├── __init__.py
│   │       │   ├── otp.py
│   │       │   ├── user_manager.py
│   │       │   └── user.py
│   │       ├── selectors # Data access layer
│   │       │   ├── create_user.py
│   │       │   ├── get_user.py
│   │       │   ├── __init__.py
│   │       │   └── user_exists.py
│   │       ├── serializers
│   │       │   └── __init__.py
│   │       ├── services # Buisness logic
│   │       │   ├── create_otp.py
│   │       │   ├── create_user.py
│   │       │   ├── __init__.py
│   │       │   ├── login_user.py
│   │       │   ├── otp_exists.py
│   │       │   ├── refresh.py
│   │       │   └── verify_otp.py
│   │       ├── signals
│   │       │   └── __init__.py
│   │       └── tests # Unit tests for application
│   │           ├── backends
│   │           │   ├── __init__.py
│   │           │   └── jwt_auth.py
│   │           ├── functions
│   │           │   ├── __init__.py
│   │           │   └── jwt.py
│   │           ├── __init__.py
│   │           ├── selectors
│   │           │   ├── create_user.py
│   │           │   ├── get_user.py
│   │           │   ├── __init__.py
│   │           │   └── user_exists.py
│   │           └── services
│   │               ├── create_otp.py
│   │               ├── create_user.py
│   │               ├── __init__.py
│   │               ├── login_user.py
│   │               ├── otp_exists.py
│   │               ├── refresh.py
│   │               └── verify_otp.py
│   ├── core
│   │   ├── asgi.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── static
│   │   ├── error_enum.py
│   │   ├── __init__.py
│   │   └── serializer_errors.py
│   └── utils # utilities
│       ├── exceptions
│       │   ├── general.py
│       │   ├── __init__.py
│       │   └── otp.py
│       ├── fakers
│       │   ├── contact_us.py
│       │   ├── __init__.py
│       │   └── user.py
│       ├── __init__.py
│       ├── nats
│       │   ├── client.py
│       │   ├── __init__.py
│       │   └── publish.py
│       └── otp
│           ├── gen_otp.py
│           ├── __init__.py
│           └── send_sms.py
└── templates #‌ templates to get used by TemplateView
    ├── cr_swagger.html
    ├── swagger.html
    ├── verify_fail.html
    └── verify_success.html
```

## 🔧 Technology Stack
- [Django](http://docs.djangoproject.com/en/5.2/) - Web framework
- [PostgreSQL](https://www.postgresql.org/docs/) - Database
- [Redis](https://redis.io/docs/latest/) - caching
- [Swagger](https://swagger.io/docs/) - API documentation

## Architecture

This template follows clean architecture principles.

**1. Application Layer** (`apps/services/`)
- Buisness entities
- Use case orchestration
- Domain service implemetation

**2. Infrastructure Layer** (`apps/selectors/`)
- Database implementations
- External service integrations
- Repository implementations

**4. Interface Layer** (`api/`)
   - HTTP handlers
   - Middleware
   - Route definitions

## 🚀 Getting Started

### installation and run 

**1. install dependecies**
```bash
>>> python -m venv venv
>>> source venv/bin/activate
>>> pip install -r requirements/all.txt
```

**2. configure environment variables in .env**
```bash
>>> nano .env
```
> Text me if you need a template

**3. change stage to development**
```bash
>>> export STAGE=dev
```

**4. Run the server**
```bash
>>> python manage.py runserver
```

---

## 🧭 How to Develop in This Project

### 1. Overview

This project follows a **clean architecture** approach:

* **Selectors** = data access (queries only)
* **Services** = business logic
* **Views** = HTTP layer (request/response)
* **Tests** = each layer has its own dedicated test folder
* **OpenAPI** = every new API endpoint must be documented
* **Settings / Requirements** = must remain consistent and environment-separated

We **do not** use direct CRUD operations inside views or serializers.
All business logic must flow through the `selectors` → `services` → `views` chain.

---

## 🧱 Directory Structure (Simplified Flow)

```
src/apps/<app_name>/
    models/          # Django ORM models
    selectors/       # Data access (queries)
    services/        # Business logic (pure Python)
    tests/           # Unit tests (organized per layer)
src/api/views/       # HTTP handlers
src/api/tests/       # E2E tests
openapi/             # Swagger/OpenAPI YAMLs
```

---

## 🧩 Step-by-Step Development Workflow

### Step 1 — Create or Update Models

Define your data structure in:

```
src/apps/<app_name>/models/
```

Example:

```python
# src/apps/authentication/models/otp.py
from django.db import models

class OTP(models.Model):
    phone = models.CharField(max_length=20)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
```

Then create your migration:

```bash
python manage.py makemigrations <app_name>
python manage.py migrate
```

✅ **Write unit tests for your models** in:

```
src/apps/<app_name>/tests/models/
```

---

### Step 2 — Create a Selector (Data Access Layer)

Selectors are **read-only** data access functions that wrap Django ORM queries.

📍 Path:

```
src/apps/<app_name>/selectors/
```

Example:

```python
# src/apps/authentication/selectors/get_user.py
from src.apps.authentication.models import User

def get_user_by_phone(phone: str):
    return User.objects.filter(phone=phone).first()
```

✅ **Write selector tests**:

```
src/apps/<app_name>/tests/selectors/test_get_user.py
```

---

### Step 3 — Create a Service (Business Logic)

Services implement business rules, combining selectors, validations, and model logic.

📍 Path:

```
src/apps/<app_name>/services/
```

Example:

```python
# src/apps/authentication/services/verify_otp.py
from src.apps.authentication.selectors.get_user import get_user_by_phone
from src.apps.authentication.models import OTP
from src.utils.exceptions.otp import InvalidOTPError

def verify_otp(phone: str, code: str):
    otp = OTP.objects.filter(phone=phone, code=code).first()
    if not otp:
        raise InvalidOTPError()
    user = get_user_by_phone(phone)
    return user
```

✅ **Write service tests**:

```
src/apps/<app_name>/tests/services/test_verify_otp.py
```

---

### Step 4 — Add a View (HTTP Layer)

Each endpoint should use the corresponding service, not directly query models.

📍 Path:

```
src/api/views/<feature>/
```

Example:

```python
# src/api/views/authentication/send_otp.py
from rest_framework.response import Response
from rest_framework.views import APIView
from src.apps.authentication.services.create_otp import create_otp

class SendOTPView(APIView):
    def post(self, request):
        phone = request.data.get("phone")
        create_otp(phone)
        return Response({"detail": "OTP sent successfully"})
```

✅ **Add route in:**

```
src/api/url_patterns_v0_0_0/<feature>.py
```

✅ **Write E2E test for the view:**

```
src/api/tests/views/<feature>/test_send_otp.py
```

---

### Step 5 — Update OpenAPI Documentation

Each endpoint must have a YAML spec file.

📍 Path:

```
openapi/<feature>/<endpoint>.yaml
```

Example:

```yaml
# openapi/auth/send_otp.yaml
post:
  summary: Send OTP to user phone
  requestBody:
    required: true
    content:
      application/json:
        schema:
          type: object
          properties:
            phone:
              type: string
  responses:
    "200":
      description: OTP sent successfully
```

Then **update `schema.yaml`** and rebuild the main Swagger spec:

---

### Step 6 — Add or Update Requirements

If your feature introduces new dependencies:

1. Add them to the appropriate `.in` file inside `requirements/`
   (e.g., `requirements/dev.in` or `requirements/common.in`)
2. Compile with **pip-compile**:

   ```bash
   pip-compile requirements/common.in
   pip-compile requirements/dev.in
   ```
3. Commit both `.in` and compiled `.txt` files.

---

### Step 7 — Testing

Run all tests before committing:

```bash
pytest --disable-warnings -q
```

Recommended structure:

```
tests/
 ├── apps/<app_name>/...        # Unit tests
 ├── api/tests/views/...        # E2E tests
```

---

### Step 8 — Git Workflow

All development should happen on a **feature branch**:

```bash
git checkout -b feature/<short_description>
```

Once done:

1. Format and lint your code

   ```bash
   black src
   isort src
   flake8
   ```
2. Run tests

   ```bash
   pytest or coverage
   ```
3. Commit your changes

   ```bash
   git add .
   git commit -m "feat(auth): add OTP verification service"
   ```
4. Push and open a **Pull Request (PR)**.

---

## 🧠 Developer Notes

* **Never import models directly inside views** — use services.
* **Never put queries inside services** — use selectors.
* **Never commit to `main` branch directly.**
* **Always update OpenAPI and tests** when changing or adding endpoints.
* **Document non-trivial functions** with docstrings.


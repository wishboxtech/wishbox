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


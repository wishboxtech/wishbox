# Arvan S3 uploads and the admin overview

## Enable S3 media storage

Uploaded media uses Django's `default` storage. Local and production settings now
share the same S3 configuration; `STAGE=local` can upload to Arvan while retaining
development login behavior. Test settings continue to use isolated local storage.
Static assets, including Django admin and dashboard CSS/JS, remain on the current
local static storage. Frontend build assets remain in the frontend image.

1. In Arvan Object Storage, create the `wishy` bucket (or choose another name if
   it is unavailable). Leave public listing/reading disabled for signed media.
2. Copy the **service endpoint** and region from the selected region's panel.
   The endpoint must not include the bucket name. Obtain S3 Access/Secret Keys
   from Object Storage access management; a CDN/API key is not an S3 credential.
3. Add the following to the server's `.env.local`. These examples are placeholders;
   use the actual endpoint and region shown in your panel:

```dotenv
USE_S3=True
S3_BUCKET_NAME=wishy
S3_ENDPOINT_URL=https://s3.YOUR-REGION.arvanstorage.ir
S3_REGION_NAME=YOUR-REGION
S3_ACCESS_KEY_ID=YOUR-ACCESS-KEY
S3_SECRET_ACCESS_KEY=YOUR-SECRET-KEY
S3_ADDRESSING_STYLE=path
S3_QUERYSTRING_AUTH=True
S3_QUERYSTRING_EXPIRE=3600
S3_CUSTOM_DOMAIN=
S3_LOCATION=
```

4. Keep credentials in the server environment file, which is gitignored. Protect
   the file with `chmod 600 .env.local`. For a native production process, supply
   the same variables through its environment or `backend/.env`.
5. Rebuild and recreate the application from the repository root:

```bash
make up PYTHON=python3
```

The key must allow reading, writing and checking objects in this bucket. The copy
command below also checks whether each destination object exists. Private file
URLs are generated on each API read and expire after one hour by default. Signing
does not change the existing API response envelopes. Keep authenticated API
responses out of CDN caches. Server-mediated uploads and image display do not
require browser direct-upload CORS rules.

If intentionally serving public media through a custom domain, configure the
bucket/CDN for public reads, set `S3_QUERYSTRING_AUTH=False`, and set
`S3_CUSTOM_DOMAIN=media.wishy.ir` (hostname only). A custom domain cannot be used
with this configuration's private signed URLs. No ACL is sent automatically.
`S3_LOCATION` optionally prefixes object keys; keep it unchanged after uploading.
S3 can be disabled with `USE_S3=False`; the string `False` is parsed as false.

Legacy `MINIO_STORAGE_ENDPOINT`, `MINIO_STORAGE_MEDIA_BUCKET_NAME`,
`MINIO_STORAGE_ACCESS_KEY` and `MINIO_STORAGE_SECRET_KEY` remain fallback inputs;
new `S3_*` values take priority. Set `S3_REGION_NAME` explicitly. Legacy
`S3_MEDIA_URL` is accepted only as a bucket name, never as a URL. S3 static storage
from the old production-only configuration is intentionally replaced by local
static storage so admin assets do not become private signed assets.

### Existing local uploads

Switching storage does not move existing files automatically. Pause uploads while
copying. Keep the existing media volume attached and preserve a backup. After
deploying the configuration, run from the repository root:

```bash
docker compose --project-name wishbox --env-file .env.local \
  -f build/docker-compose.yaml exec back \
  python manage.py copy_local_media_to_s3 --dry-run

docker compose --project-name wishbox --env-file .env.local \
  -f build/docker-compose.yaml exec back \
  python manage.py copy_local_media_to_s3
```

The command iterates only database-referenced files, preserves their keys, skips
objects already present in S3, reports missing files, and never removes local
files. It can be rerun. A nonzero exit status with `missing` means some files need
restoring. If an S3 key already exists, its contents are assumed to be the intended
file; verify this before reusing a populated bucket. An API or credential error
stops the command so it can be corrected and rerun. Existing media may be
temporarily unavailable between enabling S3 and finishing the copy.

Afterward, upload an image through Wishy and verify it opens in a shared wishlist
and the admin. This live check requires the actual bucket and credentials; local
automated tests use botocore stubs and never contact Arvan.

## Dashboard definitions

The existing `/admin/` homepage now includes an overview for **active superusers**.
Other staff retain the normal admin homepage without aggregate data. No public
metrics endpoint is added. The model list and recent admin actions are preserved.

| Metric | Definition |
| --- | --- |
| Active users | Enabled normal customer accounts with a successful login in the last rolling 30 days |
| Enabled accounts | Normal customer accounts with `is_active=True`, regardless of login recency |
| Total customer accounts | All normal accounts, including disabled accounts; excludes staff, superusers and administrator-type accounts |
| Wishes created | All currently stored wishes; deleted wishes cannot be counted retrospectively |
| Wishes fulfilled | Distinct stored wishes with a `received` reservation; reserved, purchased and legacy accepted requests are not fulfillment |
| Overall fulfillment rate | Fulfilled wishes / all currently stored wishes × 100 |
| Fulfillment by gender | The same per-wish rate within each **wish owner's** recorded gender; not the giver's gender |
| Not specified | Missing, blank and unrecognized gender values; no inference from names, phone numbers or avatars |

The four main cards show active users, wishes, fulfilled wishes and overall rate.
Below them are account totals, gender counts/rates with progress bars, current
gift stages and a 30-calendar-day chart. Daily creation uses `Wish.created_at`;
daily fulfillment uses `ReservationRequest.received_at`. Dates and cutoffs use
UTC. A fulfillment record without a receipt timestamp affects the overall count
but cannot be placed on a daily chart. The chart is an event trend, not a
creation-cohort conversion chart. Its exact values are available in an accessible
table. No external chart library or CDN script is required.

An empty denominator displays a dash rather than an invented percentage. Gender
groups show their denominators so small samples and incomplete profile data are
visible. Totals use a fixed five aggregate queries, independent of user/wish count;
reservation attempts cannot multiply the number of wishes.

### Login tracking

The OTP and direct application login use cases now update the existing
`User.last_login` field **after successful token issuance**. Invalid OTPs,
disabled accounts and failed token issuance do not mark activity. Refreshing a
token does not represent a new login. Django admin logins remain separate and
staff accounts are excluded from customer metrics. Older application logins were
not recorded, so activity before this release cannot be backfilled from the
available schema. No database migration is required.

## Validation

From `backend/`, using the project's compatible Python environment:

```bash
python scripts/check_architecture.py
python -m unittest discover -s tests/unit -v
STAGE=ci python manage.py test src.apps src.api --noinput
```

Sources: [Arvan bucket setup](https://docs.arvancloud.ir/fa/object-storage/),
[Arvan access management](https://docs.arvancloud.ir/fa/object-storage/dashboard/),
[django-storages S3 configuration](https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html).

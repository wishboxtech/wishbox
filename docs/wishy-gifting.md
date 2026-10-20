# Wishy gifting and engagement

## Product flow

Create a profile once, name a wishlist, add wishes, and copy its link. Descriptions
and photos are optional. A friend opens the link, selects a wish and reserves it.
Guests supply a nickname; registered users use their authenticated profile.

The giver buys the item independently and marks **I’ve bought it**. The owner
confirms **I’ve received this gift** after delivery. The giver can cancel before
receipt, releasing the wish. Received gifts are final. Payment, shipping and
external shopping integrations are outside this application.

## Business invariants

`GiftingService` enforces permissions and transitions for every caller. It injects
a consumer-owned `GiftRepository`, `GiftCredentials`, `WishlistReader`, profile
capability and transaction boundary through `src/core/composition.py`.

A reservation locks the wish row inside its transaction. The database additionally
has a conditional unique constraint for one reserved/purchased/received gift per
wish. A concurrent second reservation returns a conflict. Purchase/cancel/receive
also lock the wish before reading the active reservation. The owner cannot reserve
their own wish while authenticated. Only the giver can buy/cancel, and only the
owner can receive after purchase. Notifications and reservation updates share the
same database transaction; notification failure rolls back the whole operation.

Guests receive a cryptographically random 256-bit management token once. Only its
SHA-256 hash is persisted. Constant-time comparison checks the guest token supplied
in `X-Wishy-Gift-Token`. Tokens never belong in URLs. A previous cancelled token
cannot manage a later reservation. Registered givers can also use their account.
The UI persists guest keys in this browser and never inserts them into shared
links. Clearing browser data loses guest access. First-time signup can import
this browser’s gifts with consent; otherwise sign in before reserving for
cross-device management.

A view is unique per account/browser per wish for all time. Guests use a persistent
random UUID in `X-Wishy-Visitor`; authenticated users use their account regardless
of that header. Like/unlike sets one state rather than incrementing counters.
These are lightweight engagement counts, not verified human analytics: clearing
browser data or creating another account can create another unique identity.
Public activity includes counts, status and actor-relative owner/giver flags,
without giver IDs, names or management credentials.

## Routes

All routes use `/api/V0.0.0/` and the existing response envelope. Raw JWTs are
supplied in `Authorization` without `Bearer`.

| Route | Methods | Contract |
| --- | --- | --- |
| `wishlist/<id>/shared/` | GET | Public metadata, wishes, batched activity, `is_owner`; visitor header required. |
| `wish/<id>/activity/` | GET, POST | Visitor header required. POST `action`: `view`, `like`, `unlike`. Optional guest key identifies giver. |
| `wish/<id>/reservation/` | POST, PATCH | POST guest `nickname` or registered session; returns gift plus one-time key. PATCH `action`: `purchase`, `cancel`, `receive`. |
| `wish/<id>/request/` | POST, PATCH | Alias of the secure reservation route; see compatibility below. |
| `gifts/` | GET | Authenticated giver’s latest 200 gifts, including cancelled/received; no keys. |
| `notifications/` | GET, PATCH | Authenticated inbox; latest 100 notices plus total unread. PATCH `notification_id` to read one, omit/null to read all. |

Missing wishes and shared lists return 404. Conflicts return 409; forbidden lifecycle actions return 403. Notifications survive
wish deletion with a snapshot of its name and a null `wish_id`. Read updates are
always scoped to the authenticated recipient. The frontend polls the inbox every
30 seconds while visible. These are in-app notifications, not push/SMS/email.

## Intentional compatibility changes

- The old `/wish/<id>/request/` URL remains, but no longer accepts arbitrary
  `friend`/`anonymous_friend` IDs. Those IDs did not prove identity and allowed
  impersonation. Use the verified session or submit a guest nickname. The success
  envelope retains `created`, `data`, `status`; its data is the new gift schema
  (`id`, `wish_id`, `wishlist_id`, `wish_name`, `status`, `created_at`, one-time
  `management_token`). Update older clients to these fields.
- `WishlistService.submit_reservation` is retired and rejects unverified IDs.
  Internal callers should use `GiftingService.reserve` with the new input DTO.
  The anonymous-friend creation endpoint remains for existing clients but no
  longer grants authority to manage a reservation.
- Existing pending/accepted/rejected request records are preserved as historical
  requests. They are not active gifts in the new lifecycle and do not block a new
  reservation. They cannot be upgraded using an unverified anonymous ID.
- Existing wish responses add `wishlist_id`; existing list endpoints/envelopes
  remain. Prices now reject negative values in HTTP and use-case inputs. Wish/list descriptions now accept empty strings or omission on create.
- The interface supports English and Persian, sets the document direction, and
  sends the selected `Accept-Language`. User-written content is preserved.
- The Django Debug Toolbar middleware is omitted in `STAGE=local`: its optional
  Docker-host DNS probe delayed every request on Linux. Production settings are
  unchanged.

Run `make architecture unit-test api-test frontend-test frontend-build` and
`make docker-test` to validate policies, API behavior and PostgreSQL concurrency.

## Planned holds and recipient experience (2026-10-20)

See [research and product reasoning](gifting-research.md) for sources, limits and
why receipt, private fit, and a voluntarily shared message are separate events.

New reservations require `purchase_by` (date), `purchase_plan` (3–160 characters)
and `details_checked=true`, in addition to the existing authenticated actor or
guest nickname. The use case validates today through 30 days ahead using an
injected UTC clock. `expires_at` is midnight UTC two calendar days after the
chosen date, providing a cross-time-zone buffer. Purchased/received gifts do not
expire. Cancelled and expired history remains accessible to the giver.

`PATCH wish/<id>/reservation/` adds `action=reschedule` with `purchase_by`: only
the giver can move a reserved hold once, to a later date within seven days of the
original day and within 30 days of today. Replanning resets the private reminder.
All transitions check state and authorization inside the wish lock. The same
contract applies to the legacy `/request/` URL. Existing reserved rows receive a
fresh approximately seven-day window at migration rather than immediate expiry;
old receipt dates are not invented.

`GET/PATCH gifts/<reservation-id>/experience/` authenticates the registered actor
or guest giver key, including closed gifts. Unknown or unauthorized gift IDs both
return 404. Owner GET returns a lean receipt summary, private `fit`/`private_note`,
and their shared messages. Giver GET returns their own plan/receipt plus only
explicitly shared `thank_you`/`follow_up_note` fields. Giver/public projections
never include private feedback. Shared-list/wish activity returns a reservation ID
only to an authorized owner or registered giver (or a matching guest key on wish
activity), not to the public. The owner projection omits the giver's plan.

Recipient PATCH actions after receipt:

- `save_private`: optional `fit` (`fits`, `adjust`, `not_for_me`, `trying`, or null)
  and/or `private_note` (up to 800 characters). No notification or public change.
- `share_thanks` / `withdraw_thanks`: explicitly share or remove their own
  nonblank `thank_you` message, up to 800 characters.
- `share_follow_up` / `withdraw_follow_up`: explicitly share or remove a practical
  `follow_up_note`, up to 800 characters. The private fit/note is never copied.

Only the giver can PATCH `acknowledge_follow_up`, after receipt and while a shared
request exists. Repeated acknowledgment is idempotent. It records attention, not
resolution. Message writes and notifications share one transaction.

`gift_received` now means actual arrival; it does not send an invented thank-you.
`thanks_shared`, `follow_up_shared`, and `follow_up_seen` are explicit actions.
`plan_reminder`, `hold_expired`, and `hold_released` do not include personal plan
or recipient feedback text. Shared notes may be withdrawn; the associated
notification contains only the wish name, so withdrawn message text is not kept
in notification snapshots.

## Maintenance runtime

`make up` / `make dev` now include a `gift-worker` service, sharing the backend
image, with its own heartbeat health check. It runs `maintain_gifts --loop` every
60 seconds. Candidates are processed in batches of 200; each wish is rechecked
under a row lock so concurrent workers produce one expiry/notification. Failures
roll back the affected wish and the worker retries on its next loop.

For native development, run `make gift-worker` in another terminal. Use
`make gift-maintenance` for a one-shot pass. API activity/shared reads and gift
mutations also apply expiry checks, so an overdue hold cannot indefinitely block
a new reservation if the worker was stopped. The worker is still needed for
reminders while nobody is browsing. Guests do not receive background messages
without a registered inbox; the UI states this explicitly. No email, push or SMS
reminders are implied. A plan and a self-reported purchase do not verify payment
or guarantee physical fulfillment.

## One-time browser identity

Guest reservations may additionally send a 64-character lowercase hexadecimal
`guest_key`. The browser generates 32 random bytes and retains the secret locally.
This is separate from the public visitor UUID and each gift’s management token.
Only the SHA-256 digest is stored in `GuestIdentity`; the secret is never returned,
put in URLs, exposed to the recipient or included in public responses.

`POST auth/otp/verify/` accepts the optional key. Authentication verifies the OTP
first and invokes the injected `GuestClaims` capability **only when creating a
new account**. The interface offers an unchecked consent box when this browser
has eligible guest gifts. No key is submitted without that choice. Linking and
account creation share a transaction. The guest identity is row-locked and can
be consumed once, by one user; a user can claim one identity. Account deletion
preserves the consumed marker so the identity cannot be reassigned.

Claimed gifts belong to the account, appear in its Gifts page, and work from
another browser after login. Previous guest management tokens stop granting
access as soon as the identity is consumed. Later guest reservations with that
consumed key are not attached. The UI clears successfully imported local gift
records and retires the browser key. It also records the decision after a login
without linking, so it does not repeatedly prompt. Existing accounts never claim,
including an account first created on a phone and later used in this browser.
This intentionally chooses the conservative signup-only policy for shared devices.

The OTP response adds `is_new_user` and `guest_claimed` booleans. Existing gift
routes/envelopes remain. Old guest reservations without a browser identity retain
their original management-token behavior and are not bulk imported retroactively.
Registered users may manage imported gifts before completing their profile;
inbox notifications begin once their profile exists.

## Cat profile recipes

`GET/PUT profile/` adds nullable `cat_avatar`, version 1. Parts `face`, `ears`,
`eyes`, `pupils`, `brows`, `nose`, `mouth`, `whiskers`, `markings` and `accessories`
are strict integers 0–49; `fur` is 0–15 and `background` is 0–11. Missing recipe
properties default to zero. Unknown properties and invalid types/ranges fail
validation in the domain DTO, including non-HTTP callers. Omission preserves an
existing recipe; explicit null removes it and selects a photo. Existing avatar
routes and photo support remain available.

Apply migrations `wishlist.0006`, `profile.0005` and `authentication.0006` before running this version.
The profile migration also records the JSON encoder already used by legacy
Avatar.settings. Authentication changes an import-time UUID default into a callable
so separate users receive separate defaults and migration checks remain stable.

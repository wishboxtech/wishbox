# Wishy bilingual UI and gifting review

Review date: 2026-10-20. The existing purple/yellow cat identity is retained.

## Product decisions

The gift journey keeps physical arrival separate from satisfaction. Recipients can
write privately without notifying the giver, and deliberately share or withdraw a
thank-you or practical request. This avoids turning a gift into a public rating.
The existing [gifting research](gifting-research.md) explains that policy.

Anonymous gift history links only during the first account signup, with an
unchecked consent choice. Existing-account logins do not import it, including
returning from another device. This deliberately favors predictable behavior on
shared browsers. The decision is shown once per retained browser storage. The
server also enforces single-use identity consumption; this is not merely a UI
flag. See [the identity contract](wishy-gifting.md#one-time-browser-identity).

Cats provide a small act of self-expression: ten independently selectable parts,
50 styles per part, color palettes, random selection and undo. The builder edits a
profile draft; its final button clearly asks the user to save the profile. There
are 500 exported SVG layers, with geometric differences rather than renamed
color-only copies. Styles are grouped into families with smaller variants.

## Persian direction, type and copy

The implementation follows the W3C's [HTML direction guidance](https://www.w3.org/International/questions/qa-html-dir.en.html)
and [bidirectional text practices](https://www.w3.org/International/docs/bp-html-bidi/):
set `lang` and `dir` on the document, use logical spacing/alignment, isolate mixed
content, keep phone numbers and URLs LTR, and use `dir=auto` for user-written
names/descriptions. Directional navigation arrows mirror; the cat artwork does
not. Separate duplicate page trees were unnecessary and would let features drift.

Persian text uses self-hosted Vazir regular/bold from the
[official font project](https://github.com/rastikerdar/vazir-font/tree/v30.1.0/dist),
with OFL included. The Persian wordmark «ویشی» uses
[Lalezar](https://github.com/google/fonts/tree/main/ofl/lalezar), beside the original
cat logo. Font fallbacks and relaxed Persian line-height prevent Latin tracking
rules from breaking connected letters.

The interface dictionary uses conversational Persian, with the requested hero
«یکم راهنمایی برای هر کادویی لازمه». The
[Taaghche homepage](https://taaghche.com/) was reviewed as an example of short,
direct Persian product copy; Wishy's text is original. User content is never
translated. Dates/prices follow the selected locale. Price entry accepts Persian,
Arabic and Latin digits, including thousands separators, while rejecting
negative/fractional values. The browser-native date input
still accepts Gregorian dates; Persian copy explicitly explains this and shows a
Persian date confirmation after selection.

## Two review methods

Every state below has two browser passes in both languages. The first captures
screenshots at 390 and 1440 pixels, checks horizontal overflow/clipped controls,
and runs axe WCAG 2 A/AA and 2.1 AA checks. The second resizes the rendered page
between 320 and 768 pixels, exercises keyboard focus, checks modal focus trapping,
background inertness, Escape/restore, and scrolling with the close control visible.
This is 132 configurations per pass, 264 total. Static component/CSS and copy
review supplements the browser passes; screenshots were also inspected visually.

| Area | Reviewed states |
| --- | --- |
| Entry/navigation | Landing, help, contact, missing route, loading failure |
| Collections | Dashboard, empty dashboard, owner list, public shared list, empty shared list, long mixed content |
| Wishes/gifting | Public wish, reserved giver, purchased recipient, received recipient, received giver, gifts overview |
| Account | Notifications and its empty state, profile, sign-in, OTP, empty gifts, empty/error contact |
| Dialogs | Reservation plan, new list, edit list, new wish, edit wish, share, delete, cat builder |

Issues found and fixed include low contrast for small labels, RTL step-number and keepsake-cat
collisions, physical left/right spacing, long-content overflow, overly tall
reservation dialogs, inaccessible background controls during dialogs, missing
image previews, and contact navigation opening the help page. The reservation
form now keeps its heading/close control separate from the scrolling content,
with the action reachable at the bottom and secondary policy text in a disclosure.

A separate interaction test checks that changing language preserves a profile
draft, loads Vazir, persists the language, and keeps cat pagination, undo, cancel,
selection and profile persistence distinct. Additional checks cover the account
menu’s viewport bounds, Escape/focus restoration and cat/text separation at all
four widths. The real-backend browser test covers
guest reservation → consent/first signup → cat profile → purchase → receipt →
private feedback → shared thanks → login from another browser. It verifies that
the giver never sees the recipient's private note and that the cat follows the
account.

## Reproduction

From `frontend/`, with Node 22.12+:

```bash
npm ci
npm test
npm run build
npm run cats:export
npm run test:ui
```

The UI tests start Vite on 5174 when needed. Set `CHROME_PATH` to use an installed
Chrome, or install Playwright Chromium with `npx playwright install chromium`.
`WISHY_UI_URL` targets an already running frontend. Tests use API fixtures and
isolated browser contexts, never a user's browser profile. Screenshots are written
to `/tmp/wishy-ui`; Playwright diagnostics to `/tmp/wishy-playwright-results`.

Inspect `/cat-parts/review.html` for all 500 layers in a complete face and
`/cat-parts/samples.html` for 250 balanced mixed cats. Each layer group was
visually reviewed. Unit checks also render every layer, verify unique geometry,
reject invalid recipes, and validate 100 randomly generated recipes.

For a live test, start the disposable API from `backend/`:

```bash
../.venv/bin/python scripts/browser_test_server.py
```

It migrates a temporary SQLite database, seeds sample gifts, uses fixed test OTP
123456 and a 15-second cooldown, and writes `/tmp/wishy-live-data.json`. In a
second terminal, from `frontend/`, start the proxy:

```bash
API_PROXY_TARGET=http://127.0.0.1:8012 npm run dev -- --port 5175
```

Then, from `frontend/`:

```bash
WISHY_UI_URL=http://127.0.0.1:5175 \
WISHY_LIVE_DATA=/tmp/wishy-live-data.json npm run test:live
```

Restart the disposable API before repeating that scenario to obtain fresh data.
It does not use the development database. SQLite is only used for this UI flow;
PostgreSQL integration tests verify reservation/profile locks and concurrent guest
identity claims.

## Validation and limits

- Architecture dependency and migration-drift checks passed. OpenAPI: 18 YAML files parsed and 40 local references resolved.
- Framework-independent backend suite: 50 tests passed.
- Django API/persistence suite: 192 tests passed on SQLite, with four PostgreSQL-only checks skipped.
- PostgreSQL suite: 192 tests passed, including transaction/locking checks.
- Frontend unit/DOM suite: 32 tests passed; TypeScript and production build passed.
- Layout/accessibility, resize/keyboard and locale-draft suite: 11 browser tests passed on the production bundle, covering the matrix above.
- Final price-entry regression: four browser cases passed. Final keepsake/menu regression: eight cases passed.
- Real API browser scenario passed, including another browser context.

Browser automation uses desktop Chrome with responsive viewports. Safari,
Firefox, actual phone keyboards and physical-device touch behavior were not
verified. Automated accessibility checks do not replace assistive-technology
user testing. All 500 component styles and 250 mixed examples are reviewable;
the much larger space of every possible combination was not exhaustively
visually inspected. Returning engagement and social discussion remain product
hypotheses, not outcomes established by these tests.


## Cat artwork revision after logo review

The original `frontend/public/wishy-cat.jpg` is the visual reference. The old
family/variation size formulas have been replaced by 500 authored designs in
`src/catArtwork.tsx`, with English and Persian names. The default portrait uses
the original purple, golden yellow, broad black eyes, white rims, forehead gem,
small nose and smile. Face contours, folded/curled/tufted ears, lid expressions,
reflections, markings and accessories have different drawings rather than a size
multiplier. The version 1 recipe and its 0–49 indices remain compatible; saved
recipes receive the revised artwork.

Every eye aperture remains large. Pupils clip to the actual selected eye paths,
markings clip to the actual face contour, and the face outline hides the seam at
the ear roots. Reflections are mirrored toward the outer eye corners. Independent
SVG masks and export identifier prefixes prevent one portrait's shape from
changing another portrait in the gallery. Original brand artwork is unchanged.

Visual review covered the 500 individual options in full portraits and 250
balanced mixed portraits, plus the default portrait at 32, 40, 64, 96 and 160px.
`/cat-parts/eye-pairs.html` contains all 2,500 eye/pupil pairings. A browser raster
audit measures both eyes of every pairing: the smallest black proportion was
56.58%, the smallest white proportion was 12.52%, and the smallest visible
black/white aperture contained 2,736 pixels at the 256px art size. These are
composition guards, not a measurement of cuteness or a substitute for user
feedback. The first raster pass exposed a thin white rim; the artwork was fixed
before repeating the audit. Browser accessibility also exposed selected-caption
contrast of 4.46:1; the caption color was darkened.

Run `npm run test:cats` from `frontend/` for the artwork bounds, unique mask IDs,
2,500-pair raster audit and English/Persian studio checks at 320, 390, 768 and
1440px. The studio tests visit every option page in every category, choose models,
check label overflow, undo and accessibility. Review assets regenerate with
`npm run cats:export`.

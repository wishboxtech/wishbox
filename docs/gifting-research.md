# A thoughtful promise, an honest check-in, and a keepsake

Decision date: 2026-10-20. This is a research-informed product decision, not evidence
that this particular interface has already improved real-world gift completion.

## Conclusion

Help the giver turn an intention into a chosen plan. Let the recipient acknowledge
arrival without performing happiness. Keep the recipient's assessment private,
and let them explicitly share either a personal message or a practical request.
Celebrate a confirmed delivery as a completed act of care; never infer satisfaction
from delivery, silence, a private answer, or the absence of a complaint.

## Evidence reviewed and its limits

- **Gollwitzer & Sheeran (2006), Implementation Intentions and Goal Achievement.**
  The review concerns specifying how/when to act, beyond merely wanting an outcome.
  This supports testing a short planning step rather than an instant reservation.
  Wishy's day/next-step prompt is planning-inspired, not a reproduction of a
  standardized if-then intervention. Effects in other tasks do not establish an
  effect size for gifting. [Author's university publication and paper](https://www.socmot.uni-konstanz.de/publications/implementation-intentions-and-goal-achievement-meta-analysis-effects-and-processes).
- **Galak, Givi & Williams (2016), Why Certain Gifts Are Great to Give but Not to Get.**
  This review distinguishes a giver's focus on the exchange from a recipient's
  experience of owning/using the gift. Implication: ask about practical fit after
  arrival and permit a later update; do not treat an immediate delighted reaction
  as the product's success measure. [Journal paper](https://journals.sagepub.com/doi/pdf/10.1177/0963721416656937).
- **Ryan & Deci (2017), Self-Determination Theory.** Reviewed the publisher's
  introductory chapter excerpt, not the entire book. Autonomy, competence and
  relatedness inform the design: a self-chosen plan, visible follow-through, and
  personal connection. This is a framework for design, not a direct experimental
  validation of our date limits or keepsake component.
  [Publisher's chapter](https://www.guilford.com/excerpts/ryan.pdf?t=1).
- **Algoe, Haidt & Gable (2008), Beyond Reciprocity.** Reviewed the research record
  and accessible abstract. The study connects gratitude, perceived responsiveness
  and relationship formation in a particular gift-giving social context. This
  motivates a recipient-authored personal note rather than evaluating a friend.
  The work does not establish that mandatory gratitude or our specific UX improves
  friendships, nor does it establish cultural universality.
  [Research record](https://pubmed.ncbi.nlm.nih.gov/18540759/).
- **Dunn & Norton (2013), Happy Money.** Reviewed the official publisher overview,
  not the full book. Spending on others is one theme of its happiness framework.
  It is useful contextual reading for celebrating meaningful giving, but is not
  used to justify purchase pressure, spending targets, or a claim that any gift
  necessarily makes either participant happy.
  [Publisher's overview](https://www.simonandschuster.com/books/Happy-Money/Elizabeth-Dunn/9781451665086).

No numerical behavioral uplift is claimed. Social obligation, gratitude and
politeness vary with relationships and cultures; the Iranian context especially
needs direct user testing rather than an assumption that Western study samples
transfer unchanged. The private check-in/practical-note separation is our product
inference addressing the user's concern about politeness, not a published finding
about this exact design.

## Implemented experience

1. **A chosen plan.** The giver chooses a target day, an actual next step, and
   confirms checking the wish's details. The modal previews their own plan before
   they reserve. Nickname-only/instant reservations no longer pass server rules.
2. **A hold with an exit.** Target day is today through 30 days ahead. The hold
   ends at UTC midnight two calendar days after that target, covering the chosen
   day across time zones with a buffer. A giver can move it once, to a later day
   at most seven days beyond the original plan. These durations are initial
   product defaults, not values established by the cited papers.
3. **A quiet check-in.** A worker sends one in-app reminder per plan to a registered
   giver; it never exposes the giver's deadline to the owner. Guests see their
   private plan when returning with their management key. Unbought expired holds
   release the wish. Bought gifts do not expire, avoiding duplicate purchases
   during delivery. Cancellation stays available before receipt.
4. **Arrival means arrival.** Only the recipient confirms physical receipt. The
   giver gets a private receipt keepsake and a count of recent gifts received by
   their people. There is no friendship score, spending comparison or public rank.
5. **An honest personal check-in.** The recipient may choose “Fits my wish”,
   “Needs a small change”, “Not right for me”, or “Still trying it”, and keep a
   private note. Nothing is preselected, required, shared or notified. Answers
   can change after using the gift and never alter the giver's keepsake.
6. **A message with explicit audience.** A separate optional message can be shared
   with the giver and withdrawn. A practical note about a size/model is another
   explicit sharing action. It is not generated from the private answer. The giver
   can acknowledge that request; this signals attention, not that the issue is
   resolved. Private dissatisfaction never leaks into notification templates.

The public wish continues to say “Gift received” even when the recipient records
private dissatisfaction. This preserves the truth of arrival without publishing
an assessment of the relationship or falsely asserting happiness.

## Validation and future learning

Technical checks verify authorization, expiry, one-time reminders, concurrent
maintenance, transaction rollback, and absence of private fields in giver/public
responses. DOM tests exercise actual planning, private feedback, explicit sharing,
withdrawal, practical-note acknowledgment and rescheduling.

Behavioral success still requires a consent-based pilot: compare receipt-confirmed
completion within a fixed observation window, expired-hold rate, and whether users
can correctly identify what stays private. Interview recipients about whether the
private choices feel safe and whether practical requests are usable. Compare
cohorts over equivalent elapsed time; don't count recent open reservations as
failures, or present opt-in feedback as representative of silent recipients.
Clicks, shared thank-you frequency and purchase spending alone are insufficient
success metrics. No automated behavioral experiment or external analytics sharing
has been enabled by this implementation.

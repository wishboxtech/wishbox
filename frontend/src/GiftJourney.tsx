import { useLanguage } from "./i18n";
import { useEffect, useState, type FormEvent } from "react";
import {
  CalendarDays,
  Check,
  Gift,
  Heart,
  LockKeyhole,
  MessageCircle,
  Sparkles,
} from "lucide-react";
import { ApiError, request } from "./api";
import { ErrorMessage, Loading } from "./components";
import { giftHeaders, rememberGift } from "./gifting";
import type { GiftExperience, GiftPlan, GiftRecord, Wish } from "./types";

export function localDay(date = new Date()) {
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, "0")}-${String(date.getDate()).padStart(2, "0")}`;
}
function plusDays(days: number, base = localDay()) {
  const date = new Date(`${base}T12:00:00`);
  date.setDate(date.getDate() + days);
  return localDay(date);
}
function dayLabel(day: string, lang: string) {
  return new Intl.DateTimeFormat(lang, {
    month: "short",
    day: "numeric",
  }).format(new Date(`${day}T12:00:00`));
}
function timeLabel(time: string, lang: string) {
  return new Intl.DateTimeFormat(lang, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(time));
}
export function getGiftExperience(
  id: number,
  wishId: string,
  signal?: AbortSignal,
) {
  return request<GiftExperience>(`gifts/${id}/experience/`, {
    headers: giftHeaders(wishId),
    signal,
  });
}

export function CommitmentForm({
  wish,
  signedIn,
  busy,
  reserve,
}: {
  wish: Wish;
  signedIn: boolean;
  busy: boolean;
  reserve: (plan: GiftPlan) => void;
}) {
  const { tr, lang } = useLanguage();
  const [nickname, setNickname] = useState("");
  const [day, setDay] = useState("");
  const [plan, setPlan] = useState("");
  const [checked, setChecked] = useState(false);
  function submit(event: FormEvent) {
    event.preventDefault();
    if (day && plan && checked)
      reserve({
        purchase_by: day,
        purchase_plan: plan,
        details_checked: checked,
        ...(!signedIn ? { nickname: nickname.trim() } : {}),
      });
  }
  return (
    <form className="commitment-form" onSubmit={submit}>
      <div className="commitment-wish">
        <Gift size={24} />
        <div>
          <strong dir="auto">{wish.name}</strong>
          <p>
            {wish.description ||
              tr("Check the exact item, size or model before buying.")}
          </p>
        </div>
      </div>
      <p className="modal-copy">
        {tr(
          "A small plan makes a thoughtful gift happen. Your timing and next step stay private to you.",
        )}
      </p>
      {!signedIn && (
        <label>
          {tr("Your name or nickname")}
          <input
            required
            autoComplete="nickname"
            maxLength={150}
            dir="auto"
            value={nickname}
            onChange={(e) => setNickname(e.target.value)}
          />
          <small>
            {tr(
              "Your private management key stays in this browser. Keep its data to come back to your gift.",
            )}
          </small>
        </label>
      )}
      <fieldset className="plan-fieldset">
        <legend>{tr("When will you arrange the gift?")}</legend>
        <div className="date-shortcuts">
          {[
            { label: tr("Tomorrow"), days: 1 },
            { label: tr("In 3 days"), days: 3 },
            { label: tr("In a week"), days: 7 },
          ].map((option) => (
            <button
              type="button"
              key={option.days}
              aria-pressed={day === plusDays(option.days)}
              className={day === plusDays(option.days) ? "selected" : ""}
              onClick={() => setDay(plusDays(option.days))}
            >
              {option.label}
            </button>
          ))}
        </div>
        <label className="date-label">
          {tr("Or choose a day")}
          <input
            type="date"
            required
            min={localDay()}
            max={plusDays(30)}
            value={day}
            onChange={(e) => setDay(e.target.value)}
          />
          <small>
            {day
              ? dayLabel(day, lang)
              : tr(
                  "Choose a day within 30 days. The date field uses the Gregorian calendar.",
                )}
          </small>
        </label>
      </fieldset>
      <label>
        {tr("My next step")}
        <select required value={plan} onChange={(e) => setPlan(e.target.value)}>
          <option value="">{tr("Choose a real next step")}</option>
          <option value="Order the exact item online">
            {tr("Order the exact item online")}
          </option>
          <option value="Visit a shop and check the details">
            {tr("Visit a shop and check the details")}
          </option>
          <option value="Arrange the gift directly">
            {tr("Arrange the gift directly")}
          </option>
        </select>
      </label>
      <label className="check-label">
        <input
          type="checkbox"
          required
          checked={checked}
          onChange={(e) => setChecked(e.target.checked)}
        />
        <span>
          {tr(
            "I’ve checked the wish details, including any size, model or other important preferences.",
          )}
        </span>
      </label>
      {day && plan && (
        <div className="plan-preview">
          <CalendarDays size={20} />
          <span>
            {tr("I’ll {plan} by {date}.", {
              plan: tr(plan),
              date: dayLabel(day, lang),
            })}
          </span>
        </div>
      )}
      <details className="reservation-details">
        <summary>{tr("Gift details")}</summary>
        <p className="gentle-copy">
          {tr(
            "If plans change, you can release the hold or move the date once. An unbought hold ends automatically after your target day and a short buffer, so the wish won’t stay blocked. Buying and delivery happen outside Wishy.",
          )}
        </p>
      </details>
      <button
        className="button primary full"
        disabled={
          busy || !day || !plan || !checked || (!signedIn && !nickname.trim())
        }
      >
        {busy ? tr("Saving your plan…") : tr("Reserve with this plan")}
        <Check size={19} />
      </button>
    </form>
  );
}

export function GiftJourney({
  wishId,
  reservationId,
  refresh,
  notify,
}: {
  wishId: string;
  reservationId?: number | null;
  refresh: () => void;
  notify: (text: string) => void;
}) {
  const { tr, lang } = useLanguage();
  const [experience, setExperience] = useState<GiftExperience | null>(null);
  const [error, setError] = useState<unknown>(null);
  const [busy, setBusy] = useState(false);
  const [loading, setLoading] = useState(false);
  const [attempt, setAttempt] = useState(0);
  const [fit, setFit] = useState("");
  const [privateNote, setPrivateNote] = useState("");
  const [thanks, setThanks] = useState("");
  const [followUp, setFollowUp] = useState("");
  const [reschedule, setReschedule] = useState(false);
  const [newDay, setNewDay] = useState("");
  useEffect(() => {
    if (!reservationId) return;
    const controller = new AbortController();
    setLoading(true);
    setError(null);
    setExperience(null);
    getGiftExperience(reservationId, wishId, controller.signal)
      .then((result) => {
        if (controller.signal.aborted) return;
        setExperience(result);
        if (result.role === "owner") {
          setFit(result.fit);
          setPrivateNote(result.private_note);
          setThanks(result.thank_you);
          setFollowUp(result.follow_up_note);
        }
      })
      .catch((err) => {
        if (
          !controller.signal.aborted &&
          !(err instanceof ApiError && err.status === 404)
        )
          setError(err);
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false);
      });
    return () => controller.abort();
  }, [reservationId, wishId, attempt]);
  async function save(action: string, extra: Record<string, unknown> = {}) {
    if (!reservationId) return;
    setBusy(true);
    setError(null);
    try {
      const result = await request<GiftExperience>(
        `gifts/${reservationId}/experience/`,
        {
          method: "PATCH",
          body: { action, ...extra },
          headers: giftHeaders(wishId),
        },
      );
      setExperience(result);
      if (action === "withdraw_thanks") setThanks("");
      if (action === "withdraw_follow_up") setFollowUp("");
      notify(
        action === "save_private"
          ? tr("Saved just for you. Nothing was shared with your friend.")
          : action.startsWith("withdraw")
            ? tr("Your shared note has been removed.")
            : action === "acknowledge_follow_up"
              ? tr("Your friend knows you’ve seen their practical note.")
              : tr("Your note was shared only with your friend."),
      );
    } catch (err) {
      setError(err);
    } finally {
      setBusy(false);
    }
  }
  async function moveDate(event: FormEvent) {
    event.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const gift = await request<GiftRecord>(`wish/${wishId}/reservation/`, {
        method: "PATCH",
        body: { action: "reschedule", purchase_by: newDay },
        headers: giftHeaders(wishId),
      });
      rememberGift(gift);
      setReschedule(false);
      notify(tr("Your new plan is saved. One thoughtful step at a time."));
      refresh();
    } catch (err) {
      setError(err);
    } finally {
      setBusy(false);
    }
  }
  if (!reservationId) return null;
  if (loading)
    return (
      <div
        className="journey-loading"
        aria-label={tr("Loading your private gift journey")}
      >
        <Loading />
      </div>
    );
  if (!experience)
    return error ? (
      <div className="journey-panel">
        <ErrorMessage error={error} />
        <button
          className="text-button"
          onClick={() => setAttempt((value) => value + 1)}
        >
          {tr("Try loading your gift again")}
        </button>
      </div>
    ) : null;
  if (experience.role === "giver") {
    const gift = experience.gift;
    return (
      <section
        className={`journey-panel ${gift.status === "received" ? "received-keepsake" : ""}`}
        aria-label={tr("Your private gift journey")}
      >
        {gift.status === "received" ? (
          <>
            <span className="keepsake-cat cat-logo" aria-hidden="true">
              <img src="/wishy-cat.jpg" alt="" />
            </span>
            <span className="eyebrow">
              <Sparkles size={17} />
              {tr("A LITTLE KEEPSAKE")}
            </span>
            <h2>{tr("You followed through.")}</h2>
            <p>
              {tr(
                "Your friend confirmed this gift arrived. A little care, made real.",
              )}
            </p>
            {gift.received_at && (
              <span className="gentle-copy">
                {tr("Received")} {timeLabel(gift.received_at, lang)}
              </span>
            )}
          </>
        ) : gift.status === "reserved" ? (
          <>
            <span className="eyebrow">
              <LockKeyhole size={16} />
              {tr("YOUR PRIVATE PLAN")}
            </span>
            <h2>{tr("A small promise. A real next step.")}</h2>
            <p>
              <strong>{tr(gift.purchase_plan || "")}</strong>
              {gift.purchase_by && (
                <>
                  {" "}
                  {tr("by")} <strong>{dayLabel(gift.purchase_by, lang)}</strong>
                </>
              )}
              .
            </p>
            {gift.expires_at && (
              <p className="gentle-copy">
                {tr("Your hold ends")} {timeLabel(gift.expires_at, lang)}{" "}
                {tr(
                  "if you haven’t marked the gift as bought. This includes a little buffer after your planned day.",
                )}
              </p>
            )}
            <p className="gentle-copy">
              {tr(
                "Only mark it bought once you’ve actually purchased or arranged the gift. You’ll get one gentle in-app check-in if you’re signed in; guests can return here to see their plan.",
              )}
            </p>
            {(gift.extension_count || 0) < 1 &&
              gift.purchase_by &&
              gift.purchase_by < plusDays(30) && (
                <button
                  className="text-button"
                  onClick={() => setReschedule(!reschedule)}
                >
                  {tr("Need a different day?")}
                </button>
              )}
            {reschedule && (
              <form onSubmit={moveDate}>
                <label>
                  {tr("New target day")}
                  <input
                    type="date"
                    required
                    value={newDay}
                    min={
                      gift.purchase_by
                        ? [localDay(), plusDays(1, gift.purchase_by)]
                            .sort()
                            .at(-1)
                        : localDay()
                    }
                    max={
                      gift.purchase_by
                        ? [
                            plusDays(30),
                            plusDays(7, gift.purchase_by),
                          ].sort()[0]
                        : plusDays(7)
                    }
                    onChange={(e) => setNewDay(e.target.value)}
                  />
                  <small>
                    {tr("You can move your plan once, by up to 7 days.")}
                  </small>
                </label>
                <button className="button secondary" disabled={busy || !newDay}>
                  {tr("Save new day")}
                </button>
              </form>
            )}
          </>
        ) : gift.status === "expired" ? (
          <>
            <h2>{tr("This hold has gently ended.")}</h2>
            <p>
              {tr(
                "Plans change. When you’re ready, make a fresh plan if the wish is still available.",
              )}
            </p>
          </>
        ) : gift.status === "cancelled" ? (
          <>
            <h2>{tr("A little room for another plan.")}</h2>
            <p>
              {tr(
                "You released this hold. The wish is free for another friend to pick up.",
              )}
            </p>
          </>
        ) : (
          <>
            <h2>{tr("From your plan to their doorstep.")}</h2>
            <p>
              {tr(
                "You’ve marked the gift as bought. The recipient will confirm when it arrives.",
              )}
            </p>
          </>
        )}
        {gift.thank_you && (
          <div className="shared-note">
            <Heart size={21} />
            <div>
              <strong>{tr("A note from your friend")}</strong>
              <blockquote dir="auto">{gift.thank_you}</blockquote>
              <span>{tr("Shared just with you.")}</span>
            </div>
          </div>
        )}
        {gift.follow_up_note && (
          <div className="shared-note practical-note">
            <MessageCircle size={22} />
            <div>
              <strong>{tr("A practical note from your friend")}</strong>
              <blockquote dir="auto">{gift.follow_up_note}</blockquote>
              {gift.follow_up_acknowledged_at ? (
                <span>
                  {tr(
                    "You’ve seen this. Check in with your friend to work out the details together.",
                  )}
                </span>
              ) : (
                <button
                  className="button secondary"
                  disabled={busy}
                  onClick={() => save("acknowledge_follow_up")}
                >
                  {tr("I’ll check this with you")}
                </button>
              )}
            </div>
          </div>
        )}
        <ErrorMessage error={error} />
      </section>
    );
  }
  if (experience.gift.status !== "received") return null;
  return (
    <section
      className="recipient-experience"
      aria-label={tr("Your gift experience")}
    >
      <div className="journey-panel private-check-in">
        <span className="eyebrow">
          <LockKeyhole size={16} />
          {tr("JUST FOR YOU")}
        </span>
        <h2>{tr("How is it working for you?")}</h2>
        <p>
          {tr(
            "Arrival and a good fit are different things. Your check-in and private note are visible only to you. They don’t change your friend’s keepsake or send them a notification.",
          )}
        </p>
        <form
          aria-label={tr("Private gift check-in")}
          onSubmit={(event) => {
            event.preventDefault();
            save("save_private", {
              fit: fit || null,
              private_note: privateNote,
            });
          }}
        >
          <fieldset className="fit-options">
            <legend>{tr("How does the gift fit your wish?")}</legend>
            {[
              { value: "fits", text: tr("Fits my wish") },
              { value: "adjust", text: tr("Needs a small change") },
              { value: "not_for_me", text: tr("Not right for me") },
              { value: "trying", text: tr("Still trying it") },
            ].map((option) => (
              <label
                key={option.value}
                className={fit === option.value ? "chosen" : ""}
              >
                <input
                  type="radio"
                  name="gift-fit"
                  value={option.value}
                  checked={fit === option.value}
                  onChange={() => setFit(option.value)}
                />
                {option.text}
              </label>
            ))}
          </fieldset>
          <label>
            {tr("A note for future you")}{" "}
            <span className="optional">{tr("(optional)")}</span>
            <textarea
              dir="auto"
              maxLength={800}
              rows={3}
              value={privateNote}
              onChange={(e) => setPrivateNote(e.target.value)}
              placeholder={tr(
                "The size, the model, or what you’d want next time…",
              )}
            />
            <small>
              {tr(
                "You can revisit this after using the gift. There’s no deadline to feel a certain way.",
              )}
            </small>
          </label>
          <button
            className="button secondary"
            disabled={
              busy ||
              (fit === experience.fit &&
                privateNote === experience.private_note)
            }
          >
            <LockKeyhole size={17} />
            {tr("Save just for me")}
          </button>
        </form>
      </div>
      <div className="journey-panel">
        <span className="eyebrow">
          <Heart size={16} />
          {tr("BETWEEN YOU TWO")}
        </span>
        <h2>{tr("A note they can keep.")}</h2>
        <p>
          {tr(
            "If you feel like it, tell your friend what their gift means to you. This is your own message, shared only when you choose.",
          )}
        </p>
        <form
          aria-label={tr("Share a personal note")}
          onSubmit={(event) => {
            event.preventDefault();
            save("share_thanks", { thank_you: thanks.trim() });
          }}
        >
          <label>
            {tr("Your note to your friend")}
            <textarea
              dir="auto"
              value={thanks}
              maxLength={800}
              rows={3}
              onChange={(e) => setThanks(e.target.value)}
              placeholder={tr("What did their gift make possible for you?")}
            />
            <small>
              {tr(
                "Only this message will be shared. Your private check-in stays private.",
              )}
            </small>
          </label>
          <button
            className="button primary"
            disabled={
              busy || !thanks.trim() || thanks.trim() === experience.thank_you
            }
          >
            <Heart size={17} />
            {experience.thank_you
              ? tr("Update shared note")
              : tr("Share this note with my friend")}
          </button>
          {experience.thank_you && (
            <button
              className="text-button withdraw-note"
              type="button"
              disabled={busy}
              onClick={() => save("withdraw_thanks")}
            >
              {tr("Remove shared note")}
            </button>
          )}
        </form>
      </div>
      <details className="journey-panel practical-compose">
        <summary>
          <MessageCircle size={19} />
          {tr("Need to talk about a size, model or other detail?")}
        </summary>
        <p>
          {tr(
            "A practical request can help your friend get it right, without rating them. Share only what you’re comfortable discussing.",
          )}
        </p>
        <form
          aria-label={tr("Share a practical note")}
          onSubmit={(event) => {
            event.preventDefault();
            save("share_follow_up", { follow_up_note: followUp.trim() });
          }}
        >
          <label>
            {tr("Practical note to your friend")}
            <textarea
              dir="auto"
              value={followUp}
              maxLength={800}
              rows={3}
              onChange={(e) => setFollowUp(e.target.value)}
              placeholder={tr("Could we check the size together?")}
            />
            <small>
              {tr(
                "Your friend will see this message. Your private answer above is never included.",
              )}
            </small>
          </label>
          <button
            className="button secondary"
            disabled={
              busy ||
              !followUp.trim() ||
              followUp.trim() === experience.follow_up_note
            }
          >
            {tr("Share this practical note")}
          </button>
          {experience.follow_up_note && (
            <button
              className="text-button withdraw-note"
              type="button"
              disabled={busy}
              onClick={() => save("withdraw_follow_up")}
            >
              {tr("Remove practical note")}
            </button>
          )}
          {experience.follow_up_acknowledged_at && (
            <p className="gentle-copy">
              {tr(
                "Your friend acknowledged this note. You can work out the details together.",
              )}
            </p>
          )}
        </form>
      </details>
      <ErrorMessage error={error} />
    </section>
  );
}

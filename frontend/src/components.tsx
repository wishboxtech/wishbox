import { useEffect, useId, useRef, type ReactNode } from "react";
import {
  AlertCircle,
  ArrowRight,
  Gift,
  LoaderCircle,
  Sparkles,
  X,
} from "lucide-react";
import { ApiError } from "./api";
import { useLanguage, type TranslationKey } from "./i18n";

export function ErrorMessage({ error }: { error: unknown }) {
  const { t, lang } = useLanguage();
  if (!error) return null;
  let key: TranslationKey = "genericError";
  if (error instanceof ApiError) {
    if (error.status === 0) key = "networkError";
    else if (error.status === 401) key = "unauthorized";
    else if (error.status === 403) key = "forbidden";
    else if (error.status === 404) key = "notFound";
    else if (error.codes.includes("VERIFY_OTP_INVALID_OTP")) key = "invalidOtp";
    else if (error.codes.includes("SEND_OTP_OTP_ALREADY_SENT"))
      key = "otpExists";
  } else if (error instanceof Error && error.message === "invalidImage")
    key = "invalidImage";
  return (
    <div className="error-message" role="alert">
      <AlertCircle size={18} />
      <span>
        {lang !== "fa" &&
        error instanceof ApiError &&
        (error.codes.includes("gift_conflict") ||
          error.codes.includes("gift_forbidden") ||
          error.codes.includes("nickname") ||
          error.codes.includes("profile") ||
          error.codes.some((code) =>
            [
              "purchase_by",
              "purchase_plan",
              "details_checked",
              "thank_you",
              "follow_up_note",
              "fit",
            ].includes(code),
          )) &&
        error.details &&
        typeof error.details === "object"
          ? Object.values(error.details)
              .flat()
              .filter((value) => typeof value === "string")
              .join(" ") || t(key)
          : t(key)}
      </span>
    </div>
  );
}

export function Modal({
  title,
  children,
  close,
  wide = false,
}: {
  title: string;
  children: ReactNode;
  close: () => void;
  wide?: boolean;
}) {
  const titleId = useId();
  const ref = useRef<HTMLDivElement>(null);
  const closeRef = useRef(close);
  closeRef.current = close;
  useEffect(() => {
    const previous = document.activeElement as HTMLElement;
    const overflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    const backdrop = ref.current?.closest(".modal-backdrop");
    const siblings: HTMLElement[] = [];
    let current: Element | null = backdrop || null;
    while (current && current !== document.body) {
      siblings.push(
        ...(Array.from(current.parentElement?.children || []).filter(
          (el) => el !== current && el instanceof HTMLElement,
        ) as HTMLElement[]),
      );
      current = current.parentElement;
    }
    const previousInert = siblings.map((el) => el.inert);
    siblings.forEach((el) => {
      el.inert = true;
    });
    ref.current?.focus();
    function keydown(e: KeyboardEvent) {
      if (e.key === "Escape") closeRef.current();
      if (e.key !== "Tab") return;
      const items = ref.current?.querySelectorAll<HTMLElement>(
        'button:not(:disabled), input:not(:disabled), select:not(:disabled), textarea:not(:disabled), a[href], [tabindex="0"]',
      );
      if (!items?.length) {
        e.preventDefault();
        return;
      }
      const first = items[0],
        last = items[items.length - 1];
      if (
        e.shiftKey &&
        (document.activeElement === first ||
          document.activeElement === ref.current)
      ) {
        e.preventDefault();
        last.focus();
      } else if (
        !e.shiftKey &&
        (document.activeElement === last ||
          document.activeElement === ref.current)
      ) {
        e.preventDefault();
        first.focus();
      }
    }
    document.addEventListener("keydown", keydown);
    return () => {
      siblings.forEach((el, i) => {
        el.inert = previousInert[i];
      });
      document.body.style.overflow = overflow;
      document.removeEventListener("keydown", keydown);
      previous?.focus();
    };
  }, []);
  const { t, lang } = useLanguage();
  return (
    <div
      className="modal-backdrop"
      onClick={(e) => {
        if (e.target === e.currentTarget) close();
      }}
    >
      <div
        className={`modal ${wide ? "modal-wide" : ""}`}
        role="dialog"
        aria-modal="true"
        aria-labelledby={titleId}
        tabIndex={-1}
        ref={ref}
      >
        <div className="modal-heading">
          <h2 id={titleId}>{title}</h2>
          <button
            className="icon-button"
            onClick={close}
            aria-label={t("close")}
          >
            <X size={21} />
          </button>
        </div>
        <div className="modal-body">{children}</div>
      </div>
    </div>
  );
}

export function Loading() {
  const { t, lang } = useLanguage();
  return (
    <div className="loading" role="status">
      <LoaderCircle className="spin" size={26} />
      <p>{t("loading")}</p>
    </div>
  );
}

export function Empty({
  title,
  copy,
  action,
  label,
}: {
  title: string;
  copy: string;
  action?: () => void;
  label?: string;
}) {
  return (
    <div className="empty-state">
      <div className="empty-icon">
        <Gift size={31} strokeWidth={1.5} />
        <Sparkles className="tiny-spark" size={17} />
      </div>
      <h2>{title}</h2>
      <p>{copy}</p>
      {action && (
        <button className="button primary" onClick={action}>
          {label}
          <ArrowRight size={17} className="directional" />
        </button>
      )}
    </div>
  );
}

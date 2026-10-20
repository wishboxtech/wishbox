import { useEffect, useRef, useState, type FormEvent } from "react";
import {
  ArrowRight,
  Check,
  ImagePlus,
  LoaderCircle,
  ShieldCheck,
} from "lucide-react";
import { mediaUrl, request, session, upload } from "./api";
import {
  canClaimGuest,
  guestKey,
  finishGuestClaim,
  finishGuestDecision,
} from "./gifting";
import { ErrorMessage, Modal } from "./components";
import { useLanguage } from "./i18n";
import type { Collection, Tokens, Wish } from "./types";

const asciiDigits = (value: string) =>
  value.replace(/[۰-۹٠-٩]/g, (digit) =>
    String(
      "۰۱۲۳۴۵۶۷۸۹".includes(digit)
        ? "۰۱۲۳۴۵۶۷۸۹".indexOf(digit)
        : "٠١٢٣٤٥٦٧٨٩".indexOf(digit),
    ),
  );

export function ImageField({
  label,
  onChange,
  existing,
  onRemove,
}: {
  label: string;
  onChange: (file: File | null) => void;
  existing?: string;
  onRemove?: () => void;
}) {
  const { t } = useLanguage();
  const [filename, setFilename] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string>();
  const fileInput = useRef<HTMLInputElement>(null);
  useEffect(() => {
    if (!selectedFile) {
      setPreview(undefined);
      return;
    }
    const url = URL.createObjectURL(selectedFile);
    setPreview(url);
    return () => URL.revokeObjectURL(url);
  }, [selectedFile]);
  const [error, setError] = useState<unknown>(null);
  return (
    <div className="image-field">
      <span className="field-label">{label}</span>
      {(preview || existing) && (
        <img
          className="upload-preview"
          src={preview || mediaUrl(existing)}
          alt={label}
        />
      )}
      <label className="upload-zone">
        <ImagePlus size={24} />
        <span>{filename || t("chooseImage")}</span>
        <small>{t("imageHint")}</small>
        <input
          ref={fileInput}
          aria-label={label}
          type="file"
          accept="image/png,image/jpeg,image/webp,image/gif"
          onChange={(e) => {
            const file = e.target.files?.[0] || null;
            if (
              file &&
              (!["image/png", "image/jpeg", "image/webp", "image/gif"].includes(
                file.type,
              ) ||
                file.size > 10 * 1024 * 1024)
            ) {
              setError(new Error("invalidImage"));
              e.target.value = "";
              return;
            }
            setError(null);
            setFilename(file?.name || "");
            setSelectedFile(file);
            onChange(file);
          }}
        />
      </label>
      {(existing || filename) && (
        <button
          className="text-button danger-text"
          type="button"
          onClick={() => {
            onRemove?.();
            setSelectedFile(null);
            if (fileInput.current) fileInput.current.value = "";
            setFilename("");
            onChange(null);
          }}
        >
          {t("removeImage")}
        </button>
      )}
      <ErrorMessage error={error} />
    </div>
  );
}

export function AuthModal({
  close,
  complete,
}: {
  close: () => void;
  complete: () => void;
}) {
  const { tr } = useLanguage();
  const { t } = useLanguage();
  const [phone, setPhone] = useState("");
  const [linkGuest, setLinkGuest] = useState(false);
  const [claimAvailable] = useState(canClaimGuest);
  const [otpId, setOtpId] = useState("");
  const [code, setCode] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<unknown>(null);
  async function submit(e: FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      if (!otpId) {
        const result = await request<{ otp_id: string }>("auth/otp/", {
          method: "POST",
          public: true,
          body: { phone_number: phone },
        });
        setOtpId(result.otp_id);
      } else {
        const tokens = await request<Tokens>("auth/otp/verify/", {
          method: "POST",
          public: true,
          body: {
            otp_id: otpId,
            otp_code: code,
            ...(claimAvailable && linkGuest ? { guest_key: guestKey() } : {}),
          },
        });
        if (tokens.guest_claimed) finishGuestClaim();
        else if (claimAvailable) finishGuestDecision();
        session.set(tokens);
        complete();
      }
    } catch (err) {
      setError(err);
    } finally {
      setBusy(false);
    }
  }
  return (
    <Modal title={t("loginTitle")} close={close}>
      <p className="modal-copy">{t("loginCopy")}</p>
      <form onSubmit={submit}>
        {!otpId ? (
          <label>
            {t("phone")}
            <input
              type="tel"
              dir="ltr"
              autoComplete="tel-national"
              required
              pattern="09[0-9]{9}"
              placeholder="09123456789"
              value={phone}
              onChange={(e) => setPhone(asciiDigits(e.target.value))}
            />
            <small>{t("phoneHint")}</small>
          </label>
        ) : (
          <>
            <p className="muted">
              {t("codeSent")} <b dir="ltr">{phone}</b>
            </p>
            <label>
              {t("code")}
              <input
                className="otp-input"
                dir="ltr"
                inputMode="numeric"
                pattern="[0-9]{6}"
                autoComplete="one-time-code"
                maxLength={6}
                required
                value={code}
                onChange={(e) => setCode(asciiDigits(e.target.value))}
                placeholder="• • • • • •"
              />
            </label>
            <button
              type="button"
              className="text-button"
              disabled={busy}
              onClick={() => {
                setOtpId("");
                setCode("");
                setError(null);
              }}
            >
              {t("changeNumber")}
            </button>
          </>
        )}
        {claimAvailable && (
          <label className="check-label guest-claim-choice">
            <input
              type="checkbox"
              checked={linkGuest}
              onChange={(e) => setLinkGuest(e.target.checked)}
            />
            <span>
              {tr(
                "These guest gifts are mine. Add them if I’m creating my first account.",
              )}
              <small>
                {tr(
                  "This happens once, only at signup. Signing in to an existing account keeps guest gifts separate.",
                )}
              </small>
            </span>
          </label>
        )}
        {import.meta.env?.DEV && (
          <div className="notice">
            <ShieldCheck size={20} />
            {t("localCode")}
          </div>
        )}
        <ErrorMessage error={error} />
        <button className="button primary full" disabled={busy}>
          {busy ? (
            <LoaderCircle className="spin" size={18} />
          ) : (
            <>
              {t(otpId ? "verify" : "sendCode")}
              <ArrowRight size={17} className="directional" />
            </>
          )}
        </button>
      </form>
    </Modal>
  );
}

export function ResourceForm({
  kind,
  item,
  listId,
  close,
  complete,
}: {
  kind: "list" | "wish";
  item?: Collection | Wish;
  listId?: string;
  close: () => void;
  complete: (result: Collection | Wish) => void;
}) {
  const { tr } = useLanguage();
  const { t } = useLanguage();
  const [name, setName] = useState(item?.name || "");
  const [description, setDescription] = useState(item?.description || "");
  const [price, setPrice] = useState(item && "price" in item ? item.price : "");
  const [file, setFile] = useState<File | null>(null);
  const [removeCover, setRemoveCover] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<unknown>(null);
  const title = t(
    kind === "list"
      ? item
        ? "editList"
        : "newList"
      : item
        ? "editWish"
        : "addWish",
  );
  async function submit(e: FormEvent) {
    e.preventDefault();
    setBusy(true);
    setError(null);
    try {
      const cover = file ? await upload(file) : removeCover ? null : undefined;
      const body = {
        name: name.trim(),
        description: description.trim(),
        ...(kind === "wish" ? { price } : {}),
        ...(cover !== undefined ? { cover } : {}),
      };
      const path =
        kind === "list"
          ? item
            ? `wishlist/${item.id}/`
            : "profile/wishlist/"
          : item
            ? `wishlist/${listId}/wish/${item.id}/`
            : `wishlist/${listId}/`;
      const result = await request<Collection | Wish>(path, {
        method: item ? "PATCH" : "POST",
        body,
      });
      complete(result);
    } catch (err) {
      setError(err);
    } finally {
      setBusy(false);
    }
  }
  return (
    <Modal title={title} close={close}>
      <form onSubmit={submit}>
        <label>
          {t("name")}
          <input
            required
            maxLength={150}
            dir="auto"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder={t(
              kind === "list" ? "listNamePlaceholder" : "wishNamePlaceholder",
            )}
          />
        </label>
        <label>
          {t("description")}{" "}
          <span className="optional">{tr("(optional)")}</span>
          <textarea
            dir="auto"
            rows={3}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder={t("descriptionPlaceholder")}
          />
        </label>
        {kind === "wish" && (
          <label>
            {t("price")}
            <input
              required
              name="price"
              type="text"
              inputMode="numeric"
              pattern="[0-9]{1,10}"
              dir="ltr"
              value={price}
              onChange={(e) =>
                setPrice(asciiDigits(e.target.value).replace(/[,٬\s]/g, ""))
              }
            />
            <small>{t("priceHint")}</small>
          </label>
        )}
        <ImageField
          label={t("cover")}
          onChange={setFile}
          existing={removeCover ? undefined : item?.cover?.file}
          onRemove={() => setRemoveCover(true)}
        />
        <ErrorMessage error={error} />
        <div className="form-actions">
          <button type="button" className="button secondary" onClick={close}>
            {t("cancel")}
          </button>
          <button className="button primary" disabled={busy || !name.trim()}>
            {busy ? (
              <LoaderCircle size={18} className="spin" />
            ) : (
              <Check size={17} />
            )}
            {t(item ? "save" : kind === "list" ? "create" : "createWish")}
          </button>
        </div>
      </form>
    </Modal>
  );
}

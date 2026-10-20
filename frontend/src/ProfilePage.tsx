import { useLanguage } from "./i18n";
import { useState, type FormEvent } from "react";
import { request, upload } from "./api";
import { ErrorMessage } from "./components";
import { ImageField } from "./forms";
import { CatAvatar } from "./CatAvatar";
import { CatBuilder } from "./CatBuilder";
import { defaultCat, type CatRecipe } from "./cat";
import { mediaUrl } from "./api";
import type { Profile } from "./types";

export function ProfilePage({
  profile,
  complete,
  notify,
}: {
  profile: Profile | null;
  complete: (p: Profile) => void;
  notify: (s: string) => void;
}) {
  const { tr } = useLanguage();
  const [cat, setCat] = useState<CatRecipe | null>(profile?.cat_avatar || null);
  const [building, setBuilding] = useState(false);
  const [usePhoto, setUsePhoto] = useState(
    !!profile?.photo && !profile?.cat_avatar,
  );
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<unknown>(null);
  const [file, setFile] = useState<File | null>(null);
  const [removePhoto, setRemovePhoto] = useState(false);
  async function submit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setBusy(true);
    setError(null);
    const data = new FormData(e.currentTarget);
    try {
      const photo = file ? await upload(file) : removePhoto ? null : undefined;
      const result = await request<Profile>("profile/", {
        method: "PUT",
        body: {
          first_name: data.get("first_name"),
          last_name: data.get("last_name"),
          bio: data.get("bio"),
          cat_avatar: usePhoto ? null : cat || defaultCat,
          ...(photo !== undefined ? { photo } : {}),
        },
      });
      complete(result);
      notify(tr("Your profile is saved."));
    } catch (err) {
      setError(err);
    } finally {
      setBusy(false);
    }
  }
  return (
    <section className="narrow">
      <div className="page-heading">
        <span className="eyebrow">{tr("YOUR LITTLE CORNER")}</span>
        <h1>{profile ? tr("Your profile") : tr("What should we call you?")}</h1>
        <p>
          {profile
            ? tr("A familiar face for your friends.")
            : tr("Add your name, then make your first wishlist.")}
        </p>
      </div>
      <form className="panel profile-form" onSubmit={submit}>
        <div className="profile-cat-card">
          {usePhoto && profile?.photo && !removePhoto ? (
            <img
              className="profile-photo-preview"
              src={mediaUrl(profile.photo.file)}
              alt={tr("Profile picture")}
            />
          ) : (
            <CatAvatar
              recipe={cat || defaultCat}
              label={tr("Your Wishy cat")}
            />
          )}
          <div>
            <h2>{tr("Your Wishy cat")}</h2>
            <p>{tr("Your cat is ready to meet your friends.")}</p>
            <button
              className="button secondary"
              type="button"
              onClick={() => setBuilding(true)}
            >
              {tr(cat ? "Change my cat" : "Make your cat")}
            </button>
          </div>
        </div>
        <button
          type="button"
          className="text-button picture-mode-toggle"
          onClick={() => setUsePhoto(!usePhoto)}
        >
          {tr(usePhoto ? "Use my cat instead" : "Use a photo instead")}
        </button>
        <div className="form-row">
          <label>
            {tr("First name")}
            <input
              dir="auto"
              name="first_name"
              required
              maxLength={150}
              defaultValue={profile?.first_name || ""}
              autoComplete="given-name"
            />
          </label>
          <label>
            {tr("Last name")}{" "}
            <span className="optional">{tr("(optional)")}</span>
            <input
              dir="auto"
              name="last_name"
              maxLength={150}
              defaultValue={profile?.last_name || ""}
              autoComplete="family-name"
            />
          </label>
        </div>
        <label>
          {tr("A little about you")}{" "}
          <span className="optional">{tr("(optional)")}</span>
          <textarea
            dir="auto"
            name="bio"
            maxLength={250}
            rows={3}
            defaultValue={profile?.bio || ""}
          />
        </label>
        {usePhoto && (
          <ImageField
            label={tr("Profile photo (optional)")}
            onChange={setFile}
            existing={removePhoto ? undefined : profile?.photo?.file}
            onRemove={() => setRemovePhoto(true)}
          />
        )}
        <ErrorMessage error={error} />
        <button className="button primary" disabled={busy}>
          {busy
            ? tr("Saving…")
            : profile
              ? tr("Save profile")
              : tr("Start wishing")}
        </button>
      </form>
      {building && (
        <CatBuilder
          initial={cat}
          close={() => setBuilding(false)}
          choose={(value) => {
            setCat(value);
            setUsePhoto(false);
            setBuilding(false);
            notify(tr("Cat selected. Save your profile to keep it."));
          }}
        />
      )}
    </section>
  );
}

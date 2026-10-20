import { useState } from "react";
import { ArrowLeft, ArrowRight, Check, Shuffle, Undo2 } from "lucide-react";
import { Modal } from "./components";
import { CatAvatar } from "./CatAvatar";
import {
  catParts,
  catCatalog,
  catBackgrounds,
  defaultCat,
  furColors,
  partLabels,
  randomCat,
  type CatPart,
  type CatRecipe,
} from "./cat";
import { useLanguage } from "./i18n";

export function CatBuilder({
  initial,
  close,
  choose,
}: {
  initial?: CatRecipe | null;
  close: () => void;
  choose: (cat: CatRecipe) => void;
}) {
  const { tr, lang } = useLanguage();
  const [cat, setCat] = useState<CatRecipe>(initial || defaultCat);
  const [history, setHistory] = useState<CatRecipe[]>([]);
  const [part, setPart] = useState<CatPart>("face");
  const [page, setPage] = useState(Math.floor((initial?.face || 0) / 10));
  const number = (n: number) => new Intl.NumberFormat(lang).format(n);
  function update(next: CatRecipe) {
    setHistory((h) => [...h.slice(-29), cat]);
    setCat(next);
  }
  return (
    <Modal title={tr("Make your cat")} close={close} wide>
      <div className="cat-studio">
        <div className="cat-preview-panel">
          <div className="cat-live-preview">
            <CatAvatar recipe={cat} label={tr("Your Wishy cat")} />
            <span className="cat-preview-spark" aria-hidden="true">
              ✦
            </span>
          </div>
          <div>
            <h3>{tr("A little like you. Entirely a cat.")}</h3>
            <p>
              {tr("50 styles for every detail. Mix, match, make it yours.")}
            </p>
          </div>
          <div className="cat-random-actions">
            <button
              type="button"
              className="button secondary"
              onClick={() => update(randomCat())}
            >
              <Shuffle size={17} />
              {tr("Surprise me")}
            </button>
            <button
              type="button"
              className="icon-button"
              aria-label={tr("Undo")}
              disabled={!history.length}
              onClick={() => {
                setCat(history[history.length - 1]);
                setHistory((h) => h.slice(0, -1));
              }}
            >
              <Undo2 size={19} />
            </button>
          </div>
        </div>
        <div className="cat-options-panel">
          <div
            className="cat-part-tabs"
            role="group"
            aria-label={tr("Your Wishy cat")}
          >
            {catParts.map((p) => (
              <button
                type="button"
                key={p}
                aria-pressed={part === p}
                className={part === p ? "selected" : ""}
                onClick={() => {
                  setPart(p);
                  setPage(Math.floor(cat[p] / 10));
                }}
              >
                {tr(partLabels[p])}
              </button>
            ))}
          </div>
          <div className="cat-variant-heading">
            <strong>{tr(partLabels[part])}</strong>
            <span>
              {number(50)} {lang === "fa" ? "مدل" : "styles"}
            </span>
          </div>
          <div
            className="cat-variant-grid"
            role="group"
            aria-label={tr(partLabels[part])}
          >
            {catCatalog[part]
              .slice(page * 10, page * 10 + 10)
              .map(({ id, key, name, fa }) => (
                <button
                  type="button"
                  key={key}
                  title={lang === "fa" ? fa : name}
                  aria-description={lang === "fa" ? fa : name}
                  aria-label={tr("{part}, style {number}", {
                    part: tr(partLabels[part]),
                    number: number(id + 1),
                  })}
                  aria-pressed={cat[part] === id}
                  className={cat[part] === id ? "selected" : ""}
                  onClick={() => update({ ...cat, [part]: id })}
                >
                  <CatAvatar recipe={{ ...cat, [part]: id }} />
                  <span className="cat-style-name">
                    {lang === "fa" ? fa : name}
                  </span>
                  {cat[part] === id && (
                    <Check className="cat-selected-check" size={15} />
                  )}
                </button>
              ))}
          </div>
          <div className="cat-pagination">
            <button
              type="button"
              className="icon-button"
              disabled={page === 0}
              aria-label={tr("Previous styles")}
              onClick={() => setPage((p) => p - 1)}
            >
              <ArrowLeft className="directional" size={18} />
            </button>
            <span>
              {tr("Page {page} of {total}", {
                page: number(page + 1),
                total: number(5),
              })}
            </span>
            <button
              type="button"
              className="icon-button"
              disabled={page === 4}
              aria-label={tr("Next styles")}
              onClick={() => setPage((p) => p + 1)}
            >
              <ArrowRight className="directional" size={18} />
            </button>
          </div>
          <fieldset className="cat-color-field">
            <legend>{tr("Fur color")}</legend>
            <div className="cat-colors">
              {furColors.map((color, i) => (
                <button
                  type="button"
                  key={color}
                  style={{ background: color }}
                  aria-label={`${tr("Fur color")} ${number(i + 1)}`}
                  aria-pressed={cat.fur === i}
                  onClick={() => update({ ...cat, fur: i })}
                >
                  {cat.fur === i && <Check size={17} />}
                </button>
              ))}
            </div>
          </fieldset>
          <fieldset className="cat-color-field">
            <legend>{tr("Background color")}</legend>
            <div className="cat-colors">
              {catBackgrounds.map((color, i) => (
                <button
                  type="button"
                  key={color}
                  style={{ background: color }}
                  aria-label={`${tr("Background color")} ${number(i + 1)}`}
                  aria-pressed={cat.background === i}
                  onClick={() => update({ ...cat, background: i })}
                >
                  {cat.background === i && <Check size={17} />}
                </button>
              ))}
            </div>
          </fieldset>
        </div>
      </div>
      <div className="studio-actions">
        <button type="button" className="button secondary" onClick={close}>
          {tr("Cancel")}
        </button>
        <button
          type="button"
          className="button primary"
          onClick={() => choose(cat)}
        >
          <Check size={18} />
          {tr("Use this cat")}
        </button>
      </div>
    </Modal>
  );
}

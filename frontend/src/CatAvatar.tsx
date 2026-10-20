import { useId } from "react";
import {
  catBackgrounds,
  defaultCat,
  furColors,
  validCat,
  type CatPart,
  type CatRecipe,
} from "./cat";
import {
  catArtwork,
  catInk,
  faceDesigns,
  EyeMask,
  EyeShapes,
} from "./catArtwork";

export function CatLayer({
  part,
  value,
  fur,
  clipId,
}: {
  part: CatPart;
  value: number;
  fur: string;
  clipId?: string;
}) {
  const design = catArtwork[part][value] || catArtwork[part][0];
  return (
    <g
      data-cat-layer={`${part}-${value + 1}`}
      data-cat-style={design.name}
      style={{ color: fur }}
      clipPath={clipId ? `url(#${clipId})` : undefined}
    >
      {design.art}
    </g>
  );
}
export function CatAvatar({
  recipe = defaultCat,
  label,
  className = "",
}: {
  recipe?: CatRecipe | null;
  label?: string;
  className?: string;
}) {
  const id = `cat-${useId().replace(/[^a-zA-Z0-9_-]/g, "")}`;
  const r = validCat(recipe) ? recipe : defaultCat;
  const fur = furColors[r.fur];
  return (
    <svg
      className={`cat-avatar ${className}`}
      data-cat-portrait="logo-v2"
      viewBox="0 0 256 256"
      role={label ? "img" : undefined}
      aria-label={label}
      aria-hidden={label ? undefined : true}
      xmlns="http://www.w3.org/2000/svg"
    >
      <defs>
        <clipPath id={`${id}-face`}>
          <path d={faceDesigns[r.face].outline} />
        </clipPath>
        <clipPath id={`${id}-eyes`}>
          <EyeMask value={r.eyes} />
        </clipPath>
      </defs>
      <rect
        width="256"
        height="256"
        rx="64"
        fill={catBackgrounds[r.background]}
      />
      <ellipse cx="128" cy="240" rx="61" ry="5" fill={catInk} opacity=".06" />
      <CatLayer part="ears" value={r.ears} fur={fur} />
      <CatLayer part="face" value={r.face} fur={fur} />
      <CatLayer
        part="markings"
        value={r.markings}
        fur={fur}
        clipId={`${id}-face`}
      />
      <CatLayer part="brows" value={r.brows} fur={fur} />
      <CatLayer part="eyes" value={r.eyes} fur={fur} />
      <CatLayer
        part="pupils"
        value={r.pupils}
        fur={fur}
        clipId={`${id}-eyes`}
      />
      <EyeShapes value={r.eyes} outlineOnly />
      <CatLayer part="nose" value={r.nose} fur={fur} />
      <CatLayer part="mouth" value={r.mouth} fur={fur} />
      <CatLayer part="whiskers" value={r.whiskers} fur={fur} />
      <CatLayer part="accessories" value={r.accessories} fur={fur} />
    </svg>
  );
}

import { catArtwork } from "./catArtwork";

export const catParts = [
  "face",
  "ears",
  "eyes",
  "pupils",
  "brows",
  "nose",
  "mouth",
  "whiskers",
  "markings",
  "accessories",
] as const;
export type CatPart = (typeof catParts)[number];
export type CatRecipe = Record<CatPart, number> & {
  version: 1;
  fur: number;
  background: number;
};
export const defaultCat: CatRecipe = {
  version: 1,
  face: 0,
  ears: 0,
  eyes: 0,
  pupils: 0,
  brows: 0,
  nose: 0,
  mouth: 0,
  whiskers: 0,
  markings: 0,
  accessories: 0,
  fur: 0,
  background: 0,
};
export const furColors = [
  "#5328b8",
  "#f3bd78",
  "#e8ddcf",
  "#556278",
  "#c88564",
  "#f4cfb9",
  "#9e89cb",
  "#ded4c9",
  "#ad7654",
  "#818ea2",
  "#cba29e",
  "#b5b8a0",
  "#f2c6d5",
  "#927e78",
  "#e9c6a0",
  "#c2b5e0",
];
export const catBackgrounds = [
  "#f8bb06",
  "#ebe3f8",
  "#dfefea",
  "#f7ddd9",
  "#deebf6",
  "#f5e4cf",
  "#e5e6f5",
  "#e4efd8",
  "#f5e4ef",
  "#e2f1ef",
  "#eee9e2",
  "#e5d5f1",
];
export const partLabels: Record<CatPart, string> = {
  face: "Face",
  ears: "Ears",
  eyes: "Eyes",
  pupils: "Pupils",
  brows: "Brows",
  nose: "Nose",
  mouth: "Smile",
  whiskers: "Whiskers",
  markings: "Markings",
  accessories: "Accessories",
};
export const catCatalog = Object.fromEntries(
  catParts.map((part) => [
    part,
    catArtwork[part].map(({ name, fa }, id) => ({
      id,
      name,
      fa,
      key: `${part}-${String(id + 1).padStart(2, "0")}`,
    })),
  ]),
) as Record<CatPart, { id: number; name: string; fa: string; key: string }[]>;
export function validCat(value: unknown): value is CatRecipe {
  if (!value || typeof value !== "object") return false;
  const r = value as CatRecipe;
  return (
    r.version === 1 &&
    catParts.every((p) => Number.isInteger(r[p]) && r[p] >= 0 && r[p] < 50) &&
    Number.isInteger(r.fur) &&
    r.fur >= 0 &&
    r.fur < 16 &&
    Number.isInteger(r.background) &&
    r.background >= 0 &&
    r.background < 12
  );
}
export function randomCat(): CatRecipe {
  const random = (n: number) =>
    crypto.getRandomValues(new Uint32Array(1))[0] % n;
  return {
    ...defaultCat,
    ...Object.fromEntries(catParts.map((p) => [p, random(50)])),
    fur: random(16),
    background: random(12),
  };
}

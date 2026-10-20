import React from "react";
import { mkdir, writeFile } from "node:fs/promises";
import { renderToStaticMarkup } from "react-dom/server";
import { CatLayer, CatAvatar } from "../src/CatAvatar";
import { catParts, catCatalog, defaultCat, furColors } from "../src/cat";

const root = new URL("../public/cat-parts/", import.meta.url);
await mkdir(root, { recursive: true });
for (const part of catParts) {
  await mkdir(new URL(`${part}/`, root), { recursive: true });
  for (const item of catCatalog[part]) {
    const svg = renderToStaticMarkup(
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">
        <CatLayer part={part} value={item.id} fur={furColors[0]} />
      </svg>,
    );
    await writeFile(new URL(`${part}/${item.key}.svg`, root), svg + "\n");
  }
}
await writeFile(
  new URL("catalog.json", root),
  JSON.stringify(
    {
      version: 1,
      artwork: "logo-v2",
      viewBox: "0 0 256 256",
      parts: catCatalog,
    },
    null,
    2,
  ) + "\n",
);
const portrait = (recipe: typeof defaultCat, prefix: string) =>
  renderToStaticMarkup(<CatAvatar recipe={recipe} />, {
    identifierPrefix: prefix,
  });
const css = `body{font:16px system-ui;background:#fbfaf7;color:#282333;margin:32px}h1{color:#542abd}.grid{display:grid;grid-template-columns:repeat(10,minmax(0,1fr));gap:18px 12px}figure{margin:0;text-align:center}svg{width:100%;height:auto}figcaption{font-size:11px;min-height:30px}section{break-after:page;margin-bottom:42px}.reference{display:flex;align-items:center;gap:32px}.reference img,.reference svg{width:256px;height:256px}.reference img{object-fit:cover;object-position:center}a{color:#542abd}.sizes{display:flex;align-items:center;gap:24px;margin-block:24px}.sizes svg{width:var(--size);height:var(--size)}`;
const doc = (title: string, body: string) =>
  `<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>${title}</title><style>${css}</style><h1>${title}</h1>${body}</html>`;
const sheet = catParts
  .map(
    (part) =>
      `<section data-part="${part}"><h2>${part} · 50 authored designs</h2><div class="grid">${catCatalog[part].map(({ id, name }) => `<figure data-style="${part}-${id}">${portrait({ ...defaultCat, [part]: id }, `${part}-${id}-`)}<figcaption>${id + 1} · ${name}</figcaption></figure>`).join("")}</div></section>`,
  )
  .join("");
await writeFile(
  new URL("review.html", root),
  doc(
    "Wishy · logo-based cat studio",
    `<p>500 authored options. Fixed large-eye proportions, shared facial anchors and clipped eye interiors.</p><p><a href="samples.html">250 mixed portraits</a> · <a href="eye-pairs.html">All 2,500 eye / pupil pairs</a></p><div class="reference"><figure><img src="../wishy-cat.jpg" alt="Original Wishy logo"><figcaption>Original logo (full artwork)</figcaption></figure><figure>${portrait(defaultCat, "reference-")}<figcaption>New default portrait</figcaption></figure></div><div class="sizes">${[32, 40, 64, 96, 160].map((size) => `<figure style="--size:${size}px">${portrait(defaultCat, `size-${size}-`)}<figcaption>${size}px</figcaption></figure>`).join("")}</div>${sheet}`,
  ),
);
// Each part appears five times across this balanced sample; use a different
// coprime stride and permutation per part instead of low bits from an LCG.
const samples = Array.from({ length: 250 }, (_, i) => {
  const recipe = {
    ...defaultCat,
    ...Object.fromEntries(
      catParts.map((part, j) => [
        part,
        (i * [1, 3, 7, 9, 11, 13, 17, 19, 21, 23][j] +
          j * 7 +
          Math.floor(i / 50) * [3, 7, 11, 17, 19, 23, 29, 31, 37, 41][j]) %
          50,
      ]),
    ),
    fur: i % 16,
    background: (Math.floor(i / 16) + i) % 12,
  };
  return `<figure data-sample="${i}">${portrait(recipe, `mix-${i}-`)}<figcaption>${i + 1}</figcaption></figure>`;
}).join("");
await writeFile(
  new URL("samples.html", root),
  doc("Wishy · 250 balanced mixed cats", `<div class="grid">${samples}</div>`),
);
const pairs = catCatalog.eyes
  .map(
    ({ id, name }) =>
      `<section data-eye="${id}"><h2>${id + 1} · ${name}</h2><div class="grid">${catCatalog.pupils.map(({ id: pupil, name }) => `<figure>${portrait({ ...defaultCat, eyes: id, pupils: pupil }, `pair-${id}-${pupil}-`)}<figcaption>${name}</figcaption></figure>`).join("")}</div></section>`,
  )
  .join("");
await writeFile(
  new URL("eye-pairs.html", root),
  doc("Wishy · all eye and pupil pairings", pairs),
);
console.log(
  "Exported 500 layers, 500-style review, 250 mixed portraits and 2,500 eye/pupil pairings.",
);

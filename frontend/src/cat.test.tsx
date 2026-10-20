import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { renderToStaticMarkup } from "react-dom/server";
import { CatAvatar, CatLayer } from "./CatAvatar";
import { catParts, defaultCat, catCatalog, randomCat, validCat } from "./cat";

describe("composable Wishy cats", () => {
  it("has 50 geometrically distinct layers for each of its ten parts", () => {
    assert.equal(catParts.length, 10);
    for (const part of catParts) {
      assert.equal(catCatalog[part].length, 50);
      assert.equal(new Set(catCatalog[part].map((item) => item.name)).size, 50);
      assert.equal(new Set(catCatalog[part].map((item) => item.fa)).size, 50);
      const shapes = catCatalog[part].map(({ id }) =>
        renderToStaticMarkup(
          <svg>
            <CatLayer part={part} value={id} fur="#5328b8" />
          </svg>,
        ).replace(/data-cat-(?:layer|style)="[^"]+"/g, ""),
      );
      assert.equal(
        new Set(shapes).size,
        50,
        `${part} variants must have distinct geometry`,
      );
      assert.ok(
        shapes.every((s) => !s.includes("NaN") && !s.includes("undefined")),
      );
    }
  });
  it("clips markings to the face and pupils to actual eye apertures", () => {
    for (let eyes = 0; eyes < 50; eyes++) {
      const html = renderToStaticMarkup(
        <CatAvatar recipe={{ ...defaultCat, eyes }} />,
      );
      assert.match(
        html,
        /data-cat-layer="pupils-1"[^>]*clip-path="url\(#cat-[^)]+-eyes\)"/,
      );
      assert.match(
        html,
        /data-cat-layer="markings-1"[^>]*clip-path="url\(#cat-[^)]+-face\)"/,
      );
      assert.equal((html.match(/data-eye-apertures="large"/g) || []).length, 2);
      assert.ok(
        !html.includes("scale(0."),
        "eye size must not be shrunk by an expression",
      );
    }
  });
  it("gives every portrait its own masks when rendered together", () => {
    const html = renderToStaticMarkup(
      <>
        <CatAvatar />
        <CatAvatar recipe={{ ...defaultCat, eyes: 49, face: 49 }} />
      </>,
    );
    const ids = [...html.matchAll(/id="([^"]+)"/g)].map((match) => match[1]);
    assert.equal(new Set(ids).size, ids.length);
  });
  it("validates saved recipes and safely renders invalid server data", () => {
    assert.ok(validCat(defaultCat));
    assert.ok(!validCat({ ...defaultCat, eyes: 50 }));
    assert.ok(!validCat({ ...defaultCat, nose: 1.5 }));
    const html = renderToStaticMarkup(
      <CatAvatar recipe={{ ...defaultCat, eyes: 500 }} />,
    );
    assert.ok(!html.includes("NaN"));
  });
  it("keeps randomized cats within the versioned recipe bounds", () => {
    for (let n = 0; n < 100; n++) assert.ok(validCat(randomCat()));
  });
});

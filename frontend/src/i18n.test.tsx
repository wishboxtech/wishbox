import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { en, translate } from "./i18n";
import fa from "./fa.json";

describe("English and Persian interface copy", () => {
  it("keeps source copy available and translates complete user-facing phrases", () => {
    for (const text of Object.values(en)) assert.ok(text.trim());
    assert.equal(translate("Good gifts start", "en"), "Good gifts start");
    assert.equal(translate("Good gifts start", "fa"), "یکم راهنمایی");
    assert.equal(
      translate("{name}’s wishlists", "fa", { name: "سارا" }),
      "لیست‌های سارا",
    );
  });
  it("preserves placeholder names in every translation", () => {
    for (const [source, translation] of Object.entries(fa)) {
      assert.ok(translation.trim(), source);
      assert.deepEqual(
        [...source.matchAll(/\{\w+\}/g)].map((m) => m[0]).sort(),
        [...translation.matchAll(/\{\w+\}/g)].map((m) => m[0]).sort(),
        source,
      );
    }
  });
});

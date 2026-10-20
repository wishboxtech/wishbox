import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { renderToStaticMarkup } from "react-dom/server";
import { App } from "./App";
import { LanguageProvider } from "./i18n";

describe("Wishy interface", () => {
  for (const storedLocale of ["en", "fa"]) {
    it(`renders Wishy with the saved ${storedLocale} preference`, () => {
      Object.defineProperty(globalThis, "sessionStorage", {
        configurable: true,
        value: { getItem: () => null },
      });
      Object.defineProperty(globalThis, "localStorage", {
        configurable: true,
        value: { getItem: () => storedLocale },
      });
      Object.defineProperty(globalThis, "window", {
        configurable: true,
        value: { location: { pathname: "/", origin: "http://localhost" } },
      });
      const html = renderToStaticMarkup(
        <LanguageProvider>
          <App />
        </LanguageProvider>,
      );
      assert.ok(
        html.includes(
          storedLocale === "fa" ? "یکم راهنمایی" : "Good gifts start",
        ),
      );
      assert.ok(
        html.includes(
          storedLocale === "fa" ? "لیست خودم رو می‌سازم" : "Make my wishlist",
        ),
      );
      assert.ok(
        html.includes(
          storedLocale === "fa" ? "کادوهایی که می‌دم" : "Gifts I’m giving",
        ),
      );
      assert.ok(html.includes("wishy-cat.jpg"));
      assert.ok(!html.includes("Wishbox"));
      assert.ok(html.includes('value="fa"'));
      assert.ok(!html.includes("undefined"));
    });
  }
});

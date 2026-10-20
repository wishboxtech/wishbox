import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { cases, openCase } from "./ui-cases";
import { mkdir } from "node:fs/promises";

for (const lang of ["en", "fa"])
  for (const width of [390, 1440]) {
    test(`layout and accessibility · ${lang} · ${width}`, async ({
      browser,
    }) => {
      test.setTimeout(600000);

      await mkdir(`/tmp/wishy-ui/${lang}-${width}`, { recursive: true });
      for (const c of cases) {
        const context = await browser.newContext({
          viewport: { width, height: 960 },
        });
        const page = await context.newPage();
        await openCase(page, c, lang);
        await expect(page.locator("html")).toHaveAttribute(
          "dir",
          lang === "fa" ? "rtl" : "ltr",
        );
        expect
          .soft(
            await page.evaluate(
              () =>
                document.documentElement.scrollWidth <= window.innerWidth + 1,
            ),
            c.name + " document overflow",
          )
          .toBe(true);
        const overflow = await page
          .locator(
            "main h1, .modal h2, .button, .card-title, .gift-row, .notification, input, textarea, select, .cat-variant-grid",
          )
          .evaluateAll((els) =>
            els
              .filter((el) => {
                const r = el.getBoundingClientRect();
                return (
                  r.width > 0 &&
                  (r.left < -1 || r.right > window.innerWidth + 1)
                );
              })
              .map((el) => el.outerHTML.slice(0, 160)),
          );
        expect.soft(overflow, c.name + " clipped controls").toEqual([]);
        const ax = await new AxeBuilder({ page })
          .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
          .analyze();
        expect
          .soft(
            ax.violations.map((v) => ({
              id: v.id,
              nodes: v.nodes.map((n) => n.target),
            })),
            c.name + " accessibility",
          )
          .toEqual([]);
        await page.screenshot({
          path: `/tmp/wishy-ui/${lang}-${width}/${c.name}.png`,
          fullPage: !c.action,
        });
        if (c.action) {
          const dialog = page.getByRole("dialog");
          await expect(dialog).toBeVisible();
          await page.keyboard.press("Escape");
          await expect(dialog).toHaveCount(0);
        }
        await context.close();
      }
    });
  }

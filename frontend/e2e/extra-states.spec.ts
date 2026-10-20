import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { openCase } from "./ui-cases";
import { listId, wishId } from "./fixtures";

const extra = [
  {
    name: "edit-wish",
    path: `/wish/${wishId}`,
    s: { signedIn: true, owner: true },
    action: "edit-wish",
  },
  {
    name: "empty-notifications",
    path: "/notifications",
    s: { signedIn: true, empty: true },
  },
  { name: "empty-gifts", path: "/gifts", s: { signedIn: true, empty: true } },
  { name: "empty-shared", path: `/shared/${listId}`, s: { empty: true } },
  { name: "empty-contact", path: "/contact", s: { empty: true } },
  { name: "contact-error", path: "/contact", s: { error: true } },
];
for (const lang of ["en", "fa"])
  for (const width of [390, 1440]) {
    test(`additional editor and empty/error states · ${lang} · ${width}`, async ({
      browser,
    }) => {
      test.setTimeout(120000);
      for (const c of extra) {
        const context = await browser.newContext({
          viewport: { width, height: 960 },
        });
        const page = await context.newPage();
        await openCase(page, c, lang);
        if (c.action === "edit-wish") {
          const price = page.locator('input[name="price"]');
          await price.fill("۱٬۲۵۰٬۰۰۰");
          await expect(price).toHaveValue("1250000");
          await price.fill("-1");
          expect(
            await price.evaluate((el) =>
              (el as HTMLInputElement).checkValidity(),
            ),
          ).toBe(false);
          await price.fill("۱۲٫۵");
          expect(
            await price.evaluate((el) =>
              (el as HTMLInputElement).checkValidity(),
            ),
          ).toBe(false);
          await price.fill("۱۲۵۰۰۰۰");
        }
        await expect(page.locator(".loading")).toHaveCount(0);
        await expect(page.getByRole("alert")).toHaveCount(
          c.name === "contact-error" ? 1 : 0,
        );
        expect(
          (
            await new AxeBuilder({ page })
              .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
              .analyze()
          ).violations.map((v) => v.id),
          c.name,
        ).toEqual([]);
        await page.screenshot({
          path: `/tmp/wishy-ui/${lang}-${width}/${c.name}.png`,
          fullPage: !c.action,
        });
        for (const narrow of [320, 768]) {
          await page.setViewportSize({ width: narrow, height: 740 });
          expect(
            await page.evaluate(
              () => document.documentElement.scrollWidth <= innerWidth + 1,
            ),
            c.name,
          ).toBe(true);
        }
        if (c.action) {
          await page.keyboard.press("Tab");
          await page.keyboard.press("Shift+Tab");
          expect(
            await page
              .getByRole("dialog")
              .evaluate((el) => el.contains(document.activeElement)),
          ).toBe(true);
          await page.keyboard.press("Escape");
          await expect(page.getByRole("dialog")).toHaveCount(0);
        }
        await context.close();
      }
    });
  }

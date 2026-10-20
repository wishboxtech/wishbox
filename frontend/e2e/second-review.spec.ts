import { test, expect } from "@playwright/test";
import { cases, openCase } from "./ui-cases";
import { fixtures } from "./fixtures";

for (const lang of ["en", "fa"]) {
  test(`second review: resize, keyboard and dialog scrolling · ${lang}`, async ({
    browser,
  }) => {
    test.setTimeout(240000);
    for (const c of cases) {
      const context = await browser.newContext({
        viewport: { width: 768, height: 740 },
      });
      const page = await context.newPage();
      await openCase(page, c, lang);
      // Resize an already rendered page, including open dialogs and long copy.
      for (const width of [320, 768]) {
        await page.setViewportSize({ width, height: 740 });
        expect(
          await page.evaluate(
            () => document.documentElement.scrollWidth <= innerWidth + 1,
          ),
          c.name,
        ).toBe(true);
        if (c.action) {
          const dialog = page.getByRole("dialog");
          await expect(dialog).toBeInViewport({ ratio: 0.95 });
          await page.keyboard.press("Tab");
          for (let i = 0; i < 5; i++) await page.keyboard.press("Shift+Tab");
          expect(
            await dialog.evaluate((el) => el.contains(document.activeElement)),
          ).toBe(true);
          expect(
            await page
              .locator("header")
              .evaluate((el) => !!el.closest("[inert]")),
          ).toBe(true);
          await dialog.locator(".modal-body").evaluate((el) => {
            el.scrollTop = el.scrollHeight;
          });
          await expect(
            dialog.locator(".modal-heading button"),
          ).toBeInViewport();
        }
      }
      if (c.name === "landing" || c.name === "help") {
        const overlapping = await page
          .locator(".how-it-works > div")
          .evaluateAll((els) =>
            els.some((el) => {
              const range = document.createRange();
              range.selectNodeContents(el.querySelector("h2")!);
              const title = range.getBoundingClientRect();
              const num = el
                .querySelector(".step-number")!
                .getBoundingClientRect();
              return (
                num.left < title.right &&
                num.right > title.left &&
                num.top < title.bottom &&
                num.bottom > title.top
              );
            }),
          );
        expect(overlapping).toBe(false);
      }
      if (c.action) {
        await page.keyboard.press("Escape");
        await expect(page.getByRole("dialog")).toHaveCount(0);
        expect(
          await page
            .locator("header")
            .evaluate((el) => !!el.closest("[inert]")),
        ).toBe(false);
        expect(await page.evaluate(() => document.activeElement?.tagName)).toBe(
          "BUTTON",
        );
      }
      await context.close();
    }
  });
}

test("locale changes preserve a profile draft; cat pagination, undo, cancel and save remain distinct", async ({
  browser,
}) => {
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
  });
  const page = await context.newPage();
  await fixtures(page, "en", { signedIn: true });
  await page.goto("/profile");
  await page.locator('input[name="first_name"]').fill("نیما Nima");
  await page.locator(".language-switch select").selectOption("fa");
  await expect(page.locator("html")).toHaveAttribute("dir", "rtl");
  await expect(page.locator('input[name="first_name"]')).toHaveValue(
    "نیما Nima",
  );
  await expect(page.locator(".persian-wordmark").first()).toBeVisible();
  expect(
    await page
      .locator("body")
      .evaluate((el) => getComputedStyle(el).fontFamily),
  ).toContain("Vazir");
  const open = page.getByRole("button", { name: "عوض کردن گربه", exact: true });
  await open.click();
  const part = page.locator(".cat-part-tabs button").nth(1);
  await part.click();
  for (let n = 0; n < 4; n++)
    await page
      .getByRole("button", { name: "مدل‌های بعدی", exact: true })
      .click();
  await page.locator(".cat-variant-grid button").last().click();
  await expect(
    page.locator('.cat-live-preview [data-cat-layer="ears-50"]'),
  ).toHaveCount(1);
  await page.getByRole("button", { name: "برگردون", exact: true }).click();
  await expect(
    page.locator('.cat-live-preview [data-cat-layer="ears-1"]'),
  ).toHaveCount(1);
  await page.locator(".cat-variant-grid button").last().click();
  await page.keyboard.press("Escape");
  await expect(open).toBeFocused();
  await expect(
    page.locator('.profile-cat-card [data-cat-layer="ears-1"]'),
  ).toHaveCount(1);
  await open.click();
  await page.locator(".cat-part-tabs button").nth(1).click();
  await page.locator(".cat-variant-grid button").nth(4).click();
  await page
    .getByRole("button", { name: "همین گربه رو می‌خوام", exact: true })
    .click();
  await expect(
    page.locator('.profile-cat-card [data-cat-layer="ears-5"]'),
  ).toHaveCount(1);
  await expect(page.locator('input[name="first_name"]')).toHaveValue(
    "نیما Nima",
  );
  await page.reload();
  await expect(page.locator("html")).toHaveAttribute("dir", "rtl");
  // Choosing a cat updates the draft; only Save profile persists it.
  await expect(
    page.locator('.profile-cat-card [data-cat-layer="ears-1"]'),
  ).toHaveCount(1);
  await context.close();
});

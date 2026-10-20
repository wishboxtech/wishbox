import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { fixtures, wishId } from "./fixtures";
for (const lang of ["en", "fa"])
  for (const width of [320, 390, 768, 1440]) {
    test(`keepsake text, mixed notes and account menu · ${lang} · ${width}`, async ({
      browser,
    }) => {
      const context = await browser.newContext({
        viewport: { width, height: 844 },
      });
      const page = await context.newPage();
      await fixtures(page, lang, {
        signedIn: true,
        giver: true,
        status: "received",
      });
      await page.goto(`/wish/${wishId}`);
      const panel = page.locator(".received-keepsake");
      await expect(panel).toBeVisible();
      await page.evaluate(() => document.fonts.ready);
      const overlap = await panel.evaluate((el) => {
        const cat = el.querySelector(".keepsake-cat")!.getBoundingClientRect();
        return [".eyebrow", "h2"].some((selector) => {
          const range = document.createRange();
          range.selectNodeContents(el.querySelector(selector)!);
          const text = range.getBoundingClientRect();
          return (
            text.left < cat.right &&
            text.right > cat.left &&
            text.top < cat.bottom &&
            text.bottom > cat.top
          );
        });
      });
      expect(overlap).toBe(false);
      await expect(panel.locator("blockquote").first()).toHaveAttribute(
        "dir",
        "auto",
      );
      await panel.screenshot({
        path: `/tmp/wishy-ui/${lang}-${width}-keepsake-final.png`,
      });
      const trigger = page.locator(".profile-button");
      await trigger.click();
      const menu = page.locator(".account-menu");
      await expect(menu).toBeInViewport();
      expect(
        (
          await new AxeBuilder({ page })
            .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
            .analyze()
        ).violations.map((v) => v.id),
      ).toEqual([]);
      await page.keyboard.press("Tab");
      await page.keyboard.press("Escape");
      await expect(menu).toHaveCount(0);
      await expect(trigger).toBeFocused();
      await context.close();
    });
  }

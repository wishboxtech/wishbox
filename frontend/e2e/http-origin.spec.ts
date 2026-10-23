import { test, expect } from "@playwright/test";
import { fixtures, listId, wishId } from "./fixtures";

// Route the local build through a non-loopback HTTP origin. Chrome actually
// removes randomUUID here; localhost tests alone cannot catch this regression.
for (const lang of ["en", "fa"])
  for (const signedIn of [false, true]) {
    test(`wishlists and wish activity on an insecure HTTP origin · ${lang} · signed in ${signedIn}`, async ({ page, baseURL }) => {
      await page.route("http://wishy.insecure.test/**", async (route) => {
        const url = new URL(route.request().url());
        const response = await page.request.get(
          new URL(url.pathname + url.search, baseURL).href,
        );
        await route.fulfill({ response });
      });
      await fixtures(page, lang, { signedIn, owner: signedIn });
      const errors: string[] = [];
      page.on("pageerror", (error) => errors.push(error.message));
      const visitors: string[] = [];
      page.on("request", (request) => {
        if (/\/shared\/|\/activity\//.test(request.url()))
          visitors.push(request.headers()["x-wishy-visitor"]);
      });
      await page.goto(`http://wishy.insecure.test/lists/${listId}`);
      expect(await page.evaluate(() => isSecureContext)).toBe(false);
      expect(await page.evaluate(() => typeof crypto.randomUUID)).toBe("undefined");
      await expect(page.locator("main h1")).toHaveText("Birthday wishes · آرزوهای تولدم");
      const visitor = await page.evaluate(() => localStorage.getItem("wishy.visitor"));
      expect(visitor).toMatch(
        /^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$/,
      );
      await page.reload();
      await expect(page.locator("main h1")).toHaveText("Birthday wishes · آرزوهای تولدم");
      expect(await page.evaluate(() => localStorage.getItem("wishy.visitor"))).toBe(visitor);
      await page.goto(`http://wishy.insecure.test/wish/${wishId}`);
      await expect(page.locator("main h1")).toHaveText("A little reading lamp · چراغ مطالعه");
      expect(visitors.length).toBeGreaterThanOrEqual(3);
      expect(visitors.every((id) => id === visitor)).toBe(true);
      expect(errors).toEqual([]);
    });
  }

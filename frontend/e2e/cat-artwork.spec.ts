import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";
import { fixtures } from "./fixtures";
import { catParts } from "../src/cat";

test("all 500 designs stay inside the portrait and all 2,500 eye pairs keep broad black eyes", async ({
  page,
}) => {
  test.setTimeout(120_000);
  await page.goto("/cat-parts/review.html");
  expect(await page.locator("section figure").count()).toBe(500);
  const problems = await page
    .locator("section figure svg")
    .evaluateAll((cats) =>
      cats.flatMap((cat, i) => {
        const elements = [
          ...cat.querySelectorAll<SVGGraphicsElement>(
            ":scope > g[data-cat-layer]",
          ),
        ];
        return elements.flatMap((el) => {
          const b = el.getBBox();
          return b.width &&
            (b.x < 8 || b.y < 16 || b.x + b.width > 248 || b.y + b.height > 250)
            ? [
                {
                  i,
                  part: el.dataset.catLayer,
                  box: { x: b.x, y: b.y, width: b.width, height: b.height },
                },
              ]
            : [];
        });
      }),
    );
  expect(problems).toEqual([]);
  const ids = await page
    .locator("svg [id]")
    .evaluateAll((elements) => elements.map((e) => e.id));
  expect(new Set(ids).size).toBe(ids.length);
  await page.goto("/cat-parts/eye-pairs.html");
  expect(await page.locator("figure").count()).toBe(2500);
  const metrics = await page.locator("figure svg").evaluateAll(async (cats) => {
    const canvas = document.createElement("canvas");
    canvas.width = 256;
    canvas.height = 256;
    const ctx = canvas.getContext("2d", { willReadFrequently: true })!;
    let minBlack = 1,
      minWhite = 1,
      minArea = Infinity,
      worstBlack = -1,
      worstWhite = -1;
    for (let i = 0; i < cats.length; i++) {
      const svg = cats[i].cloneNode(true) as SVGSVGElement;
      for (const child of [...svg.children]) {
        if (
          child.tagName !== "defs" &&
          !["eyes-", "pupils-"].some((prefix) =>
            child.getAttribute("data-cat-layer")?.startsWith(prefix),
          ) &&
          !child.hasAttribute("data-eye-apertures")
        )
          child.remove();
      }
      svg.setAttribute("width", "256");
      svg.setAttribute("height", "256");
      const url = URL.createObjectURL(
        new Blob([new XMLSerializer().serializeToString(svg)], {
          type: "image/svg+xml",
        }),
      );
      const img = new Image();
      img.src = url;
      await img.decode();
      ctx.clearRect(0, 0, 256, 256);
      ctx.drawImage(img, 0, 0);
      URL.revokeObjectURL(url);
      const pixels = ctx.getImageData(0, 0, 256, 256).data;
      for (const [start, end] of [
        [45, 124],
        [132, 211],
      ]) {
        let black = 0,
          white = 0;
        for (let y = 108; y < 193; y++)
          for (let x = start; x < end; x++) {
            const offset = (y * 256 + x) * 4;
            if (pixels[offset + 3] < 200) continue;
            if (
              pixels[offset] < 55 &&
              pixels[offset + 1] < 50 &&
              pixels[offset + 2] < 65
            )
              black++;
            else if (
              pixels[offset] > 235 &&
              pixels[offset + 1] > 235 &&
              pixels[offset + 2] > 215
            )
              white++;
          }
        const area = black + white,
          ratio = black / area;
        if (ratio < minBlack) {
          minBlack = ratio;
          worstBlack = i;
        }
        if (white / area < minWhite) {
          minWhite = white / area;
          worstWhite = i;
        }
        minArea = Math.min(minArea, area);
      }
    }
    return { minBlack, minWhite, minArea, worstBlack, worstWhite };
  });
  console.log("Eye pair raster audit", metrics);
  expect(metrics.minBlack).toBeGreaterThan(0.42);
  expect(metrics.minWhite).toBeGreaterThan(0.1);
  expect(metrics.minArea).toBeGreaterThan(2400);
});

for (const lang of ["en", "fa"])
  for (const width of [320, 390, 768, 1440]) {
    test(`cat studio labels, all option pages, undo and masks · ${lang} · ${width}`, async ({
      browser,
    }) => {
      test.setTimeout(90_000);
      const context = await browser.newContext({
        viewport: { width, height: 1000 },
      });
      const page = await context.newPage();
      const errors: string[] = [];
      page.on("pageerror", (e) => errors.push(e.message));
      await fixtures(page, lang, { signedIn: true });
      await page.goto("/profile");
      await page
        .getByRole("button", {
          name: lang === "fa" ? "عوض کردن گربه" : "Change my cat",
          exact: true,
        })
        .click();
      for (let part = 0; part < catParts.length; part++) {
        await page.locator(".cat-part-tabs button").nth(part).click();
        for (let sheet = 0; sheet < 5; sheet++) {
          const options = page.locator(".cat-variant-grid button");
          await expect(options).toHaveCount(10);
          await options.last().click();
          await expect(
            page.locator(
              `.cat-live-preview > svg > [data-cat-layer="${catParts[part]}-${(sheet + 1) * 10}"]`,
            ),
          ).toHaveCount(1);
          expect(
            await options.evaluateAll((buttons) =>
              buttons.every((button) => {
                const label = button.querySelector(
                  ".cat-style-name",
                ) as HTMLElement;
                return (
                  !!button.getAttribute("aria-description") &&
                  label.scrollWidth <= label.clientWidth + 1
                );
              }),
            ),
          ).toBe(true);
          if (sheet < 4)
            await page
              .getByRole("button", {
                name: lang === "fa" ? "مدل‌های بعدی" : "Next styles",
                exact: true,
              })
              .click();
        }
      }
      await page.locator(".cat-part-tabs button").nth(2).click();
      await page
        .getByRole("button", {
          name: lang === "fa" ? "برگردون" : "Undo",
          exact: true,
        })
        .click();
      expect(
        await page.evaluate(
          () => document.documentElement.scrollWidth <= innerWidth,
        ),
      ).toBe(true);
      const accessibility = await new AxeBuilder({ page })
        .withTags(["wcag2a", "wcag2aa", "wcag21aa"])
        .analyze();
      if (accessibility.violations.length)
        console.log(
          JSON.stringify(
            accessibility.violations.map((v) => ({
              id: v.id,
              nodes: v.nodes.map((n) => ({
                target: n.target,
                summary: n.failureSummary,
              })),
            })),
            null,
            2,
          ),
        );
      expect(accessibility.violations.map((v) => v.id)).toEqual([]);
      await page.locator(".modal").screenshot({
        path: `/tmp/wishy-ui/cat-studio-v2-${lang}-${width}.png`,
      });
      expect(errors).toEqual([]);
      await context.close();
    });
  }

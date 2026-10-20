import { expect, type Page } from "@playwright/test";
import { fixtures, listId, wishId, type Scenario } from "./fixtures";
export const cases: {
  name: string;
  path: string;
  s: Scenario;
  action?: string;
}[] = [
  { name: "landing", path: "/", s: {} },
  { name: "dashboard", path: "/", s: { signedIn: true } },
  { name: "empty", path: "/", s: { signedIn: true, empty: true } },
  {
    name: "list-owner",
    path: `/lists/${listId}`,
    s: { signedIn: true, owner: true },
  },
  { name: "shared", path: `/shared/${listId}`, s: {} },
  { name: "wish-guest", path: `/wish/${wishId}`, s: {} },
  {
    name: "wish-giver",
    path: `/wish/${wishId}`,
    s: { signedIn: true, giver: true, status: "reserved" },
  },
  {
    name: "wish-purchased",
    path: `/wish/${wishId}`,
    s: { signedIn: true, owner: true, status: "purchased" },
  },
  {
    name: "received-owner",
    path: `/wish/${wishId}`,
    s: { signedIn: true, owner: true, status: "received" },
  },
  {
    name: "received-giver",
    path: `/wish/${wishId}`,
    s: { signedIn: true, giver: true, status: "received" },
  },
  {
    name: "gifts",
    path: "/gifts",
    s: { signedIn: true, giver: true, status: "received" },
  },
  { name: "notifications", path: "/notifications", s: { signedIn: true } },
  { name: "profile", path: "/profile", s: { signedIn: true } },
  { name: "help", path: "/help", s: {} },
  { name: "contact", path: "/contact", s: {} },
  { name: "404", path: "/missing", s: {} },
  { name: "error", path: `/shared/${listId}`, s: { error: true } },
  { name: "long-content", path: `/wish/${wishId}`, s: { long: true } },
  { name: "signin", path: "/", s: {}, action: "signin" },
  { name: "otp", path: "/", s: {}, action: "otp" },
  { name: "reserve", path: `/wish/${wishId}`, s: {}, action: "reserve" },
  { name: "new-list", path: "/", s: { signedIn: true }, action: "new-list" },
  {
    name: "edit-list",
    path: `/lists/${listId}`,
    s: { signedIn: true, owner: true },
    action: "edit-list",
  },
  {
    name: "new-wish",
    path: `/lists/${listId}`,
    s: { signedIn: true, owner: true },
    action: "new-wish",
  },
  { name: "share", path: `/shared/${listId}`, s: {}, action: "share" },
  {
    name: "delete",
    path: `/lists/${listId}`,
    s: { signedIn: true, owner: true },
    action: "delete",
  },
  {
    name: "cat-studio",
    path: "/profile",
    s: { signedIn: true },
    action: "cat",
  },
];

export async function openCase(
  page: Page,
  c: (typeof cases)[number],
  lang: string,
) {
  const crashes: string[] = [];
  page.on("pageerror", (error) => crashes.push(error.message));
  await fixtures(page, lang, c.s);
  await page.goto(c.path);
  try {
    await expect(page.locator("main h1,main h2").first(), c.name).toBeVisible();
  } catch (error) {
    await page.screenshot({
      path: `/tmp/wishy-load-failure-${lang}-${c.name}.png`,
    });
    throw new Error(`${c.name}: ${crashes.join("; ") || String(error)}`);
  }
  expect(crashes, c.name + " runtime errors").toEqual([]);
  const b = (en: string, fa: string) =>
    page.getByRole("button", { name: lang === "en" ? en : fa, exact: true });
  if (c.action === "signin" || c.action === "otp") {
    await b("Sign in", "ورود / ثبت‌نام").click();
    if (c.action === "otp") {
      await page.getByRole("textbox").fill("09123456789");
      await b("Get my code", "کد ورود رو بفرست").click();
    }
  }
  if (c.action === "reserve")
    await b("I’ll gift this", "این رو کادو می‌دم").click();
  if (c.action === "new-list") await b("New wishlist", "لیست تازه").click();
  if (c.action === "edit-list") await b("Edit list", "ویرایش لیست").click();
  if (c.action === "new-wish") await b("Add a wish", "افزودن آرزو").click();
  if (c.action === "edit-wish") await b("Edit wish", "ویرایش آرزو").click();
  if (c.action === "share") await b("Share list", "فرستادن لیست").click();
  if (c.action === "delete") await b("Delete list", "حذف لیست").click();
  if (c.action === "cat") await b("Change my cat", "عوض کردن گربه").click();
  await page.evaluate(() => document.fonts.ready);
}

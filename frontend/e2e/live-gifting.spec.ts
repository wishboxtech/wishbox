import { test, expect, type Page } from "@playwright/test";
import { readFileSync } from "node:fs";
const dataPath = process.env.WISHY_LIVE_DATA;
test.skip(!dataPath, "Run against the disposable backend browser test server.");

async function signIn(page: Page, phone: string, claim = false) {
  await page.getByRole("button", { name: "Sign in", exact: true }).click();
  if (claim) await page.locator(".guest-claim-choice input").check();
  await page.getByRole("textbox", { name: "Mobile number" }).fill(phone);
  await page.getByRole("button", { name: "Get my code" }).click();
  await page.getByRole("textbox", { name: "Verification code" }).fill("123456");
  const result = page.waitForResponse(
    (r) =>
      r.url().endsWith("auth/otp/verify/") && r.request().method() === "POST",
  );
  await page.getByRole("button", { name: "Let me in" }).click();
  await expect(page.getByRole("dialog")).toHaveCount(0);
  return (await (await result).json()).data;
}

test("real API: guest plan → first signup → cat profile → receipt and private/shared notes → another browser", async ({
  browser,
}) => {
  test.setTimeout(120000);
  const data = JSON.parse(readFileSync(dataPath!, "utf8"));
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
  });
  const guest = await context.newPage();
  await guest.goto(`/wish/${data.wish_ids[0]}`);
  await guest
    .getByRole("button", { name: "I’ll gift this", exact: true })
    .click();
  await guest
    .getByRole("textbox", { name: "Your name or nickname" })
    .fill("Nima");
  await guest.getByRole("button", { name: "Tomorrow", exact: true }).click();
  await guest
    .getByRole("combobox", { name: "My next step" })
    .selectOption("Order the exact item online");
  await guest.locator(".commitment-form input[type=checkbox]").check();
  await guest.getByRole("button", { name: "Reserve with this plan" }).click();
  await expect(
    guest.getByRole("button", { name: "I’ve bought it", exact: true }),
  ).toBeVisible();
  const signup = await signIn(guest, "09123450902", true);
  expect(signup.is_new_user).toBe(true);
  expect(signup.guest_claimed).toBe(true);
  expect(
    await guest.evaluate(() => localStorage.getItem("wishy.gifts")),
  ).toBeNull();
  await guest.goto("/profile");
  await guest
    .getByRole("textbox", { name: "First name", exact: true })
    .fill("Nima");
  await guest
    .getByRole("button", { name: "Make your cat", exact: true })
    .click();
  await guest.getByRole("button", { name: "Ears", exact: true }).click();
  for (let i = 0; i < 4; i++)
    await guest
      .getByRole("button", { name: "Next styles", exact: true })
      .click();
  await guest
    .getByRole("button", { name: "Ears, style 50", exact: true })
    .click();
  await guest
    .getByRole("button", { name: "Use this cat", exact: true })
    .click();
  await guest
    .getByRole("button", { name: "Start wishing", exact: true })
    .click();
  await expect(
    guest.getByRole("heading", { name: "Nima’s wishlists" }),
  ).toBeVisible();
  await guest.goto(`/wish/${data.wish_ids[0]}`);
  await guest
    .getByRole("button", { name: "I’ve bought it", exact: true })
    .click();
  await expect(
    guest.getByText("From your plan to their doorstep."),
  ).toBeVisible();
  const ownerContext = await browser.newContext();
  const owner = await ownerContext.newPage();
  await owner.goto("/");
  await signIn(owner, data.owner_phone);
  await owner.goto(`/wish/${data.wish_ids[0]}`);
  await owner
    .getByRole("button", { name: "Confirm gift arrived", exact: true })
    .click();
  await owner
    .getByRole("radio", { name: "Not right for me", exact: true })
    .check();
  await owner
    .getByRole("textbox", { name: "A note for future you" })
    .fill("RECIPIENT PRIVATE: wrong size");
  await owner
    .getByRole("button", { name: "Save just for me", exact: true })
    .click();
  await expect(
    owner.getByText("Saved just for you. Nothing was shared with your friend."),
  ).toBeVisible();
  await owner
    .getByRole("textbox", { name: "Your note to your friend" })
    .fill("Thanks for thinking of me 💜");
  await owner
    .getByRole("button", {
      name: "Share this note with my friend",
      exact: true,
    })
    .click();
  await guest.reload();
  await expect(
    guest.getByRole("heading", { name: "You followed through.", exact: true }),
  ).toBeVisible();
  await expect(
    guest.getByText("Thanks for thinking of me 💜", { exact: true }),
  ).toBeVisible();
  await expect(guest.getByText("RECIPIENT PRIVATE: wrong size")).toHaveCount(0);
  // The disposable server uses a 15-second OTP cooldown. Exercise a fresh OTP
  // request on the second device rather than bypassing authentication.
  await new Promise((resolve) => setTimeout(resolve, 16000));
  const deviceContext = await browser.newContext();
  const device = await deviceContext.newPage();
  await device.goto("/");
  const login = await signIn(device, "09123450902");
  expect(login.is_new_user).toBe(false);
  await device.goto("/gifts");
  await expect(device.getByText("Reading lamp", { exact: true })).toBeVisible();
  await device.goto("/profile");
  await expect(
    device.locator('.profile-cat-card [data-cat-layer="ears-50"]'),
  ).toHaveCount(1);
  await Promise.all([
    context.close(),
    ownerContext.close(),
    deviceContext.close(),
  ]);
});

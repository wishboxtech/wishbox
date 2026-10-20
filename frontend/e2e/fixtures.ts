import type { Page } from "@playwright/test";
export const listId = "11111111-1111-4111-8111-111111111111",
  wishId = "22222222-2222-4222-8222-222222222222";
const dates = {
  created_at: "2026-10-20T12:00:00Z",
  updated_at: "2026-10-20T12:00:00Z",
};
export const list = {
  id: listId,
  name: "Birthday wishes · آرزوهای تولدم",
  description: "Little things I’d love — چند تا از چیزهایی که دوست دارم",
  cover: null,
  ...dates,
};
export const wish = {
  ...list,
  id: wishId,
  wishlist_id: listId,
  name: "A little reading lamp · چراغ مطالعه",
  description:
    "Warm light, adjustable arm. رنگ بنفش، مدل قابل تنظیم.\nhttps://example.com/lamp",
  price: "1250000",
};
export const profile = {
  profile_id: "owner",
  first_name: "سارا",
  last_name: "Ahmadi",
  bio: "Cats, books & small joys.",
  photo: null,
  cat_avatar: {
    version: 1,
    face: 0,
    ears: 0,
    eyes: 0,
    pupils: 0,
    brows: 0,
    nose: 0,
    mouth: 0,
    whiskers: 0,
    markings: 0,
    accessories: 0,
    fur: 0,
    background: 0,
  },
};
export type Scenario = {
  signedIn?: boolean;
  owner?: boolean;
  giver?: boolean;
  status?: string;
  empty?: boolean;
  error?: boolean;
  long?: boolean;
  guest?: boolean;
};
export async function fixtures(page: Page, lang: string, s: Scenario = {}) {
  await page.addInitScript(
    ({ lang, s }) => {
      if (sessionStorage.getItem("wishy.fixture")) return;
      localStorage.clear();
      sessionStorage.clear();
      sessionStorage.setItem("wishy.fixture", "1");
      localStorage.setItem("wishbox.language", lang);
      if (s.signedIn)
        sessionStorage.setItem(
          "wishbox.session",
          JSON.stringify({
            access_token: "test-access",
            refresh_token: "test-refresh",
          }),
        );
    },
    { lang, s },
  );
  const stats = {
    wish_id: wishId,
    views: 1234,
    likes: 23,
    liked: false,
    status: s.status || "available",
    is_owner: !!s.owner,
    is_giver: !!s.giver,
    reservation_id: s.owner || s.giver ? 7 : null,
  };
  const gift = {
    id: 7,
    wish_id: wishId,
    wishlist_id: listId,
    wish_name: wish.name,
    status: stats.status,
    created_at: dates.created_at,
    purchase_by: "2026-11-01",
    purchase_plan: "Order the exact item online",
    extension_count: 0,
    expires_at: "2026-11-03T12:00:00Z",
    thank_you:
      stats.status === "received"
        ? "Thanks for all the cozy reading nights! مرسی که یادم بودی 💜"
        : "",
    follow_up_note:
      stats.status === "received" ? "Could we check the size together?" : "",
    received_at: stats.status === "received" ? dates.created_at : null,
  };
  await page.route("**/api/V0.0.0/**", async (route) => {
    const path = new URL(route.request().url()).pathname.split(
        "/api/V0.0.0/",
      )[1],
      method = route.request().method();
    const ok = (data: unknown, status = 200) =>
      route.fulfill({ status, json: { data } });
    if (
      s.error &&
      (path.startsWith("wishlist/") || path.startsWith("website/"))
    )
      return route.fulfill({ status: 503, json: { detail: "offline" } });
    if (path === "profile/") return ok(profile);
    if (path === "notifications/")
      return ok({
        unread: s.empty ? 0 : 1,
        items: s.empty
          ? []
          : [
              {
                id: "note1",
                wish_id: wishId,
                wish_name: wish.name,
                event: "gift_received",
                read_at: null,
                created_at: dates.created_at,
              },
            ],
      });
    if (path === "profile/wishlist/") return ok(s.empty ? [] : [list]);
    if (path === `wishlist/${listId}/shared/`)
      return ok({
        wishlist: list,
        wishes: s.empty
          ? []
          : [
              {
                ...wish,
                name: s.long ? "آرزویبسیارطولانی".repeat(15) : wish.name,
              },
            ],
        activity: [stats],
        is_owner: !!s.owner,
      });
    if (path === `wish/${wishId}/`)
      return ok({
        ...wish,
        name: s.long ? "AnUnbrokenWishName".repeat(18) : wish.name,
      });
    if (path === `wish/${wishId}/activity/`) return ok(stats);
    if (path === "gifts/") return ok(s.empty ? [] : [gift]);
    if (path === "gifts/7/experience/")
      return ok(
        s.owner
          ? {
              role: "owner",
              gift,
              fit: "trying",
              private_note: "Private — فقط برای خودم",
              thank_you: gift.thank_you,
              follow_up_note: gift.follow_up_note,
            }
          : { role: "giver", gift },
      );
    if (path === "auth/otp/") return ok({ otp_id: "otp-test" });
    if (path === "auth/otp/verify/")
      return ok({
        access_token: "test",
        refresh_token: "refresh",
        is_new_user: true,
        guest_claimed: true,
      });
    if (path === "website/contact-us/")
      return ok(s.empty ? [] : [{ id: "contact", email: "hello@example.com" }]);
    if (path === `wish/${wishId}/reservation/`)
      return ok(
        { ...gift, management_token: "private-test-key" },
        method === "POST" ? 201 : 200,
      );
    return route.fulfill({ status: 404, json: { detail: path } });
  });
}

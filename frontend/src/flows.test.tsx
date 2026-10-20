import { afterEach, beforeEach, describe, it } from "node:test";
import assert from "node:assert/strict";
import { Window } from "happy-dom";
import { act } from "react";
import type { Root } from "react-dom/client";
import type {
  Activity,
  Collection,
  GiftRecord,
  Inbox,
  Profile,
  Wish,
} from "./types";

// Isolated DOM tests use only the fake API below. No page/network is loaded.
const dom = new Window({
  url: "https://wishy.test/",
  settings: {
    enableJavaScriptEvaluation: false,
    disableJavaScriptFileLoading: true,
    enableCSSFileLoading: false,
    enableImageFileLoading: false,
    enableIframePageLoading: false,
    navigation: { disableMainFrameNavigation: true },
  },
});
for (const [key, value] of Object.entries({
  window: dom,
  document: dom.document,
  navigator: dom.navigator,
  HTMLElement: dom.HTMLElement,
  HTMLInputElement: dom.HTMLInputElement,
  Event: dom.Event,
  MouseEvent: dom.MouseEvent,
  Node: dom.Node,
  FormData: dom.FormData,
  sessionStorage: dom.sessionStorage,
  localStorage: dom.localStorage,
  IS_REACT_ACT_ENVIRONMENT: true,
}))
  Object.defineProperty(globalThis, key, {
    configurable: true,
    writable: true,
    value,
  });
const { createRoot } = await import("react-dom/client");
const { App } = await import("./App");
const { LanguageProvider } = await import("./i18n");
const { session } = await import("./api");
const listId = "11111111-1111-4111-8111-111111111111",
  wishId = "22222222-2222-4222-8222-222222222222";
const dates = {
  created_at: "2026-10-20T10:00:00Z",
  updated_at: "2026-10-20T10:00:00Z",
};
const profile: Profile = {
  profile_id: "owner",
  first_name: "Alex",
  last_name: "",
  bio: "",
  birthdate: null,
  gender: "",
  phone_number: null,
  email: null,
  photo: null,
};
let root: Root,
  lists: Collection[],
  wishes: Wish[],
  stats: Activity,
  inbox: Inbox;
let calls: {
  path: string;
  method: string;
  body: Record<string, unknown>;
  headers: Headers;
}[];
let conflict = false;
let unexpectedRequests: string[] = [];
let storedGift: GiftRecord;
let privateFit = "",
  privateNote = "";
function futureDate(days: number) {
  const day = new Date();
  day.setDate(day.getDate() + days);
  return `${day.getFullYear()}-${String(day.getMonth() + 1).padStart(2, "0")}-${String(day.getDate()).padStart(2, "0")}`;
}
function button(name: string) {
  const matches = [...document.querySelectorAll("button")].filter(
    (el) => el.textContent?.trim() === name,
  );
  assert.equal(
    matches.length,
    1,
    `Expected one button “${name}”, found ${matches.length}. ${document.body.textContent}`,
  );
  return matches[0];
}
async function click(name: string) {
  await act(async () => {
    button(name).click();
  });
}
async function fill(selector: string, value: string) {
  const input = document.querySelector<HTMLInputElement>(selector);
  assert.ok(input, selector);
  await act(async () => {
    Object.getOwnPropertyDescriptor(
      dom.HTMLInputElement.prototype,
      "value",
    )!.set!.call(input, value);
    input.dispatchEvent(new Event("input", { bubbles: true }));
  });
}
async function submitForm() {
  const form = document.querySelector("[role=dialog] form");
  assert.ok(form);
  await act(async () => {
    form.dispatchEvent(
      new Event("submit", { bubbles: true, cancelable: true }),
    );
  });
}
async function choosePlan() {
  await click("Tomorrow");
  const select = document.querySelector<HTMLSelectElement>(
    "[role=dialog] select",
  );
  assert.ok(select);
  await act(async () => {
    select.value = "Order the exact item online";
    select.dispatchEvent(new Event("change", { bubbles: true }));
  });
  const checkbox = document.querySelector<HTMLInputElement>(
    "[role=dialog] input[type=checkbox]",
  );
  assert.ok(checkbox);
  await act(async () => checkbox.click());
}
async function textarea(selector: string, text: string) {
  const element = document.querySelector<HTMLTextAreaElement>(selector);
  assert.ok(element);
  await act(async () => {
    Object.getOwnPropertyDescriptor(
      dom.HTMLTextAreaElement.prototype,
      "value",
    )!.set!.call(element, text);
    element.dispatchEvent(new Event("input", { bubbles: true }));
  });
}
async function mount(path = "/", signed = false) {
  dom.happyDOM.setURL(`https://wishy.test${path}`);
  if (signed)
    session.set({ access_token: "test-access", refresh_token: "test-refresh" });
  root = createRoot(document.getElementById("root")!);
  await act(async () => {
    root.render(
      <LanguageProvider>
        <App />
      </LanguageProvider>,
    );
  });
}
function result(data: unknown, status = 200) {
  return new Response(JSON.stringify({ data }), { status });
}
beforeEach(() => {
  document.body.innerHTML = '<div id="root"></div>';
  sessionStorage.clear();
  localStorage.clear();
  lists = [];
  wishes = [
    {
      ...dates,
      id: wishId,
      wishlist_id: listId,
      name: "A thoughtful book",
      description: "A good read",
      price: "42",
      cover: null,
    },
  ];
  privateFit = "";
  privateNote = "";
  storedGift = {
    id: 1,
    wish_id: wishId,
    wishlist_id: listId,
    wish_name: "A thoughtful book",
    status: "available",
    created_at: dates.created_at,
    purchase_by: futureDate(12),
    purchase_plan: "Order the exact item online",
    expires_at: `${futureDate(14)}T00:00:00Z`,
    extension_count: 0,
    thank_you: "",
    follow_up_note: "",
    follow_up_acknowledged_at: null,
  };
  stats = {
    wish_id: wishId,
    views: 1,
    likes: 0,
    liked: false,
    status: "available",
    is_owner: false,
    is_giver: false,
    reservation_id: null,
  };
  inbox = { items: [], unread: 0 };
  calls = [];
  conflict = false;
  unexpectedRequests = [];
  globalThis.fetch = async (url, options = {}) => {
    const path = String(url).replace("/api/V0.0.0/", ""),
      method = options.method || "GET";
    const body =
      typeof options.body === "string" ? JSON.parse(options.body) : {};
    calls.push({ path, method, body, headers: new Headers(options.headers) });
    if (path === "profile/") return result(profile);
    if (path === "profile/wishlist/") {
      if (method === "POST") {
        const item = {
          ...dates,
          id: listId,
          name: body.name,
          description: body.description,
          cover: null,
        };
        lists.push(item);
        return result(item, 201);
      }
      return result(lists);
    }
    if (path === `wishlist/${listId}/shared/`)
      return result({
        wishlist: lists[0] || {
          ...dates,
          id: listId,
          name: "Birthday",
          description: "",
          cover: null,
        },
        wishes,
        activity: [stats],
        is_owner: true,
      });
    if (path === `wishlist/${listId}/` && method === "POST") {
      const item = {
        ...dates,
        ...body,
        id: wishId,
        wishlist_id: listId,
        cover: null,
      };
      wishes.push(item);
      return result(item, 201);
    }
    if (path === `wish/${wishId}/`) return result(wishes[0]);
    if (path === `wish/${wishId}/activity/`) {
      if (body.action === "like") {
        stats.liked = true;
        stats.likes = 1;
      }
      if (body.action === "unlike") {
        stats.liked = false;
        stats.likes = 0;
      }
      return result(stats);
    }
    if (path === `wish/${wishId}/reservation/`) {
      if (method === "POST" && conflict) {
        stats.status = "reserved";
        return new Response(
          JSON.stringify({
            data: { error: "Someone has already reserved this wish." },
            error_type: ["gift_conflict"],
          }),
          { status: 409 },
        );
      }
      if (body.action === "reschedule") {
        storedGift.purchase_by = body.purchase_by;
        storedGift.extension_count = 1;
        return result(storedGift);
      }
      stats.status =
        method === "POST"
          ? "reserved"
          : body.action === "purchase"
            ? "purchased"
            : body.action === "receive"
              ? "received"
              : "available";
      stats.is_giver = stats.status !== "available" && !stats.is_owner;
      stats.reservation_id = stats.status !== "available" ? 1 : null;
      const gift: GiftRecord = {
        ...storedGift,
        id: 1,
        wish_id: wishId,
        wishlist_id: listId,
        wish_name: wishes[0].name,
        status: body.action === "cancel" ? "cancelled" : stats.status,
        created_at: dates.created_at,
        management_token: method === "POST" ? "private-management-key" : null,
      };
      if (method === "POST") {
        gift.purchase_by = body.purchase_by;
        gift.purchase_plan = body.purchase_plan;
      }
      storedGift = {
        ...gift,
        received_at: gift.status === "received" ? dates.created_at : null,
      };
      return result(gift, method === "POST" ? 201 : 200);
    }
    if (/^gifts\/[12]\/experience\/$/.test(path)) {
      const requestedId = Number(path.split("/")[1]);
      const projectedGift =
        requestedId === storedGift.id
          ? storedGift
          : { ...storedGift, id: requestedId, status: stats.status };
      if (method === "PATCH") {
        if (body.action === "save_private") {
          privateFit = body.fit || "";
          privateNote = body.private_note || "";
        }
        if (body.action === "share_thanks") {
          storedGift.thank_you = body.thank_you;
          storedGift.thank_you_sent_at = dates.created_at;
        }
        if (body.action === "withdraw_thanks") {
          storedGift.thank_you = "";
          storedGift.thank_you_sent_at = null;
        }
        if (body.action === "share_follow_up") {
          storedGift.follow_up_note = body.follow_up_note;
          storedGift.follow_up_sent_at = dates.created_at;
        }
        if (body.action === "acknowledge_follow_up")
          storedGift.follow_up_acknowledged_at = dates.created_at;
      }
      return result(
        stats.is_owner
          ? {
              role: "owner",
              gift: {
                id: 1,
                wish_id: wishId,
                wish_name: storedGift.wish_name,
                status: stats.status,
                received_at: storedGift.received_at,
              },
              fit: privateFit,
              private_note: privateNote,
              thank_you: storedGift.thank_you,
              thank_you_sent_at: storedGift.thank_you_sent_at,
              follow_up_note: storedGift.follow_up_note,
              follow_up_sent_at: storedGift.follow_up_sent_at,
              follow_up_acknowledged_at: storedGift.follow_up_acknowledged_at,
            }
          : { role: "giver", gift: projectedGift },
      );
    }
    if (path === "notifications/") {
      if (method === "PATCH") {
        inbox.unread = 0;
        inbox.items.forEach((item) => (item.read_at = dates.created_at));
      }
      return result(inbox);
    }
    if (path === "gifts/") return result([]);
    unexpectedRequests.push(`${method} ${path}`);
    throw new Error(`Unexpected fake API request: ${method} ${path}`);
  };
});
afterEach(async () => {
  if (root) await act(async () => root.unmount());
  await dom.happyDOM.abort();
  assert.deepEqual(unexpectedRequests, []);
});

describe("actual React user flows with a fake API", () => {
  it("creates a list, opens it immediately, and adds a wish to the correct parent", async () => {
    wishes = [];
    await mount("/", true);
    await click("New wishlist");
    await fill("[role=dialog] input:not([type=file])", "Birthday hints");
    await submitForm();
    assert.equal(dom.location.pathname, `/lists/${listId}`);
    assert.ok(document.body.textContent?.includes("Birthday hints"));
    await click("Add a wish");
    await fill("[role=dialog] input:not([type=file])", "A lovely book");
    await fill('[role=dialog] input[name="price"]', "۴٬۲۰۰");
    await submitForm();
    const create = calls.find(
      (call) => call.path === `wishlist/${listId}/` && call.method === "POST",
    );
    assert.ok(create);
    assert.equal(create.body.name, "A lovely book");
    assert.equal(create.body.description, "");
    assert.equal(create.body.price, "4200");
    assert.ok(document.body.textContent?.includes("A lovely book"));
    assert.ok(!calls.some((call) => call.path.includes("undefined")));
  });
  it("lets a guest like, reserve, buy, and cancel using their private key", async () => {
    await mount(`/wish/${wishId}`);
    await click("0 likes");
    assert.equal(button("1 like").getAttribute("aria-pressed"), "true");
    await click("I’ll gift this");
    await fill("[role=dialog] input", "Sam");
    await choosePlan();
    await submitForm();
    assert.ok(
      document.body.textContent?.includes("This one’s yours to make happen."),
    );
    await click("I’ve bought it");
    assert.ok(
      document.body.textContent?.includes("You’re about to make their day."),
    );
    const purchase = calls.find(
      (call) => call.method === "PATCH" && call.body.action === "purchase",
    );
    assert.equal(
      purchase?.headers.get("X-Wishy-Gift-Token"),
      "private-management-key",
    );
    await click("Cancel reservation");
    await click("Release it");
    assert.ok(document.body.textContent?.includes("Make their day."));
    const cancel = calls.find((call) => call.body.action === "cancel");
    assert.equal(
      cancel?.headers.get("X-Wishy-Gift-Token"),
      "private-management-key",
    );
    assert.ok(!document.querySelector("[role=dialog]"));
  });
  it("lets only the owner confirm a purchased gift and open their parent wishlist", async () => {
    stats.is_owner = true;
    stats.reservation_id = 1;
    stats.status = "purchased";
    storedGift.status = "purchased";
    await mount(`/wish/${wishId}`, true);
    await click("Confirm gift arrived");
    assert.ok(
      document.body.textContent?.includes("A thoughtful gift, received."),
    );
    assert.ok(!document.body.textContent?.includes("Confirm gift arrived"));
    await click("Back to wishlist");
    assert.equal(dom.location.pathname, `/shared/${listId}`);
  });
  it("shows a reservation conflict and updates availability instead of falsely succeeding", async () => {
    conflict = true;
    await mount(`/wish/${wishId}`);
    await click("I’ll gift this");
    await fill("[role=dialog] input", "Sam");
    await choosePlan();
    await submitForm();
    assert.ok(
      document.body.textContent?.includes(
        "Someone has already reserved this wish.",
      ),
    );
    assert.ok(document.body.textContent?.includes("A friend is on it."));
    assert.equal(localStorage.getItem("wishy.gifts"), null);
  });
  it("shows unread notifications and marks them read", async () => {
    inbox = {
      unread: 1,
      items: [
        {
          id: "notice",
          wish_id: wishId,
          wish_name: "A thoughtful book",
          event: "reserved",
          read_at: null,
          created_at: dates.created_at,
        },
      ],
    };
    await mount("/notifications", true);
    assert.ok(
      document.body.textContent?.includes("Someone is making your wish happen"),
    );
    await click("Mark all read");
    assert.equal(inbox.unread, 0);
    assert.ok(!document.body.textContent?.includes("Mark all read"));
  });
  it("requires a day, a next step and checked details before reserving", async () => {
    await mount(`/wish/${wishId}`);
    await click("I’ll gift this");
    await fill("[role=dialog] input", "Sam");
    assert.ok(button("Reserve with this plan").disabled);
    await submitForm();
    assert.ok(
      !calls.some(
        (call) => call.path.endsWith("reservation/") && call.method === "POST",
      ),
    );
    await choosePlan();
    await submitForm();
    const reservation = calls.find(
      (call) => call.path.endsWith("reservation/") && call.method === "POST",
    );
    assert.ok(reservation?.body.purchase_by);
    assert.equal(
      reservation?.body.purchase_plan,
      "Order the exact item online",
    );
    assert.equal(reservation?.body.details_checked, true);
  });
  it("keeps dissatisfaction private until the recipient explicitly shares their own note", async () => {
    stats.is_owner = true;
    stats.status = "received";
    stats.reservation_id = 1;
    storedGift.status = "received";
    await mount(`/wish/${wishId}`, true);
    assert.ok(
      document.body.textContent?.includes("How is it working for you?"),
    );
    const option = document.querySelector<HTMLInputElement>(
      'input[value="not_for_me"]',
    );
    assert.ok(option);
    await act(async () => option.click());
    await textarea(
      'form[aria-label="Private gift check-in"] textarea',
      "A private size issue",
    );
    await click("Save just for me");
    assert.equal(privateFit, "not_for_me");
    assert.equal(privateNote, "A private size issue");
    assert.equal(storedGift.thank_you, "");
    assert.ok(!calls.some((call) => call.body.action === "share_thanks"));
    await textarea(
      'form[aria-label="Share a personal note"] textarea',
      "Thanks for thinking of our reading afternoons.",
    );
    await click("Share this note with my friend");
    const shared = calls.find((call) => call.body.action === "share_thanks");
    assert.ok(shared);
    assert.equal(
      shared.body.thank_you,
      "Thanks for thinking of our reading afternoons.",
    );
    assert.equal(shared.body.private_note, undefined);
    assert.equal(shared.body.fit, undefined);
    await click("Remove shared note");
    assert.equal(storedGift.thank_you, "");
    assert.equal(privateNote, "A private size issue");
  });
  it("gives the giver a real receipt keepsake and lets them acknowledge a practical note", async () => {
    stats.status = "received";
    stats.is_giver = true;
    stats.reservation_id = 1;
    storedGift.status = "received";
    storedGift.thank_you = "You made a rainy afternoon better.";
    storedGift.follow_up_note = "Could we check the size together?";
    await mount(`/wish/${wishId}/gift/1`, true);
    assert.ok(document.body.textContent?.includes("You followed through."));
    assert.ok(document.body.textContent?.includes(storedGift.thank_you));
    assert.ok(
      !document.body.textContent?.includes("How is it working for you?"),
    );
    await click("I’ll check this with you");
    assert.ok(
      calls.some((call) => call.body.action === "acknowledge_follow_up"),
    );
    assert.ok(storedGift.follow_up_acknowledged_at);
  });
  it("lets a giver choose a new plan day once", async () => {
    stats.status = "reserved";
    stats.is_giver = true;
    stats.reservation_id = 1;
    storedGift.status = "reserved";
    await mount(`/wish/${wishId}`, true);
    await click("Need a different day?");
    await fill(".journey-panel input[type=date]", futureDate(15));
    await click("Save new day");
    assert.ok(
      calls.some(
        (call) =>
          call.body.action === "reschedule" &&
          call.body.purchase_by === futureDate(15),
      ),
    );
    assert.ok(!document.body.textContent?.includes("Need a different day?"));
  });
  it("keeps an old gift entry separate from the current reservation actions", async () => {
    stats.status = "reserved";
    stats.is_giver = true;
    stats.reservation_id = 2;
    storedGift.status = "cancelled";
    await mount(`/wish/${wishId}/gift/1`, true);
    assert.ok(document.body.textContent?.includes("A previous gift plan."));
    assert.ok(!document.body.textContent?.includes("I’ve bought it"));
    await click("View current wish");
    assert.equal(dom.location.pathname, `/wish/${wishId}`);
    assert.ok(document.body.textContent?.includes("I’ve bought it"));
  });
});

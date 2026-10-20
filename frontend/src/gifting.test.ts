import { beforeEach, describe, it } from "node:test";
import assert from "node:assert/strict";
import {
  giftActions,
  giftHeaders,
  localGifts,
  rememberGift,
  visitorId,
} from "./gifting";
import type { Activity, GiftRecord } from "./types";

let data: Map<string, string>;
beforeEach(() => {
  data = new Map();
  Object.defineProperty(globalThis, "localStorage", {
    configurable: true,
    value: {
      getItem: (key: string) => data.get(key) || null,
      setItem: (key: string, value: string) => data.set(key, value),
    },
  });
});
const gift: GiftRecord = {
  id: 1,
  wish_id: "wish",
  wishlist_id: "list",
  wish_name: "Camera",
  status: "reserved",
  created_at: "2026-10-20",
  management_token: "private-token",
};
const activity: Activity = {
  wish_id: "wish",
  status: "reserved",
  is_owner: false,
  is_giver: true,
  views: 1,
  likes: 0,
  liked: false,
};
describe("gift management", () => {
  it("preserves the private management token through purchase and receipt updates", () => {
    rememberGift(gift);
    rememberGift({ ...gift, status: "purchased", management_token: null });
    assert.equal(localGifts().length, 1);
    assert.equal(localGifts()[0].management_token, "private-token");
    assert.equal(giftHeaders("wish")["X-Wishy-Gift-Token"], "private-token");
    assert.equal(giftHeaders("another-wish")["X-Wishy-Gift-Token"], undefined);
  });
  it("uses one persistent visitor identity", () => {
    assert.equal(visitorId(), visitorId());
    assert.match(visitorId(), /^[a-f0-9-]{36}$/);
  });
  it("offers the correct next step to the giver and owner", () => {
    assert.deepEqual(giftActions(activity), ["purchase", "cancel"]);
    assert.deepEqual(giftActions({ ...activity, status: "purchased" }), [
      "cancel",
    ]);
    assert.deepEqual(
      giftActions({
        ...activity,
        status: "purchased",
        is_owner: true,
        is_giver: false,
      }),
      ["receive"],
    );
    assert.deepEqual(
      giftActions({
        ...activity,
        status: "reserved",
        is_owner: true,
        is_giver: false,
      }),
      [],
    );
    assert.deepEqual(giftActions({ ...activity, is_giver: false }), []);
    assert.deepEqual(giftActions({ ...activity, status: "received" }), []);
  });
  it("tolerates corrupt or missing stored guest data", () => {
    data.set("wishy.gifts", "{}");
    assert.deepEqual(localGifts(), []);
    data.set("wishy.gifts", JSON.stringify([{ nonsense: true }]));
    assert.deepEqual(localGifts(), []);
    data.set("wishy.visitor", "broken");
    assert.match(visitorId(), /^[a-f0-9-]{36}$/);
  });
});

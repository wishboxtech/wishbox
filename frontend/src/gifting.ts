import { request } from "./api";
import { randomUuid } from "./browserCrypto";
import type { Activity, GiftRecord, GiftStatus } from "./types";

const VISITOR_KEY = "wishy.visitor";
const GIFTS_KEY = "wishy.gifts";
let memoryVisitor = "";
let memoryGifts: GiftRecord[] = [];
export function visitorId() {
  try {
    const stored = localStorage.getItem(VISITOR_KEY);
    if (stored && /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(stored)) return stored;
  } catch {
    /* Keep the page usable when browser storage is disabled. */
  }
  memoryVisitor ||= randomUuid();
  try {
    localStorage.setItem(VISITOR_KEY, memoryVisitor);
  } catch {
    /* Session fallback. */
  }
  return memoryVisitor;
}
export function localGifts(): GiftRecord[] {
  try {
    const stored = JSON.parse(localStorage.getItem(GIFTS_KEY) || "[]");
    return Array.isArray(stored)
      ? stored.filter(
          (item) =>
            item &&
            typeof item.wish_id === "string" &&
            typeof item.management_token === "string",
        )
      : [];
  } catch {
    return memoryGifts;
  }
}
export function rememberGift(gift: GiftRecord) {
  const previous = localGifts();
  const old = previous.find((item) => item.wish_id === gift.wish_id);
  memoryGifts = [
    ...previous.filter((item) => item.wish_id !== gift.wish_id),
    {
      ...gift,
      management_token: gift.management_token || old?.management_token,
    },
  ];
  try {
    localStorage.setItem(GIFTS_KEY, JSON.stringify(memoryGifts));
  } catch {
    /* Session fallback. */
  }
}
export function giftHeaders(wishId?: string) {
  const token = localGifts().find(
    (item) => item.wish_id === wishId,
  )?.management_token;
  return {
    "X-Wishy-Visitor": visitorId(),
    ...(token ? { "X-Wishy-Gift-Token": token } : {}),
  };
}
export function getActivity(
  wishId: string,
  action?: "view" | "like" | "unlike",
  signal?: AbortSignal,
) {
  return request<Activity>(`wish/${wishId}/activity/`, {
    method: action ? "POST" : "GET",
    headers: giftHeaders(wishId),
    ...(action ? { body: { action } } : {}),
    signal,
  });
}
export const statusLabels: Record<GiftStatus, string> = {
  available: "Ready to gift",
  reserved: "Reserved",
  purchased: "On its way",
  received: "Gift received",
  cancelled: "Cancelled",
  expired: "Hold ended",
};
export function giftActions(
  activity: Activity,
): ("purchase" | "cancel" | "receive")[] {
  if (activity.is_owner && activity.status === "purchased") return ["receive"];
  if (activity.is_giver && activity.status === "reserved")
    return ["purchase", "cancel"];
  if (activity.is_giver && activity.status === "purchased") return ["cancel"];
  return [];
}

const GUEST_KEY = "wishy.guest-key";
const CLAIMED_KEY = "wishy.guest-claimed";
let memoryGuestKey = "";
let memoryGuestFinished = false;
export function guestKey() {
  if (memoryGuestFinished) return undefined;
  try {
    if (localStorage.getItem(CLAIMED_KEY)) return undefined;
    const key = localStorage.getItem(GUEST_KEY);
    if (key && /^[a-f0-9]{64}$/.test(key)) return key;
  } catch {
    /* Use the in-memory identity for this page. */
  }
  memoryGuestKey ||= Array.from(
    crypto.getRandomValues(new Uint8Array(32)),
    (n) => n.toString(16).padStart(2, "0"),
  ).join("");
  try {
    localStorage.setItem(GUEST_KEY, memoryGuestKey);
  } catch {
    /* Memory fallback. */
  }
  return memoryGuestKey;
}
export function canClaimGuest() {
  if (memoryGuestFinished) return false;
  try {
    return (
      !localStorage.getItem(CLAIMED_KEY) &&
      !!localStorage.getItem(GUEST_KEY) &&
      localGifts().length > 0
    );
  } catch {
    return !!memoryGuestKey && memoryGifts.length > 0;
  }
}
export function finishGuestClaim() {
  memoryGuestFinished = true;
  memoryGuestKey = "";
  memoryGifts = [];
  try {
    localStorage.setItem(CLAIMED_KEY, "1");
    localStorage.removeItem(GUEST_KEY);
    localStorage.removeItem(GIFTS_KEY);
  } catch {
    /* The server still enforces a single claim. */
  }
}

export function finishGuestDecision() {
  memoryGuestFinished = true;
  try {
    localStorage.setItem(CLAIMED_KEY, "1");
  } catch {
    /* Server enforces signup only. */
  }
}

import { beforeEach, describe, it } from "node:test";
import assert from "node:assert/strict";
import { ApiError, mediaUrl, request, session, upload } from "./api";

function storage() {
  const data = new Map<string, string>();
  return {
    getItem: (key: string) => data.get(key) ?? null,
    setItem: (key: string, value: string) => data.set(key, value),
    removeItem: (key: string) => data.delete(key),
  };
}
const calls: { url: string; options: RequestInit }[] = [];
let replies: (Response | Error)[];
let loggedOut = false;
function reply(data: unknown, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}
beforeEach(() => {
  Object.defineProperty(globalThis, "sessionStorage", {
    configurable: true,
    value: storage(),
  });
  Object.defineProperty(globalThis, "localStorage", {
    configurable: true,
    value: storage(),
  });
  Object.defineProperty(globalThis, "window", {
    configurable: true,
    value: {
      dispatchEvent: () => {
        loggedOut = true;
      },
    },
  });
  calls.length = 0;
  replies = [];
  loggedOut = false;
  globalThis.fetch = async (url, options = {}) => {
    calls.push({ url: String(url), options });
    const result = replies.shift();
    if (result instanceof Error) throw result;
    assert.ok(result, "An unexpected HTTP request was made");
    return result;
  };
});

describe("existing Wishbox HTTP contracts", () => {
  it("sends raw JWT and English locale and unwraps envelopes", async () => {
    session.set({ access_token: "access", refresh_token: "refresh" });
    localStorage.setItem("wishbox.language", "fa");
    replies.push(reply({ data: [{ id: "list" }] }));
    assert.deepEqual(await request("profile/wishlist/"), [{ id: "list" }]);
    assert.equal(calls[0].url, "/api/V0.0.0/profile/wishlist/");
    assert.equal(
      new Headers(calls[0].options.headers).get("Authorization"),
      "access",
    );
    assert.equal(
      new Headers(calls[0].options.headers).get("Accept-Language"),
      "en",
    );
    assert.equal(calls[0].options.credentials, "omit");
  });
  it("keeps private tokens out of public requests", async () => {
    session.set({ access_token: "access", refresh_token: "refresh" });
    replies.push(reply({ data: [] }));
    await request("wishlist/public/", { public: true });
    assert.equal(
      new Headers(calls[0].options.headers).has("Authorization"),
      false,
    );
  });
  it("supports the flat anonymous friend response", async () => {
    replies.push(
      reply({ created: true, anonymous_friend_id: "friend", status: 201 }, 201),
    );
    const result = await request<{ anonymous_friend_id: string }>(
      "wish/create-anonymous-friend/",
      { method: "POST", public: true, body: { nickname: "A friend" } },
    );
    assert.equal(result.anonymous_friend_id, "friend");
  });
  it("refreshes expired access and retries with the new JWT", async () => {
    session.set({ access_token: "expired", refresh_token: "refresh" });
    replies.push(
      reply({}, 401),
      reply({
        data: { access_token: "new-access", refresh_token: "new-refresh" },
      }),
      reply({ data: { profile_id: "user" } }),
    );
    assert.deepEqual(await request("profile/"), { profile_id: "user" });
    assert.deepEqual(JSON.parse(calls[1].options.body as string), {
      refresh_token: "refresh",
    });
    assert.equal(
      new Headers(calls[2].options.headers).get("Authorization"),
      "new-access",
    );
  });
  it("expires rejected refresh sessions without infinite retries", async () => {
    session.set({ access_token: "expired", refresh_token: "expired" });
    replies.push(reply({}, 401), reply({}, 400));
    await assert.rejects(request("profile/"), { status: 401 });
    assert.equal(session.get(), null);
    assert.equal(calls.length, 2);
    assert.equal(loggedOut, true);
  });
  it("does not refresh or retry a forbidden owner-only mutation", async () => {
    session.set({ access_token: "access", refresh_token: "refresh" });
    replies.push(
      reply(
        { error_type: ["NOT_WISHLIST_OWNER"], data: { error: "Denied" } },
        403,
      ),
    );
    await assert.rejects(request("wishlist/other/", { method: "DELETE" }), {
      status: 403,
      codes: ["NOT_WISHLIST_OWNER"],
    });
    assert.equal(calls.length, 1);
  });
  it("does not restore tokens when sign-out happens during refresh", async () => {
    session.set({ access_token: "expired", refresh_token: "refresh" });
    let resolveRefresh!: (response: Response) => void;
    let refreshStarted!: () => void;
    const started = new Promise<void>((resolve) => {
      refreshStarted = resolve;
    });
    globalThis.fetch = async (url) => {
      if (String(url).endsWith("refresh/")) {
        refreshStarted();
        return new Promise<Response>((resolve) => {
          resolveRefresh = resolve;
        });
      }
      return reply({}, 401);
    };
    const pending = request("profile/");
    await started;
    session.clear();
    resolveRefresh(
      reply({ data: { access_token: "new", refresh_token: "new-refresh" } }),
    );
    await assert.rejects(
      pending,
      (err: unknown) => err instanceof ApiError && err.status === 401,
    );
    assert.equal(session.get(), null);
  });
  it("uploads multipart files without a JSON content-type header", async () => {
    replies.push(reply({ data: { media_id: "media" } }, 201));
    assert.equal(
      await upload(new File(["image"], "cover.png", { type: "image/png" })),
      "media",
    );
    assert.ok(calls[0].options.body instanceof FormData);
    assert.equal(
      new Headers(calls[0].options.headers).has("Content-Type"),
      false,
    );
  });
  it("distinguishes network failures and preserves cancellation", async () => {
    replies.push(new TypeError("offline"));
    await assert.rejects(request("profile/"), { status: 0 });
    replies.push(new DOMException("Aborted", "AbortError"));
    await assert.rejects(request("profile/"), { name: "AbortError" });
  });
  it("handles non-JSON proxy failures", async () => {
    replies.push(new Response("<html>Bad Gateway</html>", { status: 502 }));
    await assert.rejects(request("profile/"), ApiError);
  });
  it("restricts media protocols and normalizes relative paths", () => {
    assert.equal(mediaUrl("javascript:alert(1)"), undefined);
    assert.equal(mediaUrl("media/photo.png"), "/media/photo.png");
    assert.equal(mediaUrl("/media/photo.png"), "/media/photo.png");
    assert.equal(
      mediaUrl("https://example.com/photo.png"),
      "https://example.com/photo.png",
    );
  });
});

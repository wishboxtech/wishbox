import { afterEach, describe, it } from "node:test";
import assert from "node:assert/strict";
import { randomUuid } from "./browserCrypto";

const original = Object.getOwnPropertyDescriptor(globalThis, "crypto")!;
afterEach(() => Object.defineProperty(globalThis, "crypto", original));

describe("browser UUID support", () => {
  it("uses the native generator when available", () => {
    const expected = "0dff9672-f8f8-4c1d-bf5b-6e78a1bbd3b5";
    const implementation = {
      randomUUID() {
        assert.equal(this, implementation);
        return expected;
      },
    };
    Object.defineProperty(globalThis, "crypto", {
      configurable: true,
      value: implementation,
    });
    assert.equal(randomUuid(), expected);
  });

  it("constructs a UUID v4 from random bytes when HTTP hides randomUUID", () => {
    let calls = 0;
    Object.defineProperty(globalThis, "crypto", {
      configurable: true,
      value: {
        getRandomValues(bytes: Uint8Array) {
          calls++;
          assert.equal(bytes.length, 16);
          return bytes.fill(0xff);
        },
      },
    });
    assert.equal(randomUuid(), "ffffffff-ffff-4fff-bfff-ffffffffffff");
    assert.equal(calls, 1);
  });

  it("keeps fallback UUIDs random and sets their version and variant bits", () => {
    const native = globalThis.crypto;
    Object.defineProperty(globalThis, "crypto", {
      configurable: true,
      value: { getRandomValues: native.getRandomValues.bind(native) },
    });
    const ids = Array.from({ length: 100 }, randomUuid);
    assert.equal(new Set(ids).size, 100);
    for (const id of ids)
      assert.match(id, /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/);
  });
});

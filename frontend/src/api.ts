import type { Tokens } from "./types";

const SESSION_KEY = "wishbox.session";
const BASE = "/api/V0.0.0/";
type Envelope<T> = {
  data: T;
  ok?: boolean;
  error_type?: string[];
  detail?: string;
};
export class ApiError extends Error {
  constructor(
    public status: number,
    public codes: string[],
    public details: unknown,
  ) {
    super(`API request failed (${status})`);
  }
}

export const session = {
  get(): Tokens | null {
    try {
      return JSON.parse(sessionStorage.getItem(SESSION_KEY) || "null");
    } catch {
      return null;
    }
  },
  set(tokens: Tokens) {
    sessionStorage.setItem(SESSION_KEY, JSON.stringify(tokens));
  },
  clear() {
    sessionStorage.removeItem(SESSION_KEY);
    window.dispatchEvent(new Event("wishbox:logout"));
  },
};

let refreshing: Promise<void> | null = null;
async function refresh() {
  if (!refreshing) {
    refreshing = (async () => {
      const tokens = session.get();
      if (!tokens) throw new ApiError(401, [], null);
      const response = await fetch(`${BASE}auth/otp/refresh/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh_token: tokens.refresh_token }),
      });
      const payload = await response.json();
      // Do not restore a signed-out session or replace a newly signed-in account.
      if (session.get()?.refresh_token !== tokens.refresh_token)
        throw new ApiError(401, [], null);
      if (!response.ok) {
        session.clear();
        throw new ApiError(401, payload.error_type || [], payload.data);
      }
      session.set(payload.data);
    })().finally(() => {
      refreshing = null;
    });
  }
  await refreshing;
}

export async function request<T>(
  path: string,
  options: {
    method?: string;
    body?: unknown;
    public?: boolean;
    signal?: AbortSignal;
    headers?: Record<string, string>;
  } = {},
  retried = false,
): Promise<T> {
  const headers: Record<string, string> = {
    Accept: "application/json",
    "Accept-Language":
      typeof document !== "undefined" && document.documentElement.lang === "fa"
        ? "fa"
        : "en",
    ...options.headers,
  };
  const tokens = options.public ? null : session.get();
  // The existing backend expects the raw JWT in Authorization (without Bearer).
  if (tokens) headers.Authorization = tokens.access_token;
  const multipart = options.body instanceof FormData;
  if (options.body !== undefined && !multipart)
    headers["Content-Type"] = "application/json";
  let response: Response;
  try {
    response = await fetch(`${BASE}${path}`, {
      method: options.method || "GET",
      headers,
      signal: options.signal,
      credentials: "omit",
      body:
        options.body === undefined
          ? undefined
          : multipart
            ? (options.body as FormData)
            : JSON.stringify(options.body),
    });
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError")
      throw error;
    throw new ApiError(0, [], null);
  }
  let payload: Envelope<T>;
  try {
    payload = await response.json();
  } catch {
    throw new ApiError(response.status, [], null);
  }
  if (response.status === 401 && tokens && !retried) {
    await refresh();
    return request<T>(path, options, true);
  }
  if (!response.ok) {
    if (response.status === 401 && tokens) session.clear();
    throw new ApiError(
      response.status,
      payload.error_type || [],
      payload.data || payload.detail,
    );
  }
  return (payload.data === undefined ? payload : payload.data) as T;
}

export async function upload(file: File): Promise<string> {
  const form = new FormData();
  form.append("file", file);
  return (
    await request<{ media_id: string }>("storage/upload/", {
      method: "POST",
      body: form,
    })
  ).media_id;
}

export function mediaUrl(file?: string) {
  if (!file) return undefined;
  if (file.startsWith("/")) return file;
  try {
    const url = new URL(file);
    return ["https:", "http:"].includes(url.protocol) ? url.href : undefined;
  } catch {
    return `/${file}`;
  }
}

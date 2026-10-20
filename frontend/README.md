# Wishy frontend

An independent, English-only React + TypeScript application for making and sharing
wishlists. Uses the supplied purple/yellow Wishy cat logo, accessible larger text,
responsive cards, guest/registered gifting, unique likes/views and notifications.

Use Node 22.12+:

```bash
npm ci
npm run dev
npm run build
npm test
```

Vite proxies backend requests at `/api/V0.0.0/` using the root `.env.local` API port.
Set `API_PROXY_TARGET` for another backend. This application owns its package
manifest, lockfile, TypeScript/Vite configuration and Dockerfile.

Run the complete project with `make up` or `make dev` at the repository root.
See [the full-stack guide](../docs/full-stack.md) and
[gifting contracts](../docs/wishy-gifting.md). Guest management tokens stay in
this browser’s local storage; JWT sessions remain in per-tab session storage.

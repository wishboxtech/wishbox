import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, "..", "");
  const target =
    env.API_PROXY_TARGET || `http://127.0.0.1:${env.API_PORT || "8000"}`;
  return {
    envDir: "..",
    plugins: [react()],
    server: {
      port: 5173,
      strictPort: true,
      proxy: Object.fromEntries(
        ["/api", "/media", "/admin", "/static"].map((path) => [
          path,
          { target, changeOrigin: true },
        ]),
      ),
    },
  };
});

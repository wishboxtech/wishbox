import { defineConfig } from "@playwright/test";
import { existsSync } from "node:fs";
const chrome =
  process.env.CHROME_PATH ||
  (existsSync("/opt/google/chrome/chrome")
    ? "/opt/google/chrome/chrome"
    : undefined);
export default defineConfig({
  testDir: "./e2e",
  fullyParallel: true,
  timeout: 30000,
  workers: 2,
  expect: { timeout: 15000 },
  outputDir: process.env.WISHY_TEST_OUTPUT || "/tmp/wishy-playwright-results",
  use: {
    baseURL: process.env.WISHY_UI_URL || "http://127.0.0.1:5174",
    headless: true,
    launchOptions: { executablePath: chrome, args: ["--no-sandbox"] },
  },
  webServer: process.env.WISHY_UI_URL
    ? undefined
    : {
        command: "npm run dev -- --port 5174 --strictPort",
        url: "http://127.0.0.1:5174",
        reuseExistingServer: !process.env.CI,
      },
  reporter: [["list"]],
});

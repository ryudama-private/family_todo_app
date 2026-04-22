import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  server: {
    host: "0.0.0.0",
    port: 5173,
    allowedHosts: [
      "frontend",
      "localhost",
      "127.0.0.1",
      "::1",
      "family-todo-app-container.bravemeadow-4bab85b8.japaneast.azurecontainerapps.io",
      "family-todo-app-container.bravemeadow-4bab85be.japaneast.azurecontainerapps.io",
    ],
    proxy: {
      "/auth": {
        target: "http://backend:8000",
        changeOrigin: true,
      },
    },
    watch: {
      usePolling: true,
      interval: 300,
    },
  },
  test: {
    environment: "jsdom",
    globals: true,
    include: ["src/**/*.test.js"],
  },
});

import { fileURLToPath, URL } from "node:url";
import vue from "@vitejs/plugin-vue";
import { defineConfig } from "vite";

// https://vitejs.dev/config/
export default defineConfig({
  // ensure font assets from dependencies are included in the build
  assetsInclude: ["**/*.woff", "**/*.woff2"],

  // MARK: start vite build config

  // vite creates a manifest and assets during the build process (local and prod)
  // django collectstatics will put assets in '/static/app_name/assets'
  // django will put the manifest in '/static/manifest.json'
  // vite manifest prefaces all files with the path 'app_name/assets/xxxx'
  build: {
    manifest: true,
    chunkSizeWarningLimit: 1600,
    rolldownOptions: {
      input: [
        // list all entry points
        "./pathways_vue/main.js",
      ],
      output: {
        // optimize css asset file names (remove hash) for better Clarity caching
        assetFileNames: (assetInfo) => {
          const prefix = "pathways/assets/";
          const name = assetInfo.names?.[0] ?? "";
          if (name.endsWith(".css")) {
            return `${prefix}[name][extname]`;
          }
          return `${prefix}[name]-[hash][extname]`;
        },
      },
    },
    outDir: "./pathways/static/", // relative path to django's static directory
    assetsDir: "pathways/assets", // default ('assets')... this is the namespaced subdirectory of outDir that vite uses
    emptyOutDir: true,
  },
  publicDir: "pathways_vue/public", // Vite will copy contents to outDir (/static/pathways/img/)
  base: "/static/", // allows for proper css url path creation during the build process

  // MARK: standard vite/vue plugin and resolver config
  plugins: [vue()],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./pathways_vue", import.meta.url)),
    },
  },
  css: {
    preprocessorOptions: {
      scss: {
        quietDeps: true,
        silenceDeprecations: ["global-builtin", "import"], // silence bootstrap5 related deprecations
      },
    },
  },
});

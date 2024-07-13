// vite.config.mjs
import { defineConfig } from "file:///C:/Users/LM2P/Documents/000_programming/000-projects/pdm-game/mvp/client/ui/node_modules/vite/dist/node/index.js";
import { svelte } from "file:///C:/Users/LM2P/Documents/000_programming/000-projects/pdm-game/mvp/client/ui/node_modules/@sveltejs/vite-plugin-svelte/src/index.js";
import { run } from "file:///C:/Users/LM2P/Documents/000_programming/000-projects/pdm-game/mvp/client/ui/node_modules/vite-plugin-run/dist/index.mjs";
import * as path from "path";
var __vite_injected_original_dirname = "C:\\Users\\LM2P\\Documents\\000_programming\\000-projects\\pdm-game\\mvp\\client\\ui";
var isTest = process.env.NODE_ENV === "test";
var vite_config_default = defineConfig({
  resolve: {
    alias: {
      src: path.resolve(__vite_injected_original_dirname, "./src")
    },
    conditions: isTest ? ["browser"] : []
  },
  plugins: [
    svelte({ hot: !process.env.VITEST }),
    run({
      silent: !!process.env.VITEST,
      input: [
        {
          name: "typecheck",
          run: ["npm", "run", "check"],
          pattern: ["src/**/*.ts", "src/**/*.svelte"]
        }
      ]
    })
  ],
  server: {
    port: isTest ? 8678 : 5173,
    proxy: isTest ? void 0 : {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: false
      }
    }
  },
  build: {
    outDir: "build",
    target: "es2020",
    cssCodeSplit: false
  },
  optimizeDeps: {
    include: isTest ? ["@testing-library/svelte", "chai"] : void 0
  },
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: "src/setup-tests.ts"
  }
});
export {
  vite_config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcubWpzIl0sCiAgInNvdXJjZXNDb250ZW50IjogWyJjb25zdCBfX3ZpdGVfaW5qZWN0ZWRfb3JpZ2luYWxfZGlybmFtZSA9IFwiQzpcXFxcVXNlcnNcXFxcTE0yUFxcXFxEb2N1bWVudHNcXFxcMDAwX3Byb2dyYW1taW5nXFxcXDAwMC1wcm9qZWN0c1xcXFxwZG0tZ2FtZVxcXFxtdnBcXFxcY2xpZW50XFxcXHVpXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ZpbGVuYW1lID0gXCJDOlxcXFxVc2Vyc1xcXFxMTTJQXFxcXERvY3VtZW50c1xcXFwwMDBfcHJvZ3JhbW1pbmdcXFxcMDAwLXByb2plY3RzXFxcXHBkbS1nYW1lXFxcXG12cFxcXFxjbGllbnRcXFxcdWlcXFxcdml0ZS5jb25maWcubWpzXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ltcG9ydF9tZXRhX3VybCA9IFwiZmlsZTovLy9DOi9Vc2Vycy9MTTJQL0RvY3VtZW50cy8wMDBfcHJvZ3JhbW1pbmcvMDAwLXByb2plY3RzL3BkbS1nYW1lL212cC9jbGllbnQvdWkvdml0ZS5jb25maWcubWpzXCI7Ly8vIDxyZWZlcmVuY2UgdHlwZXM9XCJ2aXRlc3RcIiAvPlxyXG5pbXBvcnQgeyBkZWZpbmVDb25maWcgfSBmcm9tICd2aXRlJ1xyXG5pbXBvcnQgeyBzdmVsdGUgfSBmcm9tICdAc3ZlbHRlanMvdml0ZS1wbHVnaW4tc3ZlbHRlJ1xyXG5pbXBvcnQgeyBydW4gfSBmcm9tICd2aXRlLXBsdWdpbi1ydW4nO1xyXG5pbXBvcnQgKiBhcyBwYXRoIGZyb20gJ3BhdGgnXHJcblxyXG5jb25zdCBpc1Rlc3QgPSBwcm9jZXNzLmVudi5OT0RFX0VOViA9PT0gJ3Rlc3QnXHJcblxyXG4vLyBodHRwczovL3ZpdGVqcy5kZXYvY29uZmlnL1xyXG5leHBvcnQgZGVmYXVsdCBkZWZpbmVDb25maWcoe1xyXG4gIHJlc29sdmU6IHtcclxuICAgIGFsaWFzOiB7XHJcbiAgICAgIHNyYzogcGF0aC5yZXNvbHZlKF9fZGlybmFtZSwgJy4vc3JjJylcclxuICAgIH0sXHJcbiAgICBjb25kaXRpb25zOiBpc1Rlc3QgPyBbJ2Jyb3dzZXInXSA6IFtdXHJcbiAgfSxcclxuICBwbHVnaW5zOiBbXHJcbiAgICBzdmVsdGUoeyBob3Q6ICFwcm9jZXNzLmVudi5WSVRFU1QgfSksXHJcbiAgICBydW4oe1xyXG4gICAgICBzaWxlbnQ6ICEhcHJvY2Vzcy5lbnYuVklURVNULFxyXG4gICAgICBpbnB1dDogW1xyXG4gICAgICAgIHtcclxuICAgICAgICAgIG5hbWU6ICd0eXBlY2hlY2snLFxyXG4gICAgICAgICAgcnVuOiBbJ25wbScsICdydW4nLCAnY2hlY2snXSxcclxuICAgICAgICAgIHBhdHRlcm46IFsnc3JjLyoqLyoudHMnLCAnc3JjLyoqLyouc3ZlbHRlJ10sXHJcbiAgICAgICAgfVxyXG4gICAgICBdXHJcbiAgICB9KVxyXG4gIF0sXHJcbiAgc2VydmVyOiB7XHJcbiAgICBwb3J0OiBpc1Rlc3QgPyA4Njc4IDogNTE3MyxcclxuICAgIHByb3h5OiBpc1Rlc3QgPyB1bmRlZmluZWQgOiB7XHJcbiAgICAgICcvYXBpJzoge1xyXG4gICAgICAgIHRhcmdldDogJ2h0dHA6Ly9sb2NhbGhvc3Q6ODAwMCcsXHJcbiAgICAgICAgY2hhbmdlT3JpZ2luOiBmYWxzZVxyXG4gICAgICB9XHJcbiAgICB9XHJcbiAgfSxcclxuICBidWlsZDoge1xyXG4gICAgb3V0RGlyOiAnYnVpbGQnLFxyXG4gICAgdGFyZ2V0OiAnZXMyMDIwJyxcclxuICAgIGNzc0NvZGVTcGxpdDogZmFsc2VcclxuICB9LFxyXG4gIG9wdGltaXplRGVwczoge1xyXG4gICAgaW5jbHVkZTogaXNUZXN0ID8gWydAdGVzdGluZy1saWJyYXJ5L3N2ZWx0ZScsICdjaGFpJ10gOiB1bmRlZmluZWRcclxuICB9LFxyXG4gIHRlc3Q6IHtcclxuICAgIGdsb2JhbHM6IHRydWUsXHJcbiAgICBlbnZpcm9ubWVudDogJ2pzZG9tJyxcclxuICAgIHNldHVwRmlsZXM6ICdzcmMvc2V0dXAtdGVzdHMudHMnXHJcbiAgfVxyXG59KVxyXG4iXSwKICAibWFwcGluZ3MiOiAiO0FBQ0EsU0FBUyxvQkFBb0I7QUFDN0IsU0FBUyxjQUFjO0FBQ3ZCLFNBQVMsV0FBVztBQUNwQixZQUFZLFVBQVU7QUFKdEIsSUFBTSxtQ0FBbUM7QUFNekMsSUFBTSxTQUFTLFFBQVEsSUFBSSxhQUFhO0FBR3hDLElBQU8sc0JBQVEsYUFBYTtBQUFBLEVBQzFCLFNBQVM7QUFBQSxJQUNQLE9BQU87QUFBQSxNQUNMLEtBQVUsYUFBUSxrQ0FBVyxPQUFPO0FBQUEsSUFDdEM7QUFBQSxJQUNBLFlBQVksU0FBUyxDQUFDLFNBQVMsSUFBSSxDQUFDO0FBQUEsRUFDdEM7QUFBQSxFQUNBLFNBQVM7QUFBQSxJQUNQLE9BQU8sRUFBRSxLQUFLLENBQUMsUUFBUSxJQUFJLE9BQU8sQ0FBQztBQUFBLElBQ25DLElBQUk7QUFBQSxNQUNGLFFBQVEsQ0FBQyxDQUFDLFFBQVEsSUFBSTtBQUFBLE1BQ3RCLE9BQU87QUFBQSxRQUNMO0FBQUEsVUFDRSxNQUFNO0FBQUEsVUFDTixLQUFLLENBQUMsT0FBTyxPQUFPLE9BQU87QUFBQSxVQUMzQixTQUFTLENBQUMsZUFBZSxpQkFBaUI7QUFBQSxRQUM1QztBQUFBLE1BQ0Y7QUFBQSxJQUNGLENBQUM7QUFBQSxFQUNIO0FBQUEsRUFDQSxRQUFRO0FBQUEsSUFDTixNQUFNLFNBQVMsT0FBTztBQUFBLElBQ3RCLE9BQU8sU0FBUyxTQUFZO0FBQUEsTUFDMUIsUUFBUTtBQUFBLFFBQ04sUUFBUTtBQUFBLFFBQ1IsY0FBYztBQUFBLE1BQ2hCO0FBQUEsSUFDRjtBQUFBLEVBQ0Y7QUFBQSxFQUNBLE9BQU87QUFBQSxJQUNMLFFBQVE7QUFBQSxJQUNSLFFBQVE7QUFBQSxJQUNSLGNBQWM7QUFBQSxFQUNoQjtBQUFBLEVBQ0EsY0FBYztBQUFBLElBQ1osU0FBUyxTQUFTLENBQUMsMkJBQTJCLE1BQU0sSUFBSTtBQUFBLEVBQzFEO0FBQUEsRUFDQSxNQUFNO0FBQUEsSUFDSixTQUFTO0FBQUEsSUFDVCxhQUFhO0FBQUEsSUFDYixZQUFZO0FBQUEsRUFDZDtBQUNGLENBQUM7IiwKICAibmFtZXMiOiBbXQp9Cg==

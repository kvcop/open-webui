
import { defineConfig } from 'vitest/config'
import { sveltekit } from '@sveltejs/kit/vite'

export default defineConfig({
  plugins: [sveltekit()],
  define: {
    APP_VERSION: JSON.stringify('test'),
    APP_BUILD_HASH: JSON.stringify('test-hash')
  },
  test: {
    include: ['src/**/*.{test,spec}.{js,ts}'],
    globals: true,
    environment: 'jsdom'
  },
  resolve: {
    conditions: ['browser'],
    alias: {
        'y-protocols/awareness': './node_modules/y-protocols/dist/awareness.cjs'
    }
  }
})

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'
// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(),
  ],
  resolve: {
    alias: {
      // 别名配置
      '@': resolve(__dirname, 'src'),
    }
  },
  server: {
    open: true,
  },

  build: {
    rollupOptions: {
      manualChunks(id) {
        if (id.includes('naive-ui')) {
          return 'naive-ui'
        }
        if (id.includes('components') || id.includes('route')) {
          return 'components-route'
        }
        if (id.includes('client')) {
          return 'client'
        }
        if (id.includes('@kangc')) {
          return '@kangc'
        }
        if (id.includes('highlight')) {
          return 'highlight'
        }

      },
      output: {
        entryFileNames: 'js/[name]-[hash].js',
        chunkFileNames: 'js/[name]-[hash].js',
        assetFileNames: 'assets/[name]-[hash].[ext]'
      }
    }
  },
})


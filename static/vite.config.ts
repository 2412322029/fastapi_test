import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'
// https://vitejs.dev/config/
export default defineConfig({
  base:"./",
  plugins: [vue()],
  resolve: {
    alias: {
      // 别名配置
      '@': resolve(__dirname, 'src'),
    }
  },
  server: {
    open:true,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:80/api',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
      '/uploads': {
        target: 'http://127.0.0.1:80/uploads',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/uploads/, ''),
      },

    },
  },
})


import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  base: '/static/',   // ← ここを追加！
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    host: "0.0.0.0",       // ← スマホからアクセス可能に
    port: 3000,            // ← ポート番号（必要なら変更OK）
    strictPort: true,      // ← ポート衝突時に別ポートに移らない
    watch: {
      usePolling: true,    // ← WindowsやWSLでファイル監視エラー対策
    },
  },
})

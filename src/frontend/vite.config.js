import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // 1. Cho phép Docker map port ra ngoài (quan trọng)
    host: true, 
    
    // 2. Cố định port 5173 để khớp với docker-compose
    port: 5173,
    strictPort: true,

    // 3. BẮT BUỘC để sửa code là tự cập nhật (Hot Reload) trên Docker Windows
    watch: {
      usePolling: true,
    },
  }
})
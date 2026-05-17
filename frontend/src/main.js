import axios from 'axios'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { API_BASE } from './config/api.js'
import { setRuntimeMediaOrigin } from './constants/images.js'
import './assets/styles/global.css'

async function bootstrap() {
  try {
    const { data } = await axios.get(`${API_BASE}/config`, { timeout: 8000 })
    if (data?.media_origin && typeof data.media_origin === 'string') {
      const o = data.media_origin.trim().replace(/\/$/, '')
      if (o) setRuntimeMediaOrigin(o)
    }
  } catch {
    /* Sin /api/config sigue solo VITE_BACKEND_ORIGIN / API_BASE en build */
  }
  createApp(App).use(router).mount('#app')
}

bootstrap()

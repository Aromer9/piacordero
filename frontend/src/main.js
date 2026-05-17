import axios from 'axios'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { API_BASE, backendOrigin } from './config/api.js'
import { setRuntimeMediaOrigin } from './constants/images.js'
import './assets/styles/global.css'

async function bootstrap() {
  const fromBuild = backendOrigin()
  try {
    const { data } = await axios.get(`${API_BASE}/config`, { timeout: 8000 })
    const fromApi =
      typeof data?.media_origin === 'string' ? data.media_origin.trim().replace(/\/$/, '') : ''
    // Origen del API en build: no lo pisa /api/config (a veces devuelve el host del SPA y rompe /uploads).
    if (fromBuild) {
      setRuntimeMediaOrigin(fromBuild)
    } else if (fromApi) {
      setRuntimeMediaOrigin(fromApi)
    }
  } catch {
    if (fromBuild) setRuntimeMediaOrigin(fromBuild)
  }
  createApp(App).use(router).mount('#app')
}

bootstrap()

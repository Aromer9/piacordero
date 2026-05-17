/** Origen del backend en producción (Railway), sin barra final. Vacío = mismo host (dev con proxy). */
function backendOrigin() {
  return (import.meta.env.VITE_BACKEND_ORIGIN || '').trim().replace(/\/$/, '')
}

const _origin = backendOrigin()
export const API_BASE = _origin ? `${_origin}/api` : '/api'

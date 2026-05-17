/**
 * Origen del backend (sin `/api` ni barra final).
 * Si `VITE_BACKEND_ORIGIN` incluye `/api` por error, se quita para no generar
 * URLs rotas tipo `…/api/uploads/…` ni `…/api/api/…`.
 */
export function backendOrigin() {
  let o = (import.meta.env.VITE_BACKEND_ORIGIN || '').trim().replace(/\/$/, '')
  while (o.toLowerCase().endsWith('/api')) {
    o = o.slice(0, -4).trim().replace(/\/$/, '')
  }
  return o
}

const _origin = backendOrigin()
export const API_BASE = _origin ? `${_origin}/api` : '/api'

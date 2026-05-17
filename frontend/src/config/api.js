/**
 * Origen del backend (sin `/api` ni barra final).
 * Si `VITE_BACKEND_ORIGIN` incluye `/api` por error, se quita para no generar
 * URLs rotas tipo `…/api/uploads/…` ni `…/api/api/…`.
 */
function normalizeBackendOriginVar(raw) {
  let o = (raw || "").trim().replace(/\/$/, "")
  while (o.toLowerCase().endsWith("/api")) {
    o = o.slice(0, -4).trim().replace(/\/$/, "")
  }
  return o
}

/** Raíz del API absoluta, p. ej. `https://back.up.railway.app/api` (opcional). */
const VITE_API_ROOT = (import.meta.env.VITE_API_ROOT || "").trim()

function originFromApiRoot(root) {
  if (!/^https?:\/\//i.test(root)) return ""
  try {
    return new URL(root).origin
  } catch {
    return ""
  }
}

const _resolvedOrigin =
  normalizeBackendOriginVar(import.meta.env.VITE_BACKEND_ORIGIN || "") ||
  originFromApiRoot(VITE_API_ROOT)

export function backendOrigin() {
  return _resolvedOrigin
}

/** Base del API: mismo origen que `/uploads` en producción. */
export const API_BASE = _resolvedOrigin
  ? `${_resolvedOrigin}/api`
  : /^https?:\/\//i.test(VITE_API_ROOT)
    ? VITE_API_ROOT.replace(/\/$/, "")
    : "/api"

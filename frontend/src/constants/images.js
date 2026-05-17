import { backendOrigin } from '../config/api.js'

/** Imagen por defecto cuando un producto no tiene foto (SVG inline). */
export const PRODUCT_IMAGE_PLACEHOLDER =
  "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='800' height='600' viewBox='0 0 800 600'%3E%3Crect fill='%23EDD9CC' width='800' height='600'/%3E%3Ctext x='400' y='300' dominant-baseline='middle' text-anchor='middle' fill='%23A84F3B' font-family='Georgia,serif' font-size='28' font-style='italic'%3ESin foto%3C/text%3E%3C/svg%3E"

const VIDEO_EXTS = new Set([".mp4", ".webm", ".mov", ".m4v", ".ogg"])

/**
 * Si `pathname` es un recurso bajo uploads, devuelve la ruta normalizada
 * que empieza por `/uploads` (corrige `/api/uploads/...` por error de config).
 */
function uploadsResourcePath(pathname) {
  if (!pathname || typeof pathname !== "string") return null
  const p = pathname.replace(/\/+/g, "/")
  const lower = p.toLowerCase()
  if (lower === "/uploads" || lower.startsWith("/uploads/")) return p
  if (lower === "/api/uploads" || lower.startsWith("/api/uploads/")) {
    return p.replace(/^\/api/i, "")
  }
  return null
}

/**
 * Sirve `/uploads/...` desde el backend de producción (`VITE_BACKEND_ORIGIN`).
 * También corrige URLs absolutas guardadas en dev (p. ej. `http://localhost:8001/uploads/...`),
 * que en producción apuntarían a un host inexistente para el visitante.
 */
export function mediaSrc(url) {
  const u = typeof url === "string" ? url.trim() : ""
  if (!u) return u
  const o = backendOrigin()
  if (!o) return u

  if (u.startsWith("/")) {
    const q = u.indexOf("?")
    const pathOnly = q >= 0 ? u.slice(0, q) : u
    const search = q >= 0 ? u.slice(q) : ""
    const mapped = uploadsResourcePath(pathOnly)
    if (mapped) return `${o}${mapped}${search}`
  }

  const lower = u.toLowerCase()
  if (lower.startsWith("uploads/")) return `${o}/${u}`

  if (/^https?:\/\//i.test(u)) {
    try {
      const { pathname, search } = new URL(u)
      const mapped = uploadsResourcePath(pathname)
      if (mapped) return `${o}${mapped}${search}`
    } catch {
      /* URL inválida: se devuelve tal cual */
    }
  }

  return u
}

/** Si `url` viene vacío del CMS, usa `fallback`; si es `/uploads/...`, antepone el backend. */
export function resolvePublicOrUpload(url, fallback = "") {
  const fb = typeof fallback === "string" ? fallback.trim() : ""
  const u = typeof url === "string" ? url.trim() : ""
  return mediaSrc(u || fb)
}

/** Devuelve true si la URL apunta a un archivo de vídeo. */
export function isVideo(url) {
  if (!url || typeof url !== "string") return false
  const ext = url.split("?")[0].split(".").pop().toLowerCase()
  return VIDEO_EXTS.has(`.${ext}`)
}

export function productImageSrc(url) {
  const raw = typeof url === "string" ? url.trim() : ""
  const u = mediaSrc(raw) || raw
  return u || PRODUCT_IMAGE_PLACEHOLDER
}

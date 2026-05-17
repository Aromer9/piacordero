/** Imagen por defecto cuando un producto no tiene foto (SVG inline). */
export const PRODUCT_IMAGE_PLACEHOLDER =
  "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='800' height='600' viewBox='0 0 800 600'%3E%3Crect fill='%23EDD9CC' width='800' height='600'/%3E%3Ctext x='400' y='300' dominant-baseline='middle' text-anchor='middle' fill='%23A84F3B' font-family='Georgia,serif' font-size='28' font-style='italic'%3ESin foto%3C/text%3E%3C/svg%3E"

const VIDEO_EXTS = new Set([".mp4", ".webm", ".mov", ".m4v", ".ogg"])

/** Devuelve true si la URL apunta a un archivo de vídeo. */
export function isVideo(url) {
  if (!url || typeof url !== "string") return false
  const ext = url.split("?")[0].split(".").pop().toLowerCase()
  return VIDEO_EXTS.has(`.${ext}`)
}

export function productImageSrc(url) {
  const u = typeof url === "string" ? url.trim() : ""
  return u || PRODUCT_IMAGE_PLACEHOLDER
}

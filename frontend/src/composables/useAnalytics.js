import axios from 'axios'
import { API_BASE } from '../config/api.js'

// Genera un session_id único por pestaña (se pierde al cerrar)
function getSessionId() {
  let sid = sessionStorage.getItem('_pia_sid')
  if (!sid) {
    sid = crypto.randomUUID()
    sessionStorage.setItem('_pia_sid', sid)
  }
  return sid
}

const SESSION_ID = getSessionId()
const FLUSH_INTERVAL_MS = 10_000
const ENDPOINT = `${API_BASE}/analytics/event`

let queue = []
let flushTimer = null
let pageEntryTime = null
let currentPage = null
let maxScroll = 0
let scrollListenerAdded = false

function now() {
  return new Date().toISOString()
}

function push(event) {
  queue.push({ ...event, session_id: SESSION_ID, timestamp: now() })
}

async function flush() {
  if (!queue.length) return
  const batch = queue.splice(0)
  try {
    await axios.post(ENDPOINT, { events: batch }, { timeout: 5000 })
  } catch {
    // Descartamos silenciosamente para no afectar la UX
  }
}

function scheduleFlush() {
  if (flushTimer) return
  flushTimer = setInterval(flush, FLUSH_INTERVAL_MS)
}

function stopFlush() {
  if (flushTimer) {
    clearInterval(flushTimer)
    flushTimer = null
  }
}

// --- Scroll depth ---

function onScroll() {
  const scrolled = window.scrollY + window.innerHeight
  const total = document.documentElement.scrollHeight
  if (total > 0) {
    const percent = Math.round((scrolled / total) * 100)
    if (percent > maxScroll) maxScroll = percent
  }
}

function attachScrollListener() {
  if (scrollListenerAdded) return
  window.addEventListener('scroll', onScroll, { passive: true })
  scrollListenerAdded = true
}

function flushScrollDepth(page) {
  if (maxScroll > 0 && page) {
    push({ type: 'scroll_depth', page, max_percent: maxScroll })
  }
  maxScroll = 0
}

// --- Time on page ---

function flushTimeOnPage(page) {
  if (pageEntryTime && page) {
    const duration_ms = Date.now() - pageEntryTime
    if (duration_ms > 500) {
      push({ type: 'time_on_page', page, duration_ms })
    }
  }
}

// --- Clicks ---

const INTERACTIVE_TAGS = new Set(['button', 'a', 'input', 'select', 'textarea', 'img', 'video', 'svg'])

/**
 * Sube en el DOM hasta encontrar el primer ancestro interactivo significativo.
 * Para img/video/svg retorna el elemento directamente sin subir.
 */
function findInteractiveAncestor(el) {
  const selfTag = el.tagName?.toLowerCase()
  // Elementos que son significativos por sí mismos — no subir
  if (['img', 'video', 'svg'].includes(selfTag)) return el

  let node = el
  for (let i = 0; i < 6 && node && node !== document.body; i++) {
    const tag = node.tagName?.toLowerCase()
    if (INTERACTIVE_TAGS.has(tag)) return node
    if (node.hasAttribute?.('data-track')) return node
    node = node.parentElement
  }
  return el
}

/**
 * Determina la sección semántica más cercana (id de <section> o <header>/<footer>).
 */
function findSection(el) {
  let node = el
  while (node && node !== document.body) {
    const tag = node.tagName?.toLowerCase()
    if (['section', 'header', 'footer', 'main', 'nav'].includes(tag)) {
      return node.id || node.className?.split(' ')[0] || tag
    }
    node = node.parentElement
  }
  return null
}

/**
 * Extrae una etiqueta legible priorizando atributos semánticos.
 */
function extractLabel(el) {
  const tag = el.tagName?.toLowerCase()

  // Para imágenes: alt > nombre del archivo en src
  if (tag === 'img') {
    const alt = el.getAttribute('alt')?.trim()
    if (alt) return alt
    const src = el.getAttribute('src') || ''
    const filename = src.split('/').pop()?.split('?')[0]
    return filename ? `img: ${filename.slice(0, 40)}` : 'img sin alt'
  }

  // Para links: texto visible > href limpio
  if (tag === 'a') {
    const text = el.innerText?.replace(/\s+/g, ' ').trim().slice(0, 50)
    if (text) return text
    const href = el.getAttribute('href') || ''
    return href.replace(/^https?:\/\/[^/]+/, '').slice(0, 50) || href.slice(0, 50)
  }

  // Orden general
  return (
    el.getAttribute('data-track') ||
    el.getAttribute('aria-label') ||
    el.getAttribute('title') ||
    el.getAttribute('placeholder') ||
    el.innerText?.replace(/\s+/g, ' ').trim().slice(0, 50) ||
    null
  )
}

function onDocumentClick(e) {
  const target = e.target
  if (!target || !currentPage) return

  // Ignorar clics dentro del panel admin
  if (currentPage.startsWith('/admin')) return

  const interactive = findInteractiveAncestor(target)
  const tag = interactive.tagName?.toLowerCase() || ''
  const label = extractLabel(interactive)
  const section = findSection(interactive)

  push({
    type: 'click',
    page: currentPage,
    element_tag: tag,
    element_label: label || null,
    section: section || null,
    x: Math.round(e.clientX),
    y: Math.round(e.clientY),
  })
}

function attachClickListener() {
  document.addEventListener('click', onDocumentClick, { passive: true })
}

// --- Visibilidad (flush al cambiar de pestaña o cerrar) ---

function onVisibilityChange() {
  if (document.visibilityState === 'hidden') {
    flushTimeOnPage(currentPage)
    flushScrollDepth(currentPage)
    flush()
  }
}

// --- API pública ---

export function initAnalytics() {
  attachScrollListener()
  attachClickListener()
  document.addEventListener('visibilitychange', onVisibilityChange)
  window.addEventListener('beforeunload', () => {
    flushTimeOnPage(currentPage)
    flushScrollDepth(currentPage)
    flush()
  })
  scheduleFlush()
}

export function trackPageView(page, referrer) {
  // Cerrar métricas de la página anterior
  if (currentPage) {
    flushTimeOnPage(currentPage)
    flushScrollDepth(currentPage)
  }

  currentPage = page
  pageEntryTime = Date.now()
  maxScroll = 0

  push({
    type: 'page_view',
    page,
    referrer: referrer || document.referrer || null,
    user_agent: navigator.userAgent || null,
  })
}

export function stopAnalytics() {
  stopFlush()
}

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

function onDocumentClick(e) {
  const target = e.target
  if (!target || !currentPage) return

  // Ignorar clics dentro del panel admin
  if (currentPage.startsWith('/admin')) return

  const tag = target.tagName?.toLowerCase() || ''
  const label =
    target.getAttribute('aria-label') ||
    target.getAttribute('data-label') ||
    target.innerText?.trim().slice(0, 60) ||
    target.getAttribute('href') ||
    null

  push({
    type: 'click',
    page: currentPage,
    element_tag: tag,
    element_label: label || null,
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

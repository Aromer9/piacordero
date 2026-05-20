<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { API_BASE } from '../../config/api.js'
import { getToken } from '../../composables/useAuth.js'

const loading = ref(true)
const error = ref(null)
const data = ref(null)
const days = ref(30)

async function load() {
  loading.value = true
  error.value = null
  try {
    const token = getToken()
    const res = await axios.get(`${API_BASE}/analytics/summary`, {
      params: { days: days.value },
      headers: { Authorization: `Bearer ${token}` },
    })
    data.value = res.data
  } catch (e) {
    error.value = 'No se pudo cargar el resumen de analytics.'
  } finally {
    loading.value = false
  }
}

onMounted(load)

function formatSeconds(s) {
  if (s == null) return '—'
  if (s < 60) return `${s}s`
  return `${Math.floor(s / 60)}m ${Math.round(s % 60)}s`
}

function formatPage(p) {
  return p === '/' ? 'Inicio' : p
}

const totalVisits = computed(() => {
  if (!data.value) return 0
  return data.value.page_views.reduce((acc, r) => acc + r.visits, 0)
})

// --- Gráfico de línea SVG ---
const W = 700
const H = 160
const PAD = { top: 16, right: 16, bottom: 32, left: 36 }

const lineTooltip = ref(null) // { x, y, date, visits }

const lineChart = computed(() => {
  const pts = data.value?.daily_visits ?? []
  if (pts.length < 2) return null

  const maxVal = Math.max(...pts.map(p => p.visits), 1)
  const minVal = 0

  const innerW = W - PAD.left - PAD.right
  const innerH = H - PAD.top - PAD.bottom

  function cx(i) {
    return PAD.left + (i / (pts.length - 1)) * innerW
  }
  function cy(v) {
    return PAD.top + innerH - ((v - minVal) / (maxVal - minVal)) * innerH
  }

  const points = pts.map((p, i) => ({ x: cx(i), y: cy(p.visits), date: p.date, visits: p.visits }))

  // Polilínea
  const polyline = points.map(p => `${p.x},${p.y}`).join(' ')

  // Área rellena (cierra abajo)
  const area = [
    `M${points[0].x},${PAD.top + innerH}`,
    ...points.map(p => `L${p.x},${p.y}`),
    `L${points[points.length - 1].x},${PAD.top + innerH}`,
    'Z',
  ].join(' ')

  // Etiquetas del eje X: máximo ~6 etiquetas distribuidas
  const step = Math.ceil(pts.length / 6)
  const xLabels = pts
    .map((p, i) => ({ i, date: p.date, x: cx(i) }))
    .filter((_, i) => i % step === 0 || i === pts.length - 1)

  // Líneas de guía horizontales (4 niveles)
  const yGuides = [0, 0.25, 0.5, 0.75, 1].map(t => ({
    y: PAD.top + innerH - t * innerH,
    label: Math.round(minVal + t * (maxVal - minVal)),
  }))

  return { points, polyline, area, xLabels, yGuides, maxVal }
})

function onLineMouseMove(e) {
  if (!lineChart.value) return
  const svg = e.currentTarget
  const rect = svg.getBoundingClientRect()
  const scaleX = W / rect.width
  const mouseX = (e.clientX - rect.left) * scaleX

  const pts = lineChart.value.points
  let closest = pts[0]
  let minDist = Infinity
  for (const p of pts) {
    const d = Math.abs(p.x - mouseX)
    if (d < minDist) { minDist = d; closest = p }
  }
  lineTooltip.value = { x: closest.x, y: closest.y, date: closest.date, visits: closest.visits }
}

function onLineMouseLeave() {
  lineTooltip.value = null
}
</script>

<template>
  <div class="an">
    <div class="an__header">
      <div>
        <h1 class="an__title">Analytics</h1>
        <p class="an__subtitle">Comportamiento real de visitantes</p>
      </div>
      <div class="an__controls">
        <select v-model.number="days" @change="load" class="an__select">
          <option :value="7">Últimos 7 días</option>
          <option :value="30">Últimos 30 días</option>
          <option :value="90">Últimos 90 días</option>
          <option :value="365">Último año</option>
        </select>
        <button class="an__refresh" @click="load" :disabled="loading">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/>
            <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/>
          </svg>
          Actualizar
        </button>
      </div>
    </div>

    <div v-if="loading" class="an__loading">Cargando datos...</div>
    <div v-else-if="error" class="an__error">{{ error }}</div>

    <template v-else-if="data">
      <!-- KPIs top -->
      <div class="an__kpis">
        <div class="an__kpi">
          <span class="an__kpi-value">{{ data.unique_sessions.toLocaleString() }}</span>
          <span class="an__kpi-label">Sesiones únicas</span>
        </div>
        <div class="an__kpi">
          <span class="an__kpi-value">{{ totalVisits.toLocaleString() }}</span>
          <span class="an__kpi-label">Páginas vistas</span>
        </div>
        <div class="an__kpi">
          <span class="an__kpi-value">{{ data.period_days }}d</span>
          <span class="an__kpi-label">Período analizado</span>
        </div>
      </div>

      <!-- Gráfico de línea: visitas diarias -->
      <div v-if="data.daily_visits?.length" class="an__card">
        <h2 class="an__card-title">Visitas por día</h2>

        <div v-if="!lineChart" class="an__empty" style="padding: 20px 0">
          Se necesitan al menos 2 días de datos para mostrar el gráfico.
        </div>

        <div v-else class="an__line-wrap">
          <svg
            :viewBox="`0 0 ${700} ${160}`"
            class="an__line-svg"
            @mousemove="onLineMouseMove"
            @mouseleave="onLineMouseLeave"
          >
            <!-- Guías horizontales -->
            <g class="an__guides">
              <line
                v-for="g in lineChart.yGuides"
                :key="g.y"
                :x1="PAD.left" :y1="g.y"
                :x2="700 - PAD.right" :y2="g.y"
                stroke="#ede6df" stroke-width="1"
              />
              <text
                v-for="g in lineChart.yGuides"
                :key="`l${g.y}`"
                :x="PAD.left - 6" :y="g.y + 4"
                text-anchor="end"
                class="an__axis-label"
              >{{ g.label }}</text>
            </g>

            <!-- Área rellena -->
            <defs>
              <linearGradient id="lineGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0%" stop-color="#c4614a" stop-opacity="0.18"/>
                <stop offset="100%" stop-color="#c4614a" stop-opacity="0"/>
              </linearGradient>
            </defs>
            <path :d="lineChart.area" fill="url(#lineGrad)" />

            <!-- Línea principal -->
            <polyline
              :points="lineChart.polyline"
              fill="none"
              stroke="#c4614a"
              stroke-width="2"
              stroke-linejoin="round"
              stroke-linecap="round"
            />

            <!-- Etiquetas eje X -->
            <text
              v-for="lbl in lineChart.xLabels"
              :key="lbl.date"
              :x="lbl.x" :y="160 - PAD.bottom + 14"
              text-anchor="middle"
              class="an__axis-label"
            >{{ lbl.date.slice(5) }}</text>

            <!-- Punto hover + línea vertical -->
            <template v-if="lineTooltip">
              <line
                :x1="lineTooltip.x" y1="16"
                :x2="lineTooltip.x" :y2="160 - 32"
                stroke="#c4614a" stroke-width="1" stroke-dasharray="4 3" opacity="0.5"
              />
              <circle
                :cx="lineTooltip.x" :cy="lineTooltip.y"
                r="4" fill="#c4614a" stroke="#fff" stroke-width="2"
              />
            </template>
          </svg>

          <!-- Tooltip flotante -->
          <div
            v-if="lineTooltip"
            class="an__line-tooltip"
            :style="{
              left: `${(lineTooltip.x / 700) * 100}%`,
              top: `${(lineTooltip.y / 160) * 100}%`,
            }"
          >
            <span class="an__tooltip-date">{{ lineTooltip.date }}</span>
            <span class="an__tooltip-val">{{ lineTooltip.visits }} visitas</span>
          </div>
        </div>
      </div>

      <div class="an__grid">
        <!-- Páginas más visitadas -->
        <div class="an__card">
          <h2 class="an__card-title">Páginas más visitadas</h2>
          <table class="an__table">
            <thead>
              <tr><th>Página</th><th>Visitas</th></tr>
            </thead>
            <tbody>
              <tr v-for="row in data.page_views" :key="row.page">
                <td>{{ formatPage(row.page) }}</td>
                <td class="an__td-num">{{ row.visits }}</td>
              </tr>
              <tr v-if="!data.page_views.length">
                <td colspan="2" class="an__empty">Sin datos aún</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Tiempo promedio por página -->
        <div class="an__card">
          <h2 class="an__card-title">Tiempo promedio por página</h2>
          <table class="an__table">
            <thead>
              <tr><th>Página</th><th>Promedio</th><th>Sesiones</th></tr>
            </thead>
            <tbody>
              <tr v-for="row in data.avg_time_on_page" :key="row.page">
                <td>{{ formatPage(row.page) }}</td>
                <td class="an__td-num">{{ formatSeconds(row.avg_seconds) }}</td>
                <td class="an__td-num">{{ row.sessions }}</td>
              </tr>
              <tr v-if="!data.avg_time_on_page.length">
                <td colspan="3" class="an__empty">Sin datos aún</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Scroll depth -->
        <div class="an__card">
          <h2 class="an__card-title">Profundidad de scroll</h2>
          <table class="an__table">
            <thead>
              <tr><th>Página</th><th>Scroll prom.</th><th>Sesiones</th></tr>
            </thead>
            <tbody>
              <tr v-for="row in data.scroll_depth" :key="row.page">
                <td>{{ formatPage(row.page) }}</td>
                <td class="an__td-num">
                  <div class="an__scroll-bar">
                    <div class="an__scroll-fill" :style="{ width: `${row.avg_scroll_percent}%` }"></div>
                    <span>{{ row.avg_scroll_percent }}%</span>
                  </div>
                </td>
                <td class="an__td-num">{{ row.sessions }}</td>
              </tr>
              <tr v-if="!data.scroll_depth.length">
                <td colspan="3" class="an__empty">Sin datos aún</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Clics más frecuentes -->
        <div class="an__card">
          <h2 class="an__card-title">Elementos más clickeados</h2>
          <table class="an__table">
            <thead>
              <tr><th>Tipo</th><th>Etiqueta</th><th>Sección</th><th>Clics</th></tr>
            </thead>
            <tbody>
              <tr v-for="(row, i) in data.top_clicks" :key="i">
                <td>
                  <span class="an__tag-badge" :class="`an__tag--${row.tag || 'other'}`">
                    {{ row.tag || '?' }}
                  </span>
                </td>
                <td class="an__td-label" :title="row.label || ''">
                  {{ row.label || '—' }}
                </td>
                <td class="an__td-section">{{ row.section || '—' }}</td>
                <td class="an__td-num">{{ row.count }}</td>
              </tr>
              <tr v-if="!data.top_clicks.length">
                <td colspan="4" class="an__empty">Sin datos aún</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>
  </div>
</template>

<style scoped>
.an {
  max-width: 1100px;
}

.an__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 32px;
}

.an__title {
  font-family: var(--font-serif);
  font-size: 1.6rem;
  font-weight: 500;
  color: var(--color-bg-dark);
  margin: 0 0 4px;
}

.an__subtitle {
  font-size: 0.8rem;
  color: #8c7b6e;
  margin: 0;
}

.an__controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

.an__select {
  font-family: var(--font-sans);
  font-size: 0.8rem;
  padding: 8px 12px;
  border: 1px solid #d9cfc8;
  border-radius: 8px;
  background: #fff;
  color: var(--color-bg-dark);
  cursor: pointer;
}

.an__refresh {
  display: flex;
  align-items: center;
  gap: 6px;
  font-family: var(--font-sans);
  font-size: 0.8rem;
  padding: 8px 14px;
  background: var(--color-bg-dark);
  color: var(--color-text-dark-bg);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: opacity 0.2s;
}

.an__refresh:disabled { opacity: 0.5; cursor: not-allowed; }

.an__loading {
  text-align: center;
  padding: 60px;
  color: #8c7b6e;
  font-size: 0.9rem;
}

.an__error {
  background: #fde8e4;
  color: #c0392b;
  padding: 16px 20px;
  border-radius: 10px;
  font-size: 0.85rem;
}

.an__kpis {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.an__kpi {
  background: #fff;
  border-radius: 12px;
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  box-shadow: 0 1px 4px rgba(28,16,8,0.06);
}

.an__kpi-value {
  font-family: var(--font-serif);
  font-size: 2rem;
  font-weight: 500;
  color: var(--color-bg-dark);
}

.an__kpi-label {
  font-size: 0.72rem;
  color: #8c7b6e;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.an__card {
  background: #fff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 1px 4px rgba(28,16,8,0.06);
  margin-bottom: 24px;
}

.an__card-title {
  font-family: var(--font-serif);
  font-size: 1rem;
  font-weight: 500;
  color: var(--color-bg-dark);
  margin: 0 0 16px;
}

/* Gráfico de línea */
.an__line-wrap {
  position: relative;
}

.an__line-svg {
  width: 100%;
  height: auto;
  display: block;
  cursor: crosshair;
}

.an__axis-label {
  font-size: 9px;
  fill: #b0a096;
  font-family: var(--font-sans, sans-serif);
}

.an__line-tooltip {
  position: absolute;
  transform: translate(-50%, -120%);
  background: var(--color-bg-dark, #2a1a10);
  color: #fff;
  border-radius: 8px;
  padding: 6px 10px;
  pointer-events: none;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1px;
  white-space: nowrap;
  font-size: 0.75rem;
  box-shadow: 0 4px 12px rgba(28,16,8,0.2);
}

.an__tooltip-date {
  font-size: 0.65rem;
  opacity: 0.65;
}

.an__tooltip-val {
  font-family: var(--font-serif, serif);
  font-size: 0.9rem;
}

/* Tablas */
.an__grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.an__table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.82rem;
}

.an__table th {
  text-align: left;
  font-weight: 500;
  color: #8c7b6e;
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding: 0 0 10px;
  border-bottom: 1px solid #ede6df;
}

.an__table td {
  padding: 10px 0;
  border-bottom: 1px solid #f4ede6;
  color: var(--color-bg-dark);
}

.an__td-num {
  text-align: right;
  font-variant-numeric: tabular-nums;
  color: #5c4a3a;
}

.an__td-label {
  max-width: 180px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  cursor: default;
}

.an__td-section {
  font-size: 0.75rem;
  color: #8c7b6e;
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.an__tag-badge {
  display: inline-block;
  font-size: 0.65rem;
  font-weight: 600;
  letter-spacing: 0.04em;
  padding: 2px 7px;
  border-radius: 4px;
  text-transform: lowercase;
  background: #f0e9e3;
  color: #7a5c4a;
}

.an__tag--button,
.an__tag--a {
  background: #fde8e0;
  color: #c4614a;
}

.an__tag--input,
.an__tag--select,
.an__tag--textarea {
  background: #e8f0e0;
  color: #5a7a40;
}

.an__tag--img {
  background: #e8eaf0;
  color: #4a5a7a;
}

.an__empty {
  text-align: center;
  color: #b0a096;
  padding: 20px 0;
  font-size: 0.8rem;
}

.an__scroll-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  justify-content: flex-end;
}

.an__scroll-fill {
  height: 6px;
  background: var(--color-rose-mid, #c4614a);
  border-radius: 3px;
  min-width: 2px;
  max-width: 80px;
}

@media (max-width: 900px) {
  .an__grid { grid-template-columns: 1fr; }
  .an__kpis { grid-template-columns: 1fr 1fr; }
}

@media (max-width: 600px) {
  .an__kpis { grid-template-columns: 1fr; }
}
</style>

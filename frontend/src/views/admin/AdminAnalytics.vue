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

      <!-- Gráfico de visitas diarias -->
      <div v-if="data.daily_visits?.length" class="an__card">
        <h2 class="an__card-title">Visitas por día</h2>
        <div class="an__bar-chart">
          <div
            v-for="d in data.daily_visits"
            :key="d.date"
            class="an__bar-wrap"
            :title="`${d.date}: ${d.visits} visitas`"
          >
            <div
              class="an__bar"
              :style="{
                height: `${Math.round((d.visits / Math.max(...data.daily_visits.map(x => x.visits))) * 100)}%`
              }"
            ></div>
            <span class="an__bar-label">{{ d.date.slice(5) }}</span>
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
              <tr><th>Elemento</th><th>Página</th><th>Clics</th></tr>
            </thead>
            <tbody>
              <tr v-for="(row, i) in data.top_clicks" :key="i">
                <td class="an__td-label">{{ row.label || row.tag || '—' }}</td>
                <td>{{ formatPage(row.page) }}</td>
                <td class="an__td-num">{{ row.count }}</td>
              </tr>
              <tr v-if="!data.top_clicks.length">
                <td colspan="3" class="an__empty">Sin datos aún</td>
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

/* Gráfico de barras */
.an__bar-chart {
  display: flex;
  align-items: flex-end;
  gap: 4px;
  height: 100px;
  overflow-x: auto;
  padding-bottom: 4px;
}

.an__bar-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  min-width: 28px;
  flex: 1;
  height: 100%;
  justify-content: flex-end;
}

.an__bar {
  width: 100%;
  background: var(--color-rose-mid, #c4614a);
  border-radius: 3px 3px 0 0;
  min-height: 2px;
  transition: height 0.3s;
}

.an__bar-label {
  font-size: 0.55rem;
  color: #8c7b6e;
  white-space: nowrap;
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
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
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

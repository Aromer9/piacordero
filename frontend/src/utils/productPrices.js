/** Formatea precio en pesos chilenos */
export function formatMoneyCLP(value) {
  if (value == null || value === '') return null
  const n = Number(value)
  if (!Number.isFinite(n)) return null
  return new Intl.NumberFormat('es-CL', {
    style: 'currency',
    currency: 'CLP',
    maximumFractionDigits: 0,
  }).format(n)
}

/** Convierte input de formulario a número o null (acepta string con espacios; CLP sin decimales) */
export function numOrNull(v) {
  if (v === '' || v == null) return null
  if (typeof v === 'number') return Number.isFinite(v) ? Math.trunc(v) : null
  const s = String(v).trim().replace(/\s/g, '').replace(/\./g, '').replace(/,/g, '')
  if (s === '') return null
  const n = Number(s)
  return Number.isFinite(n) ? Math.trunc(n) : null
}

export function hasTierPrices(product) {
  if (!product) return false
  return [
    product.price_8_10p,
    product.price_15p,
    product.price_20p,
    product.price_30p,
  ].some((x) => x != null && x !== '' && Number.isFinite(Number(x)))
}

function numericTier(v) {
  if (v == null || v === '') return null
  const n = Number(v)
  return Number.isFinite(n) ? n : null
}

/** Filas para modal / detalle: tartas incluyen 8–10 p.; el resto 15 / 20 / 30 */
export function tierPriceRowsForDetail(product) {
  if (!product) return []
  const isTartas = product.category === 'tartas'
  let p810 = isTartas ? numericTier(product.price_8_10p) : null
  let p15 = numericTier(product.price_15p)
  let p20 = numericTier(product.price_20p)
  let p30 = numericTier(product.price_30p)
  const anyExplicit =
    p810 != null || p15 != null || p20 != null || p30 != null
  if (!anyExplicit) {
    const leg = numericTier(product.price)
    if (leg != null) p15 = leg
  }
  const row = (key, label, cents) => ({
    size: key,
    label,
    formatted: cents != null ? formatMoneyCLP(cents) : null,
  })
  const rows = []
  if (isTartas) {
    rows.push(row('8-10', '8 a 10 personas', p810))
  }
  rows.push(row(15, '15 personas', p15), row(20, '20 personas', p20), row(30, '30 personas', p30))
  return rows
}

/** Líneas de precios por tamaño (para cards compactas) */
export function tierPricesSummary(product) {
  if (!product) return null
  const lines = []
  if (product.category === 'tartas' && product.price_8_10p) {
    lines.push(`8–10 p.: ${formatMoneyCLP(product.price_8_10p)}`)
  }
  if (product.price_15p) lines.push(`15 p.: ${formatMoneyCLP(product.price_15p)}`)
  if (product.price_20p) lines.push(`20 p.: ${formatMoneyCLP(product.price_20p)}`)
  if (product.price_30p) lines.push(`30 p.: ${formatMoneyCLP(product.price_30p)}`)
  return lines.length ? lines : null
}

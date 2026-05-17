<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { productImageSrc, isVideo, mediaSrc, PRODUCT_IMAGE_PLACEHOLDER } from '../../constants/images.js'
import { hasTierPrices, tierPricesSummary, tierPriceRowsForDetail } from '../../utils/productPrices.js'

const props = defineProps({
  products: {
    type: Array,
    default: () => [],
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

const categories = [
  { value: 'all', label: 'Todas' },
  { value: 'tortas', label: 'Tortas' },
  { value: 'tartas', label: 'Tartas' },
  { value: 'petit_fours', label: 'Petit Fours' },
  { value: 'temporada', label: 'Temporada' },
]

const CATEGORY_LABELS = {
  tortas: 'Tortas',
  tartas: 'Tartas',
  petit_fours: 'Petit Fours',
  temporada: 'Temporada',
}

const activeCategory = ref('all')
const selectedProduct = ref(null)

const filtered = computed(() => {
  if (activeCategory.value === 'all') return props.products
  return props.products.filter((p) => p.category === activeCategory.value)
})

const featured = computed(() => props.products.filter((p) => p.featured))

/** Productos cuya foto principal falló al cargar (Vue no debe reaplicar la URL rota). */
const failedProductImages = ref(new Set())

function productMediaId(product) {
  const id = product?._id ?? product?.id
  if (id != null && id !== "") return String(id)
  const img = (product?.image_url || "").trim()
  if (img) return `u:${img}`
  const name = (product?.name || "").trim()
  if (name) return `n:${name}`
  return ""
}

function productCardSrc(product) {
  const pid = productMediaId(product)
  if (pid && failedProductImages.value.has(pid)) return PRODUCT_IMAGE_PLACEHOLDER
  return productImageSrc(product?.image_url)
}

function onProductImgError(product) {
  const pid = productMediaId(product)
  if (!pid || failedProductImages.value.has(pid)) return
  failedProductImages.value = new Set([...failedProductImages.value, pid])
}

watch(featured, () => nextTick(updateScrollState))

watch(selectedProduct, (p, _prev, onCleanup) => {
  if (!p) return
  document.body.style.overflow = 'hidden'
  const onKey = (e) => {
    if (e.key === 'Escape') selectedProduct.value = null
  }
  window.addEventListener('keydown', onKey)
  onCleanup(() => {
    document.body.style.overflow = ''
    window.removeEventListener('keydown', onKey)
  })
})

function openDetail(product) {
  selectedProduct.value = product
}

function closeDetail() {
  selectedProduct.value = null
}

function openWhatsApp(productName) {
  const msg = encodeURIComponent(`Hola Pía! Me gustaría pedir: ${productName} 🎂`)
  window.open(`https://wa.me/56989646783?text=${msg}`, '_blank')
}

function formatPrice(price) {
  if (!price) return null
  return new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP', maximumFractionDigits: 0 }).format(price)
}

function productPriceLines(product) {
  if (hasTierPrices(product)) return tierPricesSummary(product)
  return null
}

function categoryLabel(product) {
  if (!product?.category) return ''
  return CATEGORY_LABELS[product.category] || product.category
}

// ── Scroll horizontal "Lo más pedido" ──────────────────────────────────
const featuredTrackRef = ref(null)
const canScrollLeft = ref(false)
const canScrollRight = ref(false)

function updateScrollState() {
  const el = featuredTrackRef.value
  if (!el) return
  canScrollLeft.value = el.scrollLeft > 4
  canScrollRight.value = el.scrollLeft + el.clientWidth < el.scrollWidth - 4
}

function scrollFeatured(dir) {
  const el = featuredTrackRef.value
  if (!el) return
  const card = el.querySelector('.featured__card')
  const amount = card ? card.offsetWidth + 20 : 300
  el.scrollBy({ left: dir * amount, behavior: 'smooth' })
}

onMounted(() => {
  nextTick(() => {
    updateScrollState()
    featuredTrackRef.value?.addEventListener('scroll', updateScrollState, { passive: true })
    window.addEventListener('resize', updateScrollState, { passive: true })
  })
})

onBeforeUnmount(() => {
  featuredTrackRef.value?.removeEventListener('scroll', updateScrollState)
  window.removeEventListener('resize', updateScrollState)
})
</script>

<template>
  <!-- Galería masonry -->
  <section id="galeria" class="gallery">
    <div class="container">
      <header class="gallery__header">
        <p class="eyebrow fade-in">Galería</p>
        <div class="gallery__header-row">
          <h2 class="gallery__title fade-up">
            Mis últimas<br /><em>creaciones</em>
          </h2>
          <a class="gallery__see-all fade-in" href="#" @click.prevent="activeCategory = 'all'">Ver todo →</a>
        </div>
      </header>

      <nav class="gallery__filters fade-up" data-delay="80">
        <button
          v-for="cat in categories"
          :key="cat.value"
          class="gallery__filter-btn"
          :class="{ active: activeCategory === cat.value }"
          @click="activeCategory = cat.value"
        >
          {{ cat.label }}
        </button>
      </nav>

      <div v-if="loading" class="gallery__grid">
        <div class="gallery__skeleton" v-for="n in 8" :key="n" />
      </div>

      <div v-else class="gallery__grid">
        <div
          v-for="(product, i) in filtered"
          :key="product._id"
          class="gallery__item fade-up"
          :data-delay="(i % 4) * 60"
          data-hover
          role="button"
          tabindex="0"
          :aria-label="'Ver detalles de ' + product.name"
          @click="openDetail(product)"
          @keydown.enter.prevent="openDetail(product)"
          @keydown.space.prevent="openDetail(product)"
        >
          <video
            v-if="isVideo(product.image_url)"
            :src="mediaSrc(product.image_url)"
            class="gallery__img"
            muted
            loop
            autoplay
            playsinline
          />
          <img
            v-else
            :src="productCardSrc(product)"
            :alt="product.name"
            loading="lazy"
            class="gallery__img"
            @error="onProductImgError(product)"
          />
          <div class="gallery__overlay">
            <h3 class="gallery__overlay-name">{{ product.name }}</h3>
            <span class="gallery__overlay-cta">Ver detalles →</span>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- Lo más pedido - cards con precio -->
  <section id="creaciones" class="featured">
    <div class="container">
      <header class="featured__header">
        <p class="eyebrow fade-in">Especialidades</p>
        <h2 class="featured__title fade-up">
          Lo más <em>pedido</em>
        </h2>
      </header>

      <div class="featured__carousel">
        <!-- flecha izquierda -->
        <button
          v-show="canScrollLeft"
          type="button"
          class="featured__arrow featured__arrow--left"
          aria-label="Anterior"
          @click="scrollFeatured(-1)"
        >
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true">
            <path d="M13 4l-6 6 6 6" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>

        <div v-if="loading" class="featured__track featured__track--loading">
          <div class="featured__skeleton" v-for="n in 4" :key="n" />
        </div>

        <div v-else ref="featuredTrackRef" class="featured__track">
          <article
            v-for="(product, i) in featured"
            :key="product._id"
            class="featured__card fade-up"
            :data-delay="i * 80"
            data-hover
          >
          <div class="featured__card-img-wrap" role="button" tabindex="0" @click="openDetail(product)" @keydown.enter.prevent="openDetail(product)" @keydown.space.prevent="openDetail(product)">
            <video
              v-if="isVideo(product.image_url)"
              :src="mediaSrc(product.image_url)"
              muted loop autoplay playsinline
              style="width:100%;height:100%;object-fit:cover;object-position:center 20%"
            />
            <img
              v-else
              :src="productCardSrc(product)"
              :alt="product.name"
              loading="lazy"
              @error="onProductImgError(product)"
            />
            <span v-if="product.badge" class="featured__card-badge">{{ product.badge }}</span>
          </div>
          <div class="featured__card-body">
            <h3 class="featured__card-name">{{ product.name }}</h3>
            <p class="featured__card-desc">{{ product.description }}</p>
            <button type="button" class="featured__card-more" @click.stop="openDetail(product)">
              Ver detalles
            </button>
            <div class="featured__card-footer">
              <div v-if="productPriceLines(product)?.length" class="featured__card-price-block">
                <span
                  v-for="line in productPriceLines(product)"
                  :key="line"
                  class="featured__card-price-line"
                >{{ line }}</span>
              </div>
              <span class="featured__card-price" v-else-if="product.price">
                desde {{ formatPrice(product.price) }}
              </span>
              <span class="featured__card-price" v-else>A consultar</span>
              <button class="featured__card-btn" @click="openWhatsApp(product.name)">
                Pedir
              </button>
            </div>
          </div>
          </article>
        </div>

        <!-- flecha derecha -->
        <button
          v-show="canScrollRight"
          type="button"
          class="featured__arrow featured__arrow--right"
          aria-label="Siguiente"
          @click="scrollFeatured(1)"
        >
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true">
            <path d="M7 4l6 6-6 6" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </div>
  </section>

  <Teleport to="body">
    <div
      v-if="selectedProduct"
      class="featured-detail"
      role="dialog"
      aria-modal="true"
      :aria-labelledby="'featured-detail-title-' + selectedProduct._id"
      @click.self="closeDetail"
    >
      <div class="featured-detail__panel">
        <button type="button" class="featured-detail__close" aria-label="Cerrar" @click="closeDetail">×</button>
        <div class="featured-detail__img">
          <video
            v-if="isVideo(selectedProduct.image_url)"
            :src="mediaSrc(selectedProduct.image_url)"
            muted loop autoplay playsinline
            class="featured-detail__video"
          />
          <img
            v-else
            :src="productCardSrc(selectedProduct)"
            :alt="selectedProduct.name"
            @error="onProductImgError(selectedProduct)"
          />
          <span v-if="selectedProduct.badge" class="featured-detail__badge">{{ selectedProduct.badge }}</span>
        </div>
        <div class="featured-detail__body">
          <p class="featured-detail__eyebrow">{{ categoryLabel(selectedProduct) }}</p>
          <h3 :id="'featured-detail-title-' + selectedProduct._id" class="featured-detail__title">
            {{ selectedProduct.name }}
          </h3>
          <p class="featured-detail__desc">{{ selectedProduct.description }}</p>
          <div class="featured-detail__prices">
            <p class="featured-detail__prices-title">Precios por tamaño</p>
            <dl class="featured-detail__price-list">
              <template v-for="row in tierPriceRowsForDetail(selectedProduct)" :key="row.size">
                <dt class="featured-detail__price-label">{{ row.label }}</dt>
                <dd
                  class="featured-detail__price-value"
                  :class="{ 'featured-detail__price-value--muted': !row.formatted }"
                >
                  {{ row.formatted || 'A consultar' }}
                </dd>
              </template>
            </dl>
          </div>
          <div class="featured-detail__actions">
            <button type="button" class="featured-detail__btn featured-detail__btn--ghost" @click="closeDetail">
              Cerrar
            </button>
            <button
              type="button"
              class="featured-detail__btn featured-detail__btn--primary"
              @click="openWhatsApp(selectedProduct.name)"
            >
              Pedir por WhatsApp
            </button>
          </div>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
/* ===== GALERÍA MASONRY ===== */
.gallery {
  padding: var(--section-padding) 0 60px;
}

.gallery__header {
  margin-bottom: 36px;
}

.gallery__header-row {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-top: 8px;
}

.gallery__title {
  font-family: var(--font-serif);
  font-size: clamp(2rem, 3.5vw, 2.8rem);
  color: var(--color-text);
}

.gallery__title em {
  font-style: italic;
  color: var(--color-rose-mid);
}

.gallery__see-all {
  font-family: var(--font-sans);
  font-size: 0.72rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--color-rose-mid);
  transition: opacity var(--transition);
  cursor: none;
  margin-bottom: 6px;
}

.gallery__see-all:hover {
  opacity: 0.7;
}

.gallery__filters {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 36px;
}

.gallery__filter-btn {
  font-family: var(--font-sans);
  font-size: 0.7rem;
  font-weight: 400;
  letter-spacing: 0.1em;
  color: var(--color-text-secondary);
  padding: 7px 18px;
  border: 1px solid var(--color-border);
  border-radius: 40px;
  background: transparent;
  transition: all var(--transition);
  cursor: none;
}

.gallery__filter-btn:hover,
.gallery__filter-btn.active {
  border-color: var(--color-rose-mid);
  color: var(--color-rose-mid);
  background: var(--color-rose-light);
}

.gallery__grid {
  columns: 4;
  column-gap: 12px;
}

.gallery__item {
  break-inside: avoid;
  margin-bottom: 12px;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
  cursor: pointer;
}

.gallery__img {
  width: 100%;
  display: block;
  transition: transform 0.5s ease;
}

.gallery__item:hover .gallery__img {
  transform: scale(1.04);
}

.gallery__overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(to top, rgba(28,16,8,0.72) 0%, transparent 55%);
  opacity: 0;
  transition: opacity var(--transition);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-end;
  padding: 16px;
  gap: 4px;
}

.gallery__item:hover .gallery__overlay {
  opacity: 1;
}

.gallery__overlay-name {
  font-family: var(--font-serif);
  font-size: 0.95rem;
  font-weight: 400;
  color: #fff;
}

.gallery__overlay-cta {
  font-family: var(--font-sans);
  font-size: 0.72rem;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: rgba(255,255,255,0.82);
}

.gallery__skeleton {
  break-inside: avoid;
  margin-bottom: 12px;
  border-radius: 8px;
  background: var(--color-rose-light);
  height: 220px;
  animation: shimmer 1.6s ease infinite;
}

.gallery__skeleton:nth-child(2n) { height: 280px; }
.gallery__skeleton:nth-child(3n) { height: 180px; }

/* ===== LO MÁS PEDIDO ===== */
.featured {
  padding: 60px 0 var(--section-padding);
}

.featured__header {
  text-align: center;
  margin-bottom: 48px;
}

.featured__title {
  font-family: var(--font-serif);
  font-size: clamp(2rem, 3.5vw, 2.8rem);
  color: var(--color-text);
  margin-top: 8px;
}

.featured__title em {
  font-style: italic;
  color: var(--color-rose-mid);
}

.featured__carousel {
  position: relative;
}

.featured__track {
  display: flex;
  gap: 20px;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
  padding-bottom: 4px;
}

.featured__track::-webkit-scrollbar { display: none; }

.featured__track--loading {
  display: flex;
  gap: 20px;
  overflow: hidden;
}

/* flechas ─────────────────────────────────────── */
.featured__arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 10;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  border: 1.5px solid rgba(168, 79, 59, 0.25);
  background: rgba(250, 243, 236, 0.92);
  color: var(--color-rose-mid);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  backdrop-filter: blur(6px);
  transition: background var(--transition), border-color var(--transition), transform var(--transition), box-shadow var(--transition);
  box-shadow: 0 2px 12px rgba(28,16,8,0.10);
}

.featured__arrow:hover {
  background: var(--color-rose-mid);
  border-color: var(--color-rose-mid);
  color: #fff;
  box-shadow: 0 4px 20px rgba(168,79,59,0.25);
  transform: translateY(-50%) scale(1.08);
}

.featured__arrow--left  { left: -22px; }
.featured__arrow--right { right: -22px; }

.featured__card {
  background: var(--color-bg-card);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 16px rgba(28,16,8,0.06);
  transition: box-shadow var(--transition), transform var(--transition);
  flex: 0 0 clamp(240px, 28vw, 310px);
  scroll-snap-align: start;
}

.featured__card:hover {
  box-shadow: 0 8px 32px rgba(28,16,8,0.12);
  transform: translateY(-3px);
}

.featured__card-img-wrap {
  position: relative;
  aspect-ratio: 4 / 3;
  overflow: hidden;
  cursor: pointer;
}

.featured__card-img-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.featured__card:hover .featured__card-img-wrap img {
  transform: scale(1.04);
}

.featured__card-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  background: rgba(250,243,236,0.95);
  color: var(--color-rose-mid);
  font-family: var(--font-sans);
  font-size: 0.6rem;
  font-weight: 500;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  padding: 4px 10px;
  border-radius: 20px;
}

.featured__card-body {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.featured__card-name {
  font-family: var(--font-serif);
  font-size: 1rem;
  font-weight: 400;
  color: var(--color-text);
}

.featured__card-desc {
  font-size: 0.78rem;
  color: var(--color-text-secondary);
  line-height: 1.5;
  font-weight: 300;
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.featured__card-more {
  align-self: flex-start;
  margin-top: 4px;
  padding: 0;
  border: none;
  background: none;
  font-family: var(--font-sans);
  font-size: 0.68rem;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--color-rose-mid);
  cursor: pointer;
  text-decoration: underline;
  text-underline-offset: 3px;
  transition: opacity var(--transition);
}

.featured__card-more:hover {
  opacity: 0.75;
}

.featured__card-footer {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 12px;
  margin-top: 8px;
}

.featured__card-price-block {
  display: flex;
  flex-direction: column;
  gap: 2px;
  align-items: flex-start;
  min-width: 0;
}

.featured__card-price-line {
  font-family: var(--font-serif);
  font-size: 0.82rem;
  color: var(--color-rose-mid);
  font-style: italic;
  line-height: 1.25;
}

.featured__card-price {
  font-family: var(--font-serif);
  font-size: 0.9rem;
  color: var(--color-rose-mid);
  font-style: italic;
}

.featured__card-btn {
  background: var(--color-rose-light);
  color: var(--color-rose-dark);
  font-family: var(--font-sans);
  font-size: 0.7rem;
  font-weight: 500;
  letter-spacing: 0.08em;
  padding: 8px 18px;
  border-radius: 40px;
  border: none;
  transition: background var(--transition), color var(--transition);
  cursor: none;
}

.featured__card-btn:hover {
  background: var(--color-rose-mid);
  color: var(--color-white);
}

.featured__skeleton {
  border-radius: 16px;
  background: var(--color-rose-light);
  height: 320px;
  animation: shimmer 1.6s ease infinite;
}

/* Modal detalle destacado */
.featured-detail {
  position: fixed;
  inset: 0;
  z-index: 300;
  background: rgba(28, 16, 8, 0.48);
  backdrop-filter: blur(6px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  animation: featured-detail-in 0.22s ease;
}

@keyframes featured-detail-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

.featured-detail__panel {
  position: relative;
  background: var(--color-bg-card);
  border-radius: 20px;
  width: 100%;
  max-width: 520px;
  max-height: min(90vh, 720px);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 24px 64px rgba(28, 16, 8, 0.22);
}

.featured-detail__close {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 2;
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 50%;
  background: rgba(250, 243, 236, 0.92);
  color: var(--color-text);
  font-size: 1.35rem;
  line-height: 1;
  cursor: pointer;
  transition: background var(--transition), color var(--transition);
}

.featured-detail__close:hover {
  background: var(--color-rose-mid);
  color: #fff;
}

.featured-detail__img {
  position: relative;
  flex-shrink: 0;
  aspect-ratio: 16 / 10;
  overflow: hidden;
}

.featured-detail__img img,
.featured-detail__video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 25%;
}

.featured-detail__badge {
  position: absolute;
  top: 14px;
  left: 14px;
  background: rgba(250, 243, 236, 0.95);
  color: var(--color-rose-mid);
  font-family: var(--font-sans);
  font-size: 0.58rem;
  font-weight: 500;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  padding: 5px 12px;
  border-radius: 20px;
}

.featured-detail__body {
  padding: 22px 26px 26px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.featured-detail__eyebrow {
  margin: 0;
  font-family: var(--font-sans);
  font-size: 0.62rem;
  font-weight: 500;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--color-text-secondary);
}

.featured-detail__title {
  margin: 0;
  font-family: var(--font-serif);
  font-size: 1.35rem;
  font-weight: 400;
  color: var(--color-text);
  line-height: 1.25;
}

.featured-detail__desc {
  margin: 0 0 6px;
  font-size: 0.88rem;
  line-height: 1.65;
  color: var(--color-text-secondary);
  font-weight: 300;
  white-space: pre-wrap;
}

.featured-detail__prices {
  padding-top: 8px;
  margin-top: 4px;
  border-top: 1px solid var(--color-border);
}

.featured-detail__prices-title {
  margin: 0 0 12px;
  font-family: var(--font-sans);
  font-size: 0.62rem;
  font-weight: 500;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--color-text-secondary);
}

.featured-detail__price-list {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 8px 20px;
  margin: 0;
  align-items: baseline;
}

.featured-detail__price-label {
  margin: 0;
  font-family: var(--font-sans);
  font-size: 0.8rem;
  font-weight: 400;
  color: var(--color-text);
}

.featured-detail__price-value {
  margin: 0;
  font-family: var(--font-serif);
  font-size: 1rem;
  font-style: italic;
  color: var(--color-rose-mid);
  text-align: right;
  white-space: nowrap;
}

.featured-detail__price-value--muted {
  font-family: var(--font-sans);
  font-size: 0.82rem;
  font-style: normal;
  color: var(--color-text-secondary);
}

.featured-detail__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 12px;
  padding-top: 4px;
}

.featured-detail__btn {
  font-family: var(--font-sans);
  font-size: 0.75rem;
  font-weight: 500;
  letter-spacing: 0.06em;
  padding: 11px 20px;
  border-radius: 40px;
  border: none;
  cursor: pointer;
  transition: background var(--transition), color var(--transition);
}

.featured-detail__btn--ghost {
  background: transparent;
  color: var(--color-text-secondary);
  border: 1px solid var(--color-border);
}

.featured-detail__btn--ghost:hover {
  background: var(--color-bg);
  color: var(--color-text);
}

.featured-detail__btn--primary {
  flex: 1;
  min-width: 160px;
  background: var(--color-rose-mid);
  color: #fff;
}

.featured-detail__btn--primary:hover {
  background: var(--color-rose-dark);
}

@keyframes shimmer {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 0.7; }
}

@media (max-width: 1024px) {
  .gallery__grid { columns: 3; }
  .featured__card { flex: 0 0 clamp(220px, 42vw, 280px); }
  .featured__arrow--left  { left: -14px; }
  .featured__arrow--right { right: -14px; }
}

@media (max-width: 768px) {
  .gallery__grid { columns: 2; }
  .gallery__header-row { flex-direction: column; align-items: flex-start; gap: 8px; }
  .featured__card { flex: 0 0 clamp(200px, 72vw, 280px); }
  .featured__arrow { width: 38px; height: 38px; }
  .featured__arrow--left  { left: -8px; }
  .featured__arrow--right { right: -8px; }
}

@media (max-width: 480px) {
  .gallery__grid { columns: 1; }
  .featured__card { flex: 0 0 80vw; }
  .featured__arrow { display: none; }
}
</style>

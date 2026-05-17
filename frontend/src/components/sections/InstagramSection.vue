<script setup>
const props = defineProps({
  handle: {
    type: String,
    default: '@piacordero_pasteleria',
  },
  reels: {
    type: Array,
    default: () => [],
  },
})

const FALLBACK_PHOTOS = [
  { id: 1, url: '/images/torta-frutos-rojos.jpg', alt: 'Torta frutos rojos' },
  { id: 2, url: '/images/torta-naranja-lavanda.jpg', alt: 'Torta naranja y lavanda' },
  { id: 3, url: '/images/torta-limon-top.jpg', alt: 'Torta limón' },
  { id: 4, url: '/images/torta-frambuesas.jpg', alt: 'Torta frambuesas' },
  { id: 5, url: '/images/pavlova-frambuesas.jpg', alt: 'Pavlova frambuesas' },
  { id: 6, url: '/images/torta-espiral-top.jpg', alt: 'Torta espiral' },
]

/** Convierte una URL pública de Instagram a su URL de embed */
function toEmbedUrl(raw) {
  if (!raw) return null
  const url = raw.trim().replace(/\/$/, '')
  const m = url.match(/instagram\.com\/(p|reel|tv)\/([A-Za-z0-9_-]+)/)
  if (!m) return null
  return `https://www.instagram.com/${m[1]}/${m[2]}/embed/`
}

const validReels = (props.reels || [])
  .map(toEmbedUrl)
  .filter(Boolean)

const profileUrl = `https://instagram.com/${props.handle.replace('@', '')}`
</script>

<template>
  <section class="instagram">
    <div class="container">
      <header class="instagram__header">
        <p class="instagram__handle fade-in">{{ handle }}</p>
        <h2 class="instagram__title fade-up">
          Sígueme en <em>Instagram</em>
        </h2>
      </header>

      <!-- Reels embebidos -->
      <div v-if="validReels.length" class="instagram__reels fade-up" data-delay="80">
        <div
          v-for="(embedUrl, i) in validReels"
          :key="i"
          class="instagram__reel-wrap"
        >
          <iframe
            :src="embedUrl"
            class="instagram__reel-frame"
            frameborder="0"
            scrolling="no"
            allowtransparency="true"
            allow="autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share"
            loading="lazy"
          />
        </div>
      </div>

      <!-- Fallback: fotos estáticas -->
      <div v-else class="instagram__grid fade-up" data-delay="80">
        <a
          v-for="photo in FALLBACK_PHOTOS"
          :key="photo.id"
          :href="profileUrl"
          target="_blank"
          rel="noopener noreferrer"
          class="instagram__item"
          data-hover
        >
          <img :src="photo.url" :alt="photo.alt" loading="lazy" />
          <div class="instagram__overlay">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
              <rect x="2" y="2" width="20" height="20" rx="5" ry="5"/>
              <circle cx="12" cy="12" r="4"/>
              <circle cx="17.5" cy="6.5" r="0.5" fill="currentColor" stroke="none"/>
            </svg>
          </div>
        </a>
      </div>

      <div class="instagram__link fade-up" data-delay="160">
        <a
          :href="profileUrl"
          target="_blank"
          rel="noopener noreferrer"
          class="instagram__see-all"
        >
          Ver todos los posts en Instagram →
        </a>
      </div>
    </div>
  </section>
</template>

<style scoped>
.instagram {
  padding: var(--section-padding) 0;
  background: var(--color-bg);
  border-top: 1px solid var(--color-border);
}

.instagram__header {
  text-align: center;
  margin-bottom: 40px;
}

.instagram__handle {
  font-size: 0.65rem;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  color: var(--color-rose-mid);
  font-weight: 400;
  font-family: var(--font-sans);
  margin-bottom: 10px;
}

.instagram__title {
  font-family: var(--font-serif);
  font-size: clamp(1.8rem, 3vw, 2.6rem);
  color: var(--color-text);
}

.instagram__title em {
  font-style: italic;
  color: var(--color-rose-mid);
}

/* ── Reels ───────────────────────────────── */
.instagram__reels {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 36px;
}

.instagram__reel-wrap {
  flex: 0 0 clamp(260px, 28vw, 340px);
  aspect-ratio: 9 / 16;
  border-radius: 14px;
  overflow: hidden;
  box-shadow: 0 4px 24px rgba(28,16,8,0.10);
  background: var(--color-bg-card);
}

.instagram__reel-frame {
  width: 100%;
  height: 100%;
  border: none;
  display: block;
}

/* ── Grid estático (fallback) ────────────── */
.instagram__grid {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  gap: 8px;
  margin-bottom: 36px;
}

.instagram__item {
  aspect-ratio: 1;
  border-radius: 6px;
  overflow: hidden;
  position: relative;
  display: block;
  cursor: none;
}

.instagram__item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.instagram__item:hover img {
  transform: scale(1.06);
}

.instagram__overlay {
  position: absolute;
  inset: 0;
  background: rgba(28,16,8,0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  opacity: 0;
  transition: opacity var(--transition);
}

.instagram__item:hover .instagram__overlay {
  opacity: 1;
}

/* ── Link ────────────────────────────────── */
.instagram__link {
  text-align: center;
}

.instagram__see-all {
  font-family: var(--font-sans);
  font-size: 0.72rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--color-rose-mid);
  transition: opacity var(--transition);
  cursor: none;
}

.instagram__see-all:hover {
  opacity: 0.7;
}

@media (max-width: 900px) {
  .instagram__grid { grid-template-columns: repeat(3, 1fr); }
  .instagram__reel-wrap { flex: 0 0 clamp(220px, 42vw, 300px); }
}

@media (max-width: 600px) {
  .instagram__reels { gap: 12px; }
  .instagram__reel-wrap { flex: 0 0 80vw; }
}

@media (max-width: 480px) {
  .instagram__grid { grid-template-columns: repeat(2, 1fr); }
}
</style>

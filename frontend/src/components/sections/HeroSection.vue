<script setup>
import { ref, computed } from 'vue'
import { resolvePublicOrUpload } from '../../constants/images.js'

const DEFAULTS = {
  tagline: 'Pasteles que cuentan una historia',
  tagline_italic: 'historia',
  subtitle: 'Tortas artesanales, pasteles y dulces únicos hechos con los mejores ingredientes. Cada creación es diseñada especialmente para ti.',
  image_main: '/images/torta-frambuesas.jpg',
  image_2: '/images/torta-frutos-rojos.jpg',
  image_3: '/images/torta-naranja-top.jpg',
  featured_label: 'Torta del mes',
  featured_desc: 'Frambuesa & vainilla',
  eyebrow: 'Hecho con amor en Chile',
}

const props = defineProps({
  content: {
    type: Object,
    default: () => ({}),
  },
})

/** Tras un error de carga, Vue no debe volver a aplicar la URL rota del CMS. */
const heroImgFailed = ref(new Set())

const display = computed(() => {
  const c = props.content || {}
  const pick = (key) =>
    heroImgFailed.value.has(key)
      ? DEFAULTS[key]
      : resolvePublicOrUpload(c[key], DEFAULTS[key])
  return {
    ...DEFAULTS,
    ...c,
    image_main: pick('image_main'),
    image_2: pick('image_2'),
    image_3: pick('image_3'),
  }
})

function scrollTo(id) {
  const el = document.getElementById(id)
  if (el) {
    const top = el.getBoundingClientRect().top + window.scrollY - 68
    window.scrollTo({ top, behavior: 'smooth' })
  }
}

function onHeroImgError(e) {
  const el = e.target
  if (!(el instanceof HTMLImageElement)) return
  const key = el.dataset.fallbackKey
  if (!key || heroImgFailed.value.has(key)) return
  heroImgFailed.value = new Set([...heroImgFailed.value, key])
}
</script>

<template>
  <section id="hero" class="hero">
    <div class="hero__inner container">

      <!-- Lado izquierdo: texto -->
      <div class="hero__text">
        <p class="hero__eyebrow fade-in">
          <span class="hero__eyebrow-line" aria-hidden="true" />
          {{ display.eyebrow }}
        </p>
        <h1 class="hero__title fade-up">
          Pasteles que<br />
          cuentan una <em>historia</em>
        </h1>
        <p class="hero__subtitle fade-up" data-delay="120">
          {{ display.subtitle }}
        </p>
        <div class="hero__actions fade-up" data-delay="240">
          <button class="hero__btn-primary" @click="scrollTo('galeria')" data-track="Hero: Ver creaciones">
            Ver creaciones
          </button>
          <button class="hero__btn-secondary" @click="scrollTo('contacto')" data-track="Hero: Hacer un pedido">
            Hacer un pedido →
          </button>
        </div>
      </div>

      <!-- Lado derecho: collage de fotos -->
      <div class="hero__gallery fade-in" data-delay="200">
        <div class="hero__gallery-main">
          <img
            :src="display.image_main"
            alt="Torta principal"
            loading="eager"
            data-fallback-key="image_main"
            @error="onHeroImgError"
          />
          <div class="hero__badge">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
            <div>
              <span class="hero__badge-label">{{ display.featured_label }}</span>
              <span class="hero__badge-desc">{{ display.featured_desc }}</span>
            </div>
          </div>
        </div>
        <div class="hero__gallery-side">
          <img
            :src="display.image_2"
            alt="Creación 2"
            loading="eager"
            data-fallback-key="image_2"
            @error="onHeroImgError"
          />
          <img
            :src="display.image_3"
            alt="Creación 3"
            loading="eager"
            data-fallback-key="image_3"
            @error="onHeroImgError"
          />
        </div>
      </div>
    </div>

    <!-- Círculo decorativo fondo -->
    <div class="hero__deco" aria-hidden="true" />
  </section>
</template>

<style scoped>
.hero {
  position: relative;
  min-height: calc(100vh - var(--header-height));
  display: flex;
  align-items: center;
  overflow: hidden;
  padding: 60px 0 80px;
}

.hero__inner {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: clamp(40px, 5vw, 80px);
  align-items: center;
  position: relative;
  z-index: 2;
}

/* Decoración circular */
.hero__deco {
  position: absolute;
  right: -10%;
  top: 50%;
  transform: translateY(-50%);
  width: clamp(400px, 55vw, 720px);
  height: clamp(400px, 55vw, 720px);
  border-radius: 50%;
  background: var(--color-rose-pale);
  opacity: 0.45;
  z-index: 1;
}

/* Texto izquierda */
.hero__eyebrow {
  display: flex;
  align-items: center;
  gap: 14px;
  font-size: 0.7rem;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: var(--color-rose-mid);
  font-weight: 400;
  margin-bottom: 22px;
}

.hero__eyebrow-line {
  display: block;
  width: 36px;
  height: 1px;
  background: var(--color-rose-mid);
  flex-shrink: 0;
}

.hero__title {
  font-family: var(--font-serif);
  font-size: clamp(2.4rem, 4.5vw, 3.8rem);
  font-weight: 400;
  color: var(--color-text);
  line-height: 1.15;
  margin-bottom: 22px;
}

.hero__title em {
  font-style: italic;
  color: var(--color-rose-mid);
}

.hero__subtitle {
  font-size: 0.95rem;
  color: var(--color-text-secondary);
  line-height: 1.8;
  font-weight: 300;
  max-width: 420px;
  margin-bottom: 40px;
}

.hero__actions {
  display: flex;
  align-items: center;
  gap: 24px;
  flex-wrap: wrap;
}

.hero__btn-primary {
  background: var(--color-rose-mid);
  color: var(--color-white);
  font-family: var(--font-sans);
  font-size: 0.82rem;
  font-weight: 400;
  letter-spacing: 0.05em;
  padding: 14px 32px;
  border-radius: 40px;
  border: none;
  transition: background var(--transition);
  cursor: none;
}

.hero__btn-primary:hover {
  background: var(--color-rose-dark);
}

.hero__btn-secondary {
  font-family: var(--font-sans);
  font-size: 0.82rem;
  font-weight: 400;
  color: var(--color-text-secondary);
  border: none;
  background: none;
  cursor: none;
  transition: color var(--transition);
  letter-spacing: 0.03em;
}

.hero__btn-secondary:hover {
  color: var(--color-text);
}

/* Galería derecha */
.hero__gallery {
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: 12px;
  height: clamp(360px, 55vh, 520px);
  position: relative;
  z-index: 2;
}

.hero__gallery-main {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
}

.hero__gallery-main img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 20%;
}

.hero__badge {
  position: absolute;
  bottom: 16px;
  left: 16px;
  background: rgba(250, 243, 236, 0.95);
  backdrop-filter: blur(8px);
  border-radius: 10px;
  padding: 10px 14px;
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--color-rose-mid);
}

.hero__badge > div {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.hero__badge-label {
  font-family: var(--font-sans);
  font-size: 0.72rem;
  font-weight: 500;
  color: var(--color-text);
  letter-spacing: 0.02em;
}

.hero__badge-desc {
  font-family: var(--font-sans);
  font-size: 0.62rem;
  font-weight: 300;
  color: var(--color-text-secondary);
}

.hero__gallery-side {
  display: grid;
  grid-template-rows: 1fr 1fr;
  gap: 12px;
}

.hero__gallery-side img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 15%;
  border-radius: 12px;
}

@media (max-width: 900px) {
  .hero__inner {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .hero__eyebrow {
    justify-content: center;
  }

  .hero__subtitle {
    margin: 0 auto 40px;
  }

  .hero__actions {
    justify-content: center;
  }

  .hero__gallery {
    max-width: 480px;
    margin: 0 auto;
    height: 300px;
  }

  .hero__deco {
    display: none;
  }
}

@media (max-width: 480px) {
  .hero__gallery {
    display: none;
  }
}
</style>

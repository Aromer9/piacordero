<script setup>
import { ref, computed } from 'vue'
import { resolvePublicOrUpload } from '../../constants/images.js'

const DEFAULTS = {
  title: 'Hola, soy Pía',
  paragraphs: [
    'Creadora de los pasteles que hago con tanto amor. Hace ya varios años estudié Gastronomía y, después de practicar en restaurantes y hacer cursos de muchas cosas diferentes, me di cuenta que lo mío era hacer pasteles, cosas dulces y hacer felices a mi familia y mis amigos.',
    'En todo este tiempo conocí gente hermosa, profesores que admiro muchísimo y colegas que son talentosísimas.',
    'Ahora que decidí emprender, estoy feliz de hacer lo que amo y que se vea reflejado en cada detalle que hago para ustedes.',
  ],
  signature: 'Pía Cordero',
  since_year: '2015',
  image_main: '/images/naked-cake-naranja.jpg',
  image_2: '/images/torta-espiral-top.jpg',
}

const props = defineProps({
  content: {
    type: Object,
    default: () => ({}),
  },
})

const aboutImgFailed = ref(new Set())

const display = computed(() => {
  const c = props.content || {}
  const pick = (key) =>
    aboutImgFailed.value.has(key)
      ? DEFAULTS[key]
      : resolvePublicOrUpload(c[key], DEFAULTS[key])
  return {
    ...DEFAULTS,
    ...c,
    image_main: pick('image_main'),
    image_2: pick('image_2'),
  }
})

function onAboutImgError(e) {
  const el = e.target
  if (!(el instanceof HTMLImageElement)) return
  const key = el.dataset.fallbackKey
  if (!key || aboutImgFailed.value.has(key)) return
  aboutImgFailed.value = new Set([...aboutImgFailed.value, key])
}
</script>

<template>
  <section id="sobre-mi" class="about">
    <div class="about__inner container">

      <!-- Izquierda: fotos superpuestas -->
      <div class="about__images fade-in">
        <div class="about__img-main-wrap">
          <img
            :src="display.image_main"
            :alt="`Foto de ${display.signature}`"
            class="about__img-main"
            loading="lazy"
            data-fallback-key="image_main"
            @error="onAboutImgError"
          />
        </div>
      </div>

      <!-- Derecha: texto -->
      <div class="about__content">
        <p class="eyebrow fade-in">Sobre mí</p>
        <h2 class="about__title fade-up">
          Hola, soy <em>Pía</em>
        </h2>
        <div class="about__texts">
          <p
            v-for="(p, i) in display.paragraphs"
            :key="i"
            class="about__text fade-up"
            :data-delay="i * 80"
          >{{ p }}</p>
        </div>
        <p class="about__signature fade-up" data-delay="280">— {{ display.signature }} 🫶</p>
      </div>
    </div>
  </section>
</template>

<style scoped>
.about {
  padding: var(--section-padding) 0;
  background: var(--color-bg);
}

.about__inner {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: clamp(48px, 7vw, 100px);
  align-items: center;
}

/* Fotos superpuestas */
.about__images {
  position: relative;
  height: 480px;
}

.about__img-main-wrap {
  position: absolute;
  top: 0;
  left: 0;
  width: 70%;
  height: 85%;
  border-radius: 12px;
  overflow: hidden;
}

.about__img-main {
  width: 100%;
  height: 100%;
  object-fit: cover;
}


/* Contenido de texto */
.about__content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.about__title {
  font-family: var(--font-serif);
  font-size: clamp(2rem, 3.5vw, 2.8rem);
  color: var(--color-text);
  margin-top: 8px;
}

.about__title em {
  font-style: italic;
  color: var(--color-rose-mid);
}

.about__texts {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.about__text {
  font-size: 0.92rem;
  color: var(--color-text-secondary);
  line-height: 1.85;
  font-weight: 300;
}

.about__signature {
  font-family: var(--font-serif);
  font-size: 1rem;
  font-style: italic;
  color: var(--color-rose-mid);
  margin-top: 4px;
}

@media (max-width: 900px) {
  .about__inner {
    grid-template-columns: 1fr;
  }

  .about__images {
    height: 360px;
    max-width: 460px;
    margin: 0 auto;
  }
}

@media (max-width: 480px) {
  .about__images {
    height: 280px;
  }
}
</style>

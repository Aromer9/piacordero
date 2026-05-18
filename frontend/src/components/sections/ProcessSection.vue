<script setup>
defineProps({
  content: {
    type: Object,
    default: () => ({
      steps: [
        { title: 'Conversamos', description: 'Me cuentas tu idea, la ocasión especial y tus sabores favoritos. Juntas diseñamos algo único para ti.' },
        { title: 'Creamos', description: 'Selecciono los mejores ingredientes de temporada y elaboro tu pedido con todo el cuidado artesanal.' },
        { title: 'Celebramos', description: 'Tu creación llega lista para hacer de tu momento algo verdaderamente memorable.' },
      ],
    }),
  },
})
</script>

<template>
  <section id="proceso" class="process">
    <div class="container">
      <header class="process__header">
        <p class="eyebrow fade-in">Cómo funciona</p>
        <h2 class="process__title fade-up">
          Así creamos juntas<br /><em>tu torta perfecta</em>
        </h2>
      </header>

      <div class="process__steps">
        <div
          v-for="(step, i) in content.steps"
          :key="i"
          class="process__step fade-up"
          :data-delay="i * 120"
        >
          <div class="process__step-number">{{ String(i + 1).padStart(2, '0') }}</div>
          <div class="process__step-icon" aria-hidden="true">
            <svg v-if="i === 0" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
            <svg v-else-if="i === 1" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"/>
              <path d="M12 6v6l4 2"/>
            </svg>
            <svg v-else width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
            </svg>
          </div>
          <h3 class="process__step-title">{{ step.title }}</h3>
          <p class="process__step-desc">{{ step.description }}</p>
          <div v-if="i < content.steps.length - 1" class="process__connector" aria-hidden="true" />
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.process {
  padding: var(--section-padding) 0;
  background: var(--color-bg);
  position: relative;
}

.process::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: var(--color-border);
}

.process__header {
  text-align: center;
  margin-bottom: 64px;
}

.process__title {
  font-family: var(--font-serif);
  font-size: clamp(1.8rem, 3vw, 2.6rem);
  color: var(--color-text);
  margin-top: 8px;
}

.process__title em {
  font-style: italic;
  color: var(--color-rose-mid);
}

.process__steps {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 0;
  position: relative;
}

.process__step {
  text-align: center;
  padding: 0 40px;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.process__step:not(:last-child)::after {
  content: '';
  position: absolute;
  top: 48px;
  right: -1px;
  width: 1px;
  height: 60px;
  background: var(--color-border);
}

.process__step-number {
  font-family: var(--font-serif);
  font-size: 0.7rem;
  color: var(--color-rose-mid);
  letter-spacing: 0.15em;
  font-style: italic;
  margin-bottom: 16px;
}

.process__step-icon {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  border: 1px solid var(--color-border);
  background: var(--color-bg-card);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-rose-mid);
  margin-bottom: 24px;
}

.process__step-title {
  font-family: var(--font-serif);
  font-size: 1.3rem;
  font-weight: 400;
  color: var(--color-text);
  margin-bottom: 12px;
}

.process__step-desc {
  font-size: 0.88rem;
  color: var(--color-text-secondary);
  line-height: 1.8;
  font-weight: 300;
  max-width: 260px;
}

@media (max-width: 768px) {
  .process__steps {
    grid-template-columns: 1fr;
    gap: 48px;
  }

  .process__step {
    padding: 0 24px;
  }

  .process__step:not(:last-child)::after {
    display: none;
  }
}
</style>

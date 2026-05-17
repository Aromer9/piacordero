<template>
  <div class="features">
    <div class="features__inner container">
      <div v-for="(f, i) in features" :key="i" class="features__item">
        <div class="features__icon" v-html="f.icon" />
        <span class="features__label">{{ f.label }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
const features = [
  {
    label: 'Ingredientes\nnaturales',
    icon: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a10 10 0 0 1 0 20"/><path d="M12 2C6.5 2 2 6.5 2 12"/><path d="M12 6v6l4 2"/></svg>`,
  },
  {
    label: 'Diseño\npersonalizado',
    icon: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>`,
  },
  {
    label: 'Despacho a\ndomicilio',
    icon: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="3" width="15" height="13"/><path d="M16 8h4l3 4v5h-7V8z"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>`,
  },
  {
    label: '+500 clientes\nfelices',
    icon: `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>`,
  },
]
</script>

<style scoped>
.features {
  border-top: 1px solid var(--color-border);
  border-bottom: 1px solid var(--color-border);
  padding: 20px 0;
  background: var(--color-bg);
}

.features__inner {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
}

.features__item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 12px 24px;
}

.features__item:not(:last-child) {
  border-right: 1px solid var(--color-border);
}

.features__icon {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: var(--color-rose-light);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-rose-mid);
  flex-shrink: 0;
}

.features__label {
  font-family: var(--font-sans);
  font-size: 0.68rem;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--color-text);
  white-space: pre-line;
  line-height: 1.4;
}

@media (max-width: 768px) {
  .features__inner {
    grid-template-columns: repeat(2, 1fr);
  }

  .features__item:nth-child(2) {
    border-right: none;
  }

  .features__item:nth-child(1),
  .features__item:nth-child(2) {
    border-bottom: 1px solid var(--color-border);
  }
}

@media (max-width: 480px) {
  .features__inner {
    grid-template-columns: 1fr;
  }

  .features__item {
    border-right: none !important;
    border-bottom: 1px solid var(--color-border);
    padding: 14px 0;
  }

  .features__item:last-child {
    border-bottom: none;
  }
}
</style>

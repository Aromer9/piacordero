<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const scrolled = ref(false)
const menuOpen = ref(false)

function onScroll() {
  scrolled.value = window.scrollY > 40
}

function scrollTo(id) {
  menuOpen.value = false
  const el = document.getElementById(id)
  if (el) {
    const top = el.getBoundingClientRect().top + window.scrollY - 68
    window.scrollTo({ top, behavior: 'smooth' })
  }
}

onMounted(() => window.addEventListener('scroll', onScroll, { passive: true }))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<template>
  <header class="header" :class="{ scrolled }">
    <div class="header__inner container">

      <button class="header__logo" @click="scrollTo('hero')" aria-label="Inicio">
        <span class="header__logo-name">Pía Cordero</span>
        <span class="header__logo-sub">Pastelería Artesanal</span>
      </button>

      <nav class="header__nav" :class="{ open: menuOpen }">
        <button @click="scrollTo('galeria')">Galería</button>
        <button @click="scrollTo('creaciones')">Tortas</button>
        <button @click="scrollTo('sobre-mi')">Sobre mí</button>
        <button @click="scrollTo('contacto')">Pedidos</button>
      </nav>

      <button class="header__cta" @click="scrollTo('contacto')">
        <span class="header__cta-dot" aria-hidden="true" />
        Pedir ahora
      </button>

      <button class="header__burger" :class="{ open: menuOpen }" @click="menuOpen = !menuOpen" aria-label="Menú">
        <span></span>
        <span></span>
      </button>
    </div>
  </header>
</template>

<style scoped>
.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  height: var(--header-height);
  transition: background var(--transition), box-shadow var(--transition);
}

.header.scrolled {
  background: rgba(250, 243, 236, 0.92);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  box-shadow: 0 1px 0 var(--color-border);
}

.header__inner {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  height: 100%;
  gap: 24px;
}

.header__logo {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 1px;
  background: none;
  border: none;
  cursor: none;
  flex-shrink: 0;
}

.header__logo-name {
  font-family: var(--font-serif);
  font-size: 1.05rem;
  font-weight: 500;
  font-style: italic;
  letter-spacing: 0.02em;
  color: var(--color-text);
  line-height: 1;
}

.header__logo-sub {
  font-family: var(--font-sans);
  font-size: 0.58rem;
  font-weight: 300;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: var(--color-text-secondary);
  line-height: 1;
}

.header__nav {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2.5rem;
}

.header__nav button {
  font-family: var(--font-sans);
  font-size: 0.75rem;
  font-weight: 400;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--color-text-secondary);
  transition: color var(--transition);
  cursor: none;
}

.header__nav button:hover {
  color: var(--color-rose-mid);
}

.header__cta {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: var(--font-sans);
  font-size: 0.73rem;
  font-weight: 400;
  letter-spacing: 0.08em;
  color: var(--color-white);
  background: var(--color-rose-mid);
  padding: 10px 22px;
  border-radius: 40px;
  border: none;
  transition: background var(--transition);
  cursor: none;
  flex-shrink: 0;
  white-space: nowrap;
}

.header__cta:hover {
  background: var(--color-rose-dark);
}

.header__cta-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: rgba(255,255,255,0.7);
  display: block;
  flex-shrink: 0;
}

.header__burger {
  display: none;
  flex-direction: column;
  gap: 6px;
  width: 24px;
  cursor: none;
  background: none;
  border: none;
}

.header__burger span {
  display: block;
  height: 1px;
  background: var(--color-text);
  transition: transform var(--transition), opacity var(--transition);
  transform-origin: center;
}

.header__burger.open span:first-child {
  transform: translateY(3.5px) rotate(45deg);
}

.header__burger.open span:last-child {
  transform: translateY(-3.5px) rotate(-45deg);
}

@media (max-width: 900px) {
  .header__inner {
    grid-template-columns: 1fr auto auto;
  }

  .header__nav {
    display: none;
  }

  .header__burger {
    display: flex;
  }

  .header__nav.open {
    display: flex;
    position: fixed;
    top: var(--header-height);
    left: 0;
    right: 0;
    bottom: 0;
    background: var(--color-bg);
    flex-direction: column;
    justify-content: center;
    gap: 2.5rem;
    z-index: 99;
    animation: slideIn 0.3s ease;
  }

  .header__nav.open button {
    font-size: 1.2rem;
    letter-spacing: 0.2em;
  }
}

@keyframes slideIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>

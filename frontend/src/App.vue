<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import AppHeader from './components/layout/AppHeader.vue'
import AppFooter from './components/layout/AppFooter.vue'

const cursorX = ref(0)
const cursorY = ref(0)
const cursorExpanded = ref(false)

function onMouseMove(e) {
  cursorX.value = e.clientX
  cursorY.value = e.clientY
}

function onMouseOver(e) {
  const tag = e.target.tagName.toLowerCase()
  const interactable = ['a', 'button', 'img'].includes(tag) ||
    e.target.closest('a, button, [data-hover]')
  cursorExpanded.value = !!interactable
}

onMounted(() => {
  window.addEventListener('mousemove', onMouseMove, { passive: true })
  window.addEventListener('mouseover', onMouseOver, { passive: true })
})

onUnmounted(() => {
  window.removeEventListener('mousemove', onMouseMove)
  window.removeEventListener('mouseover', onMouseOver)
})
</script>

<template>
  <div
    class="cursor"
    :class="{ expanded: cursorExpanded }"
    :style="{ left: `${cursorX}px`, top: `${cursorY}px` }"
  />
  <AppHeader />
  <main>
    <router-view />
  </main>
  <AppFooter />
</template>

<style scoped>
main {
  padding-top: var(--header-height);
}
</style>

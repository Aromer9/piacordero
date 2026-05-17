import { onMounted, onUnmounted, nextTick } from 'vue'

export function useScrollAnimation(selector = '.fade-up, .fade-in', options = {}) {
  let observer = null

  const defaultOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -30px 0px',
    ...options,
  }

  const observe = () => {
    document.querySelectorAll(selector).forEach((el) => {
      if (!el.classList.contains('visible')) {
        observer.observe(el)
      }
    })
  }

  onMounted(async () => {
    await nextTick()

    observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const delay = entry.target.dataset.delay || 0
          setTimeout(() => {
            entry.target.classList.add('visible')
          }, Number(delay))
          observer.unobserve(entry.target)
        }
      })
    }, defaultOptions)

    observe()

    // Re-observe after a tick to catch dynamically rendered elements
    setTimeout(observe, 300)
    setTimeout(observe, 1000)
  })

  onUnmounted(() => {
    if (observer) observer.disconnect()
  })

  return { observe }
}

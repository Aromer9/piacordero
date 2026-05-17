<script setup>
import { ref, onMounted } from 'vue'
import { useApi } from '../composables/useApi.js'
import { useScrollAnimation } from '../composables/useScrollAnimation.js'

import HeroSection from '../components/sections/HeroSection.vue'
import FeaturesStrip from '../components/sections/FeaturesStrip.vue'
import CreationsGallery from '../components/sections/CreationsGallery.vue'
import AboutSection from '../components/sections/AboutSection.vue'
import ProcessSection from '../components/sections/ProcessSection.vue'
import ContactSection from '../components/sections/ContactSection.vue'
import InstagramSection from '../components/sections/InstagramSection.vue'

const { getProducts, getSiteContent } = useApi()

const FALLBACK_PRODUCTS = [
  { _id: '1', name: 'Torta Frambuesas', description: 'Bizcocho de vainilla con crema diplomática y frambuesas frescas', category: 'tortas', image_url: '/images/torta-frambuesas.jpg', featured: true, price: 32000, price_15p: 32000, price_20p: 42000, price_30p: 56000, badge: 'Favorita' },
  { _id: '2', name: 'Torta Naranja & Lavanda', description: 'Naked cake con crema de naranja, merengues y naranjas deshidratadas', category: 'tortas', image_url: '/images/torta-naranja-lavanda.jpg', featured: true, price: 38000, badge: null },
  { _id: '3', name: 'Torta Frutos Rojos', description: 'Crema chantilly con frutillas, moras, arándanos y frambuesas de temporada', category: 'tortas', image_url: '/images/torta-frutos-rojos.jpg', featured: true, price: 32000, badge: null },
  { _id: '4', name: 'Pavlova de Frambuesas', description: 'Merengue crujiente por fuera y suave por dentro con frambuesas y menta', category: 'temporada', image_url: '/images/pavlova-frambuesas.jpg', featured: true, price: 28000, badge: 'Temporada' },
  { _id: '5', name: 'Torta Limón & Arándanos', description: 'Crema de limón con decoración en espiral, arándanos y flores comestibles', category: 'tartas', image_url: '/images/torta-limon-top.jpg', featured: false, price: 30000, badge: null },
  { _id: '6', name: 'Torta Espiral de Limón', description: 'Crema de vainilla con espiral artesanal, arándanos y flores silvestres', category: 'tartas', image_url: '/images/torta-espiral-top.jpg', featured: false, price: 28000, badge: null },
  { _id: '7', name: 'Naked Cake Naranja', description: 'Naked cake con naranjas deshidratadas, almendras y flores de lavanda', category: 'tortas', image_url: '/images/naked-cake-naranja.jpg', featured: false, price: 36000, badge: null },
  { _id: '8', name: 'Torta Naranja Festiva', description: 'Torta festiva con merengues, naranjas caramelizadas y lavanda', category: 'tortas', image_url: '/images/torta-naranja-top.jpg', featured: false, price: 34000, badge: null },
]

const products = ref([])
const siteContent = ref({})
const loading = ref(true)

useScrollAnimation()

onMounted(async () => {
  try {
    const [prods, content] = await Promise.all([
      getProducts(),
      getSiteContent(),
    ])
    products.value = prods.length ? prods : FALLBACK_PRODUCTS
    siteContent.value = content
  } catch (err) {
    console.warn('API no disponible, usando contenido por defecto:', err.message)
    products.value = FALLBACK_PRODUCTS
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="home">
    <HeroSection :content="siteContent.hero?.content" />
    <FeaturesStrip />
    <CreationsGallery :products="products" :loading="loading" />
    <AboutSection :content="siteContent.about?.content" />
    <ProcessSection :content="siteContent.process?.content" />
    <ContactSection :content="siteContent.contact?.content" />
    <InstagramSection
      :handle="siteContent.contact?.content?.instagram || '@piacordero_pasteleria'"
      :reels="siteContent.instagram?.content?.reels || []"
    />
  </div>
</template>

<style scoped>
.home {
  min-height: 100vh;
}
</style>

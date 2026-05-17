<script setup>
import { ref, onMounted } from 'vue'
import { useAdminApi } from '../../composables/useAdminApi.js'
import { productImageSrc, isVideo, mediaSrc } from '../../constants/images.js'
import { hasTierPrices, tierPricesSummary } from '../../utils/productPrices.js'
import AdminProductForm from './AdminProductForm.vue'

const { getProducts, deleteProduct, updateProductOrder } = useAdminApi()

const products = ref([])
const loading = ref(true)
const showForm = ref(false)
const editingProduct = ref(null)
const deletingId = ref(null)
const successMsg = ref('')

async function load() {
  loading.value = true
  try {
    products.value = await getProducts()
  } finally {
    loading.value = false
  }
}

async function handleDelete(product) {
  if (!confirm(`¿Eliminar "${product.name}"? Esta acción no se puede deshacer.`)) return
  deletingId.value = product._id
  try {
    await deleteProduct(product._id)
    products.value = products.value.filter(p => p._id !== product._id)
    showSuccess('Producto eliminado')
  } finally {
    deletingId.value = null
  }
}

function openCreate() {
  editingProduct.value = null
  showForm.value = true
}

function openEdit(product) {
  editingProduct.value = { ...product }
  showForm.value = true
}

function handleSaved(product) {
  const idx = products.value.findIndex(p => p._id === product._id)
  if (idx >= 0) {
    products.value[idx] = product
  } else {
    products.value.unshift(product)
  }
  showForm.value = false
  showSuccess(idx >= 0 ? 'Producto actualizado' : 'Producto creado')
}

function showSuccess(msg) {
  successMsg.value = msg
  setTimeout(() => successMsg.value = '', 3000)
}

function formatPrice(price) {
  if (!price) return '—'
  return new Intl.NumberFormat('es-CL', { style: 'currency', currency: 'CLP', maximumFractionDigits: 0 }).format(price)
}

function productPriceLines(product) {
  if (hasTierPrices(product)) return tierPricesSummary(product)
  return null
}

const CATEGORY_LABELS = {
  tortas: 'Tortas',
  tartas: 'Tartas',
  petit_fours: 'Petit Fours',
  temporada: 'Temporada',
}

onMounted(load)
</script>

<template>
  <div class="ap">
    <!-- Header -->
    <div class="ap__header">
      <div>
        <h1 class="ap__title">Catálogo</h1>
        <p class="ap__subtitle">{{ products.length }} productos en total</p>
      </div>
      <button class="ap__btn-primary" @click="openCreate">
        + Agregar producto
      </button>
    </div>

    <!-- Success toast -->
    <transition name="toast">
      <div v-if="successMsg" class="ap__toast">✓ {{ successMsg }}</div>
    </transition>

    <!-- Loading -->
    <div v-if="loading" class="ap__skeletons">
      <div class="ap__skeleton" v-for="n in 6" :key="n" />
    </div>

    <!-- Grid de productos -->
    <div v-else class="ap__grid">
      <div v-for="product in products" :key="product._id" class="ap__card">
        <div class="ap__card-img">
          <video
            v-if="isVideo(product.image_url)"
            :src="mediaSrc(product.image_url)"
            muted loop autoplay playsinline
            class="ap__card-video"
          />
          <img v-else :src="productImageSrc(product.image_url)" :alt="product.name" loading="lazy" />
          <span v-if="product.featured" class="ap__card-featured">★ Destacado</span>
          <span v-if="product.sold_out" class="ap__card-soldout">Agotado</span>
        </div>
        <div class="ap__card-body">
          <div class="ap__card-meta">
            <span class="ap__card-cat">{{ CATEGORY_LABELS[product.category] }}</span>
            <span v-if="product.sold_out" class="ap__card-meta-tag">Sin pedidos</span>
            <span v-if="product.badge" class="ap__card-badge">{{ product.badge }}</span>
          </div>
          <h3 class="ap__card-name">{{ product.name }}</h3>
          <p class="ap__card-desc">{{ product.description }}</p>
          <div v-if="productPriceLines(product)?.length" class="ap__card-price-block">
            <p v-for="line in productPriceLines(product)" :key="line" class="ap__card-price-line">{{ line }}</p>
          </div>
          <p v-else class="ap__card-price">{{ formatPrice(product.price) }}</p>
          <div class="ap__card-actions">
            <button class="ap__btn-edit" @click="openEdit(product)">
              Editar
            </button>
            <button
              class="ap__btn-delete"
              :disabled="deletingId === product._id"
              @click="handleDelete(product)"
            >
              {{ deletingId === product._id ? '...' : 'Eliminar' }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal formulario -->
    <Teleport to="body">
      <div v-if="showForm" class="ap__modal-bg" @click.self="showForm = false">
        <div class="ap__modal">
          <button class="ap__modal-close" @click="showForm = false">×</button>
          <AdminProductForm
            :product="editingProduct"
            @saved="handleSaved"
            @cancel="showForm = false"
          />
        </div>
      </div>
    </Teleport>
  </div>
</template>

<style scoped>
.ap { max-width: 1100px; }

.ap__header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 32px;
  gap: 16px;
  flex-wrap: wrap;
}

.ap__title {
  font-family: var(--font-serif);
  font-size: 1.8rem;
  font-weight: 400;
  color: var(--color-text);
  margin-bottom: 4px;
}

.ap__subtitle {
  font-size: 0.8rem;
  color: var(--color-text-secondary);
}

.ap__btn-primary {
  background: var(--color-rose-mid);
  color: #fff;
  font-family: var(--font-sans);
  font-size: 0.8rem;
  font-weight: 500;
  padding: 10px 20px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: background var(--transition);
  white-space: nowrap;
}

.ap__btn-primary:hover { background: var(--color-rose-dark); }

.ap__toast {
  background: #2a7a4a;
  color: #fff;
  font-size: 0.82rem;
  padding: 10px 18px;
  border-radius: 8px;
  margin-bottom: 20px;
  width: fit-content;
}

.toast-enter-active, .toast-leave-active { transition: opacity 0.3s; }
.toast-enter-from, .toast-leave-to { opacity: 0; }

.ap__skeletons {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.ap__skeleton {
  height: 320px;
  border-radius: 12px;
  background: var(--color-rose-light);
  animation: shimmer 1.5s ease infinite;
}

@keyframes shimmer { 0%,100%{opacity:.4} 50%{opacity:.7} }

.ap__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.ap__card {
  background: var(--color-bg-card);
  border-radius: 12px;
  overflow: hidden;
  border: 1px solid var(--color-border);
  transition: box-shadow var(--transition);
}

.ap__card:hover { box-shadow: 0 4px 20px rgba(28,16,8,0.1); }

.ap__card-img {
  position: relative;
  aspect-ratio: 4/3;
  overflow: hidden;
}

.ap__card-img img,
.ap__card-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 20%;
}

.ap__card-featured {
  position: absolute;
  top: 10px;
  left: 10px;
  background: var(--color-rose-mid);
  color: #fff;
  font-size: 0.6rem;
  font-weight: 500;
  letter-spacing: 0.08em;
  padding: 3px 10px;
  border-radius: 20px;
}

.ap__card-soldout {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(80, 52, 44, 0.92);
  color: #faf3ec;
  font-size: 0.58rem;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 4px 10px;
  border-radius: 6px;
}

.ap__card-meta-tag {
  font-size: 0.58rem;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--color-text-secondary);
  background: rgba(120, 100, 92, 0.15);
  padding: 2px 8px;
  border-radius: 20px;
}

.ap__card-body {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.ap__card-meta {
  display: flex;
  gap: 6px;
  align-items: center;
}

.ap__card-cat {
  font-size: 0.62rem;
  font-weight: 500;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--color-text-secondary);
}

.ap__card-badge {
  font-size: 0.58rem;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--color-rose-mid);
  background: var(--color-rose-light);
  padding: 2px 8px;
  border-radius: 20px;
}

.ap__card-name {
  font-family: var(--font-serif);
  font-size: 1rem;
  font-weight: 400;
  color: var(--color-text);
}

.ap__card-desc {
  font-size: 0.78rem;
  color: var(--color-text-secondary);
  line-height: 1.5;
  font-weight: 300;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.ap__card-price-block {
  margin-top: 2px;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.ap__card-price-line {
  font-family: var(--font-serif);
  font-size: 0.82rem;
  font-style: italic;
  color: var(--color-rose-mid);
  margin: 0;
  line-height: 1.25;
}

.ap__card-price {
  font-family: var(--font-serif);
  font-size: 0.9rem;
  font-style: italic;
  color: var(--color-rose-mid);
  margin-top: 2px;
}

.ap__card-actions {
  display: flex;
  gap: 8px;
  margin-top: 8px;
}

.ap__btn-edit, .ap__btn-delete {
  flex: 1;
  font-family: var(--font-sans);
  font-size: 0.72rem;
  font-weight: 500;
  padding: 8px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  transition: background var(--transition), color var(--transition);
}

.ap__btn-edit {
  background: var(--color-rose-light);
  color: var(--color-rose-dark);
}

.ap__btn-edit:hover { background: var(--color-rose-mid); color: #fff; }

.ap__btn-delete {
  background: #fef2f2;
  color: #c44;
}

.ap__btn-delete:hover:not(:disabled) { background: #fde8e8; }
.ap__btn-delete:disabled { opacity: 0.5; cursor: not-allowed; }

/* Modal */
.ap__modal-bg {
  position: fixed;
  inset: 0;
  background: rgba(28,16,8,0.5);
  backdrop-filter: blur(4px);
  z-index: 200;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.ap__modal {
  background: var(--color-bg-card);
  border-radius: 16px;
  width: 100%;
  max-width: 560px;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 20px 60px rgba(28,16,8,0.25);
}

.ap__modal-close {
  position: absolute;
  top: 16px;
  right: 16px;
  font-size: 1.4rem;
  color: var(--color-text-secondary);
  background: none;
  border: none;
  cursor: pointer;
  line-height: 1;
  z-index: 1;
}

@media (max-width: 900px) {
  .ap__grid, .ap__skeletons { grid-template-columns: repeat(2,1fr); }
}

@media (max-width: 540px) {
  .ap__grid, .ap__skeletons { grid-template-columns: 1fr; }
}
</style>

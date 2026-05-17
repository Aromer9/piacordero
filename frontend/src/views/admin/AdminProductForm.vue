<script setup>
import { ref, watch, nextTick } from 'vue'
import { useAdminApi } from '../../composables/useAdminApi.js'
import { productImageSrc, isVideo } from '../../constants/images.js'
import { numOrNull } from '../../utils/productPrices.js'

const props = defineProps({
  product: { type: Object, default: null },
})

const emit = defineEmits(['saved', 'cancel'])
const { createProduct, updateProduct, uploadImage } = useAdminApi()

const isEdit = ref(!!props.product)
const saving = ref(false)
const uploadingImg = ref(false)
const error = ref('')

const form = ref({
  name: '',
  description: '',
  category: 'tortas',
  image_url: '',
  price_15p: '',
  price_20p: '',
  price_30p: '',
  badge: '',
  featured: false,
  order: 0,
})

function hasAnyTierField(p) {
  if (!p) return false
  return [p.price_15p, p.price_20p, p.price_30p].some(
    (x) => x != null && x !== '' && Number.isFinite(Number(x)),
  )
}

/** Valor API → texto para inputs de precio (solo dígitos / separadores miles) */
function tierFromApi(val) {
  const n = numOrNull(val)
  return n != null ? String(n) : ''
}

watch(() => props.product, (p) => {
  isEdit.value = !!p
  if (p) {
    let p15 = tierFromApi(p.price_15p)
    let p20 = tierFromApi(p.price_20p)
    let p30 = tierFromApi(p.price_30p)
    if (!hasAnyTierField(p) && p.price != null && p.price !== '') {
      const leg = numOrNull(p.price)
      if (leg != null) p15 = String(leg)
    }
    form.value = {
      name: p.name || '',
      description: p.description || '',
      category: p.category || 'tortas',
      image_url: p.image_url || '',
      price_15p: p15,
      price_20p: p20,
      price_30p: p30,
      badge: p.badge || '',
      featured: p.featured || false,
      order: p.order || 0,
    }
  } else {
    form.value = {
      name: '',
      description: '',
      category: 'tortas',
      image_url: '',
      price_15p: '',
      price_20p: '',
      price_30p: '',
      badge: '',
      featured: false,
      order: 0,
    }
  }
}, { immediate: true })

async function handleImageFile(e) {
  const file = e.target.files[0]
  if (!file) return
  uploadingImg.value = true
  error.value = ''
  try {
    const result = await uploadImage(file)
    form.value.image_url = result.url
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al subir el archivo'
  } finally {
    uploadingImg.value = false
  }
}

async function handleSubmit() {
  if (!form.value.name?.trim()) {
    error.value = 'El nombre es obligatorio'
    return
  }
  saving.value = true
  error.value = ''
  try {
    /* type="number" a veces no vuelca el valor a v-model hasta blur; Guardar sin salir del campo perdía el dato (ej. 20 p.). */
    if (document.activeElement instanceof HTMLElement) {
      document.activeElement.blur()
    }
    await nextTick()

    const img = (form.value.image_url || '').trim()
    const p15 = numOrNull(form.value.price_15p)
    const p20 = numOrNull(form.value.price_20p)
    const p30 = numOrNull(form.value.price_30p)
    const tierNums = [p15, p20, p30].filter((x) => x != null)
    const payload = {
      name: form.value.name.trim(),
      description: (form.value.description || '').trim(),
      category: form.value.category,
      featured: !!form.value.featured,
      order: Number(form.value.order) || 0,
      price_15p: p15,
      price_20p: p20,
      price_30p: p30,
      price: tierNums.length ? Math.min(...tierNums) : null,
      badge: form.value.badge?.trim() || null,
      image_url: img || '',
    }

    console.log('[AdminProductForm] payload a enviar →', JSON.stringify(payload))

    let saved
    if (isEdit.value && props.product?._id) {
      saved = await updateProduct(props.product._id, payload)
      console.log('[AdminProductForm] respuesta del servidor →', JSON.stringify(saved))
    } else {
      saved = await createProduct(payload)
    }
    emit('saved', saved)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Error al guardar'
  } finally {
    saving.value = false
  }
}

const CATEGORIES = [
  { value: 'tortas', label: 'Tortas' },
  { value: 'tartas', label: 'Tartas' },
  { value: 'petit_fours', label: 'Petit Fours' },
  { value: 'temporada', label: 'Temporada' },
]
</script>

<template>
  <div class="pf">
    <div class="pf__header">
      <h2 class="pf__title">{{ isEdit ? 'Editar producto' : 'Nuevo producto' }}</h2>
    </div>

    <form class="pf__form" novalidate @submit.prevent="handleSubmit">
      <!-- Foto / Vídeo -->
      <div class="pf__field">
        <label class="pf__label">Foto o vídeo <span class="pf__optional">(opcional)</span></label>
        <div class="pf__img-preview" v-if="form.image_url">
          <video
            v-if="isVideo(form.image_url)"
            :src="form.image_url"
            class="pf__preview-video"
            muted
            loop
            autoplay
            playsinline
          />
          <img v-else :src="productImageSrc(form.image_url)" alt="Preview" />
        </div>
        <div v-else class="pf__img-preview pf__img-preview--empty">
          <span>Sin foto ni vídeo — se mostrará un marcador en el sitio</span>
        </div>
        <div class="pf__img-actions">
          <label class="pf__btn-upload" :class="{ loading: uploadingImg }">
            <input
              type="file"
              accept="image/jpeg,image/png,image/webp,image/gif,video/mp4,video/webm,video/quicktime"
              @change="handleImageFile"
              style="display:none"
            />
            {{ uploadingImg ? 'Subiendo...' : '↑ Foto o vídeo' }}
          </label>
          <span class="pf__hint">o ruta / URL:</span>
          <input
            v-model="form.image_url"
            type="text"
            class="pf__input pf__input--url"
            placeholder="/uploads/foto.jpg o /uploads/video.mp4"
          />
        </div>
        <p class="pf__hint pf__hint--block">Imágenes: hasta 8 MB. Vídeos (MP4, WebM, MOV): hasta 80 MB.</p>
      </div>

      <!-- Nombre -->
      <div class="pf__field">
        <label class="pf__label">Nombre <span class="pf__required">*</span></label>
        <input v-model="form.name" type="text" class="pf__input" placeholder="Torta Frambuesas" required />
      </div>

      <!-- Descripción -->
      <div class="pf__field">
        <label class="pf__label">Descripción</label>
        <textarea
          v-model="form.description"
          class="pf__input pf__textarea"
          placeholder="Describe el producto brevemente..."
          rows="3"
        />
      </div>

      <!-- Categoría -->
      <div class="pf__field">
        <label class="pf__label">Categoría</label>
        <select v-model="form.category" class="pf__input pf__select">
          <option v-for="c in CATEGORIES" :key="c.value" :value="c.value">{{ c.label }}</option>
        </select>
      </div>

      <!-- Precios por tamaño (personas) -->
      <div class="pf__field">
        <label class="pf__label">Precios (CLP)</label>
        <p class="pf__hint pf__hint--block">Rellena los tamaños que apliquen. Si el producto solo tenía un precio, quedará en 15 p.</p>
        <div class="pf__row pf__row--tiers">
          <div class="pf__field">
            <label class="pf__label pf__label--sub">15 personas</label>
            <input
              v-model="form.price_15p"
              type="text"
              class="pf__input"
              name="price_15p"
              autocomplete="off"
              placeholder="Ej: 50000"
              inputmode="numeric"
              maxlength="12"
            />
          </div>
          <div class="pf__field">
            <label class="pf__label pf__label--sub">20 personas</label>
            <input
              v-model="form.price_20p"
              type="text"
              class="pf__input"
              name="price_20p"
              autocomplete="off"
              placeholder="Ej: 42000"
              inputmode="numeric"
              maxlength="12"
            />
          </div>
          <div class="pf__field">
            <label class="pf__label pf__label--sub">30 personas</label>
            <input
              v-model="form.price_30p"
              type="text"
              class="pf__input"
              name="price_30p"
              autocomplete="off"
              placeholder="Ej: 56000"
              inputmode="numeric"
              maxlength="12"
            />
          </div>
        </div>
      </div>

      <!-- Badge + Orden -->
      <div class="pf__row">
        <div class="pf__field">
          <label class="pf__label">Badge <span class="pf__hint-inline">(ej: Favorita, Nuevo)</span></label>
          <input v-model="form.badge" type="text" class="pf__input" placeholder="Ej: Favorita, Nuevo" />
        </div>
        <div class="pf__field">
          <label class="pf__label">Orden</label>
          <input v-model="form.order" type="number" class="pf__input" min="0" />
        </div>
      </div>

      <!-- Destacado -->
      <label class="pf__checkbox">
        <input v-model="form.featured" type="checkbox" />
        <span>Mostrar como destacado en "Lo más pedido"</span>
      </label>

      <p v-if="error" class="pf__error">{{ error }}</p>

      <div class="pf__footer">
        <button type="button" class="pf__btn-cancel" @click="emit('cancel')">Cancelar</button>
        <button type="submit" class="pf__btn-save" :disabled="saving">
          {{ saving ? 'Guardando...' : isEdit ? 'Guardar cambios' : 'Crear producto' }}
        </button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.pf { padding: 28px 32px 32px; }

.pf__header { margin-bottom: 24px; }

.pf__title {
  font-family: var(--font-serif);
  font-size: 1.3rem;
  font-weight: 400;
  color: var(--color-text);
}

.pf__form { display: flex; flex-direction: column; gap: 18px; }

.pf__field { display: flex; flex-direction: column; gap: 7px; flex: 1; }

.pf__row { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }

.pf__row--tiers {
  grid-template-columns: 1fr 1fr 1fr;
}

@media (max-width: 520px) {
  .pf__row--tiers {
    grid-template-columns: 1fr;
  }
}

.pf__label--sub {
  font-size: 0.62rem;
  letter-spacing: 0.06em;
}

.pf__hint--block {
  margin: 0 0 8px;
  white-space: normal;
}

.pf__label {
  font-family: var(--font-sans);
  font-size: 0.68rem;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--color-text-secondary);
}

.pf__required { color: var(--color-rose-mid); }

.pf__optional {
  font-size: 0.58rem;
  font-weight: 300;
  text-transform: none;
  letter-spacing: 0.04em;
  color: var(--color-text-secondary);
}

.pf__hint-inline {
  font-size: 0.62rem;
  font-weight: 300;
  text-transform: none;
  letter-spacing: 0;
  color: var(--color-text-secondary);
}

.pf__input {
  font-family: var(--font-sans);
  font-size: 0.88rem;
  color: var(--color-text);
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: 8px;
  padding: 10px 12px;
  outline: none;
  transition: border-color var(--transition);
  width: 100%;
}

.pf__input:focus { border-color: var(--color-rose-mid); }

.pf__textarea { resize: vertical; min-height: 80px; }

.pf__select { cursor: pointer; }

.pf__input--url { flex: 1; min-width: 0; }

.pf__img-preview {
  width: 100%;
  height: 160px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid var(--color-border);
  margin-bottom: 8px;
}

.pf__img-preview img,
.pf__preview-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 20%;
}

.pf__img-preview--empty {
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg);
  padding: 16px;
  text-align: center;
}

.pf__img-preview--empty span {
  font-size: 0.78rem;
  color: var(--color-text-secondary);
  font-weight: 300;
  line-height: 1.5;
}

.pf__img-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.pf__btn-upload {
  display: inline-flex;
  align-items: center;
  font-family: var(--font-sans);
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--color-rose-dark);
  background: var(--color-rose-light);
  border: none;
  border-radius: 6px;
  padding: 8px 14px;
  cursor: pointer;
  transition: background var(--transition);
  white-space: nowrap;
}

.pf__btn-upload:hover { background: var(--color-rose-mid); color: #fff; }
.pf__btn-upload.loading { opacity: 0.6; cursor: wait; }

.pf__hint {
  font-size: 0.72rem;
  color: var(--color-text-secondary);
  white-space: nowrap;
}

.pf__checkbox {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  font-size: 0.82rem;
  color: var(--color-text);
}

.pf__checkbox input { accent-color: var(--color-rose-mid); width: 15px; height: 15px; }

.pf__error {
  font-size: 0.78rem;
  color: #c44;
  background: #fef2f2;
  padding: 8px 12px;
  border-radius: 6px;
}

.pf__footer {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  padding-top: 8px;
  border-top: 1px solid var(--color-border);
}

.pf__btn-cancel, .pf__btn-save {
  font-family: var(--font-sans);
  font-size: 0.8rem;
  font-weight: 500;
  padding: 10px 20px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: background var(--transition), color var(--transition);
}

.pf__btn-cancel {
  background: var(--color-bg);
  color: var(--color-text-secondary);
  border: 1px solid var(--color-border);
}

.pf__btn-cancel:hover { background: var(--color-border); }

.pf__btn-save {
  background: var(--color-rose-mid);
  color: #fff;
}

.pf__btn-save:hover:not(:disabled) { background: var(--color-rose-dark); }
.pf__btn-save:disabled { opacity: 0.6; cursor: not-allowed; }
</style>

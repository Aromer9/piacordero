<script setup>
import { ref, onMounted } from 'vue'
import { useAdminApi } from '../../composables/useAdminApi.js'

const { getSiteContent, updateSiteContent, uploadImage } = useAdminApi()

const loading = ref(true)
const saving = ref({})
const successMsg = ref('')
const error = ref('')

const about = ref({ title: '', paragraphs: ['', '', ''], signature: '', since_year: '' })
const contact = ref({ phone: '', email: '', instagram: '', whatsapp_number: '', whatsapp_message: '', location: '' })
const hero = ref({ eyebrow: '', tagline: '', subtitle: '', featured_label: '', featured_desc: '' })
const reels = ref([])

const uploadingField = ref('')

async function load() {
  try {
    const data = await getSiteContent()
    if (data.about?.content) {
      const a = data.about.content
      about.value = {
        title: a.title || '',
        paragraphs: a.paragraphs || ['', '', ''],
        signature: a.signature || '',
        since_year: a.since_year || '',
        image_main: a.image_main || '',
        image_2: a.image_2 || '',
      }
    }
    if (data.contact?.content) {
      contact.value = { ...data.contact.content }
    }
    if (data.hero?.content) {
      const h = data.hero.content
      hero.value = {
        eyebrow: h.eyebrow || '',
        tagline: h.tagline || '',
        subtitle: h.subtitle || '',
        featured_label: h.featured_label || '',
        featured_desc: h.featured_desc || '',
        image_main: h.image_main || '',
        image_2: h.image_2 || '',
        image_3: h.image_3 || '',
      }
    }
    if (data.instagram?.content?.reels) {
      reels.value = [...data.instagram.content.reels]
    }
  } catch (e) {
    error.value = 'Error cargando contenido'
  } finally {
    loading.value = false
  }
}

async function save(section, data) {
  saving.value[section] = true
  error.value = ''
  try {
    await updateSiteContent(section, data)
    showSuccess('Cambios guardados')
  } catch {
    error.value = 'Error al guardar'
  } finally {
    saving.value[section] = false
  }
}

async function handleImageUpload(field, targetObj) {
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
  input.onchange = async (e) => {
    const file = e.target.files[0]
    if (!file) return
    uploadingField.value = field
    try {
      const result = await uploadImage(file)
      targetObj[field] = result.url
    } catch {
      error.value = 'Error al subir imagen'
    } finally {
      uploadingField.value = ''
    }
  }
  input.click()
}

function showSuccess(msg) {
  successMsg.value = msg
  setTimeout(() => successMsg.value = '', 3000)
}

onMounted(load)
</script>

<template>
  <div class="ac">
    <div class="ac__header">
      <h1 class="ac__title">Contenido del sitio</h1>
      <p class="ac__subtitle">Edita los textos e imágenes que aparecen en el sitio</p>
    </div>

    <transition name="toast">
      <div v-if="successMsg" class="ac__toast">✓ {{ successMsg }}</div>
    </transition>
    <p v-if="error" class="ac__error">{{ error }}</p>

    <div v-if="loading" class="ac__loading">Cargando contenido...</div>

    <div v-else class="ac__sections">

      <!-- Sobre mí -->
      <section class="ac__section">
        <div class="ac__section-header">
          <h2 class="ac__section-title">Sobre mí</h2>
          <p class="ac__section-desc">Texto que aparece en la sección "Hola, soy Pía"</p>
        </div>

        <div class="ac__fields">
          <div class="ac__field">
            <label class="ac__label">Título</label>
            <input v-model="about.title" type="text" class="ac__input" />
          </div>
          <div class="ac__field">
            <label class="ac__label">Firma</label>
            <input v-model="about.signature" type="text" class="ac__input" placeholder="Pía" />
          </div>
          <div class="ac__field">
            <label class="ac__label">Año de inicio</label>
            <input v-model="about.since_year" type="text" class="ac__input" placeholder="2015" />
          </div>

          <div class="ac__field ac__field--full">
            <label class="ac__label">Párrafo 1</label>
            <textarea v-model="about.paragraphs[0]" class="ac__input ac__textarea" rows="3" />
          </div>
          <div class="ac__field ac__field--full">
            <label class="ac__label">Párrafo 2</label>
            <textarea v-model="about.paragraphs[1]" class="ac__input ac__textarea" rows="3" />
          </div>
          <div class="ac__field ac__field--full">
            <label class="ac__label">Párrafo 3</label>
            <textarea v-model="about.paragraphs[2]" class="ac__input ac__textarea" rows="3" />
          </div>

          <!-- Imágenes -->
          <div class="ac__field">
            <label class="ac__label">Foto principal</label>
            <div class="ac__img-row">
              <img v-if="about.image_main" :src="about.image_main" class="ac__img-thumb" />
              <button type="button" class="ac__btn-upload" @click="handleImageUpload('image_main', about)" :disabled="uploadingField === 'image_main'">
                {{ uploadingField === 'image_main' ? 'Subiendo...' : '↑ Subir foto' }}
              </button>
            </div>
          </div>
          <div class="ac__field">
            <label class="ac__label">Foto secundaria</label>
            <div class="ac__img-row">
              <img v-if="about.image_2" :src="about.image_2" class="ac__img-thumb" />
              <button type="button" class="ac__btn-upload" @click="handleImageUpload('image_2', about)" :disabled="uploadingField === 'image_2'">
                {{ uploadingField === 'image_2' ? 'Subiendo...' : '↑ Subir foto' }}
              </button>
            </div>
          </div>
        </div>

        <button class="ac__btn-save" :disabled="saving.about" @click="save('about', about)">
          {{ saving.about ? 'Guardando...' : 'Guardar sección' }}
        </button>
      </section>

      <!-- Contacto -->
      <section class="ac__section">
        <div class="ac__section-header">
          <h2 class="ac__section-title">Contacto</h2>
          <p class="ac__section-desc">Información de contacto y redes sociales</p>
        </div>

        <div class="ac__fields">
          <div class="ac__field">
            <label class="ac__label">Teléfono</label>
            <input v-model="contact.phone" type="text" class="ac__input" placeholder="+56 9 1234 5678" />
          </div>
          <div class="ac__field">
            <label class="ac__label">Email</label>
            <input v-model="contact.email" type="email" class="ac__input" />
          </div>
          <div class="ac__field">
            <label class="ac__label">Instagram</label>
            <input v-model="contact.instagram" type="text" class="ac__input" placeholder="@piacordero_pasteleria" />
          </div>
          <div class="ac__field">
            <label class="ac__label">Número WhatsApp <span class="ac__hint">(solo dígitos, con código país)</span></label>
            <input v-model="contact.whatsapp_number" type="text" class="ac__input" placeholder="56989646783" />
          </div>
          <div class="ac__field ac__field--full">
            <label class="ac__label">Mensaje predefinido WhatsApp</label>
            <input v-model="contact.whatsapp_message" type="text" class="ac__input" />
          </div>
          <div class="ac__field">
            <label class="ac__label">Ciudad</label>
            <input v-model="contact.location" type="text" class="ac__input" placeholder="Santiago, Chile" />
          </div>
        </div>

        <button class="ac__btn-save" :disabled="saving.contact" @click="save('contact', contact)">
          {{ saving.contact ? 'Guardando...' : 'Guardar sección' }}
        </button>
      </section>

      <!-- Hero -->
      <section class="ac__section">
        <div class="ac__section-header">
          <h2 class="ac__section-title">Hero (portada)</h2>
          <p class="ac__section-desc">Textos e imágenes de la sección principal</p>
        </div>

        <div class="ac__fields">
          <div class="ac__field ac__field--full">
            <label class="ac__label">Frase principal</label>
            <input v-model="hero.tagline" type="text" class="ac__input" />
          </div>
          <div class="ac__field ac__field--full">
            <label class="ac__label">Subtítulo</label>
            <textarea v-model="hero.subtitle" class="ac__input ac__textarea" rows="2" />
          </div>
          <div class="ac__field">
            <label class="ac__label">Texto eyebrow</label>
            <input v-model="hero.eyebrow" type="text" class="ac__input" placeholder="Hecho con amor en Chile" />
          </div>
          <div class="ac__field">
            <label class="ac__label">Badge: etiqueta</label>
            <input v-model="hero.featured_label" type="text" class="ac__input" placeholder="Torta del mes" />
          </div>
          <div class="ac__field">
            <label class="ac__label">Badge: descripción</label>
            <input v-model="hero.featured_desc" type="text" class="ac__input" placeholder="Frambuesa & vainilla" />
          </div>

          <div class="ac__field">
            <label class="ac__label">Imagen principal</label>
            <div class="ac__img-row">
              <img v-if="hero.image_main" :src="hero.image_main" class="ac__img-thumb" />
              <button type="button" class="ac__btn-upload" @click="handleImageUpload('image_main', hero)" :disabled="uploadingField === 'image_main'">
                {{ uploadingField === 'image_main' ? 'Subiendo...' : '↑ Subir' }}
              </button>
            </div>
          </div>
          <div class="ac__field">
            <label class="ac__label">Imagen 2 (collage)</label>
            <div class="ac__img-row">
              <img v-if="hero.image_2" :src="hero.image_2" class="ac__img-thumb" />
              <button type="button" class="ac__btn-upload" @click="handleImageUpload('image_2', hero)" :disabled="uploadingField === 'image_2'">
                {{ uploadingField === 'image_2' ? 'Subiendo...' : '↑ Subir' }}
              </button>
            </div>
          </div>
          <div class="ac__field">
            <label class="ac__label">Imagen 3 (collage)</label>
            <div class="ac__img-row">
              <img v-if="hero.image_3" :src="hero.image_3" class="ac__img-thumb" />
              <button type="button" class="ac__btn-upload" @click="handleImageUpload('image_3', hero)" :disabled="uploadingField === 'image_3'">
                {{ uploadingField === 'image_3' ? 'Subiendo...' : '↑ Subir' }}
              </button>
            </div>
          </div>
        </div>

        <button class="ac__btn-save" :disabled="saving.hero" @click="save('hero', hero)">
          {{ saving.hero ? 'Guardando...' : 'Guardar sección' }}
        </button>
      </section>

      <!-- Reels de Instagram -->
      <section class="ac__section">
        <div class="ac__section-header">
          <h2 class="ac__section-title">Reels de Instagram</h2>
          <p class="ac__section-desc">
            Pega hasta 6 URLs de Reels o posts de Instagram (ej: https://www.instagram.com/reel/ABC123/).
            Si no hay ninguno, se mostrarán las fotos de ejemplo.
          </p>
        </div>

        <div class="ac__fields ac__fields--reels">
          <div v-for="(_, i) in reels" :key="i" class="ac__field ac__field--full ac__field--reel-row">
            <label class="ac__label">Reel {{ i + 1 }}</label>
            <div class="ac__reel-row">
              <input
                v-model="reels[i]"
                type="url"
                class="ac__input"
                :placeholder="`https://www.instagram.com/reel/CODE${i + 1}/`"
              />
              <button type="button" class="ac__btn-reel-remove" @click="reels.splice(i, 1)" aria-label="Quitar">×</button>
            </div>
          </div>

          <div class="ac__field ac__field--full" v-if="reels.length < 6">
            <button type="button" class="ac__btn-reel-add" @click="reels.push('')">
              + Agregar Reel
            </button>
          </div>
        </div>

        <button class="ac__btn-save" :disabled="saving.instagram" @click="save('instagram', { reels: reels.filter(r => r.trim()) })">
          {{ saving.instagram ? 'Guardando...' : 'Guardar Reels' }}
        </button>
      </section>

    </div>
  </div>
</template>

<style scoped>
.ac { max-width: 900px; }

.ac__header { margin-bottom: 32px; }

.ac__title {
  font-family: var(--font-serif);
  font-size: 1.8rem;
  font-weight: 400;
  color: var(--color-text);
  margin-bottom: 4px;
}

.ac__subtitle { font-size: 0.8rem; color: var(--color-text-secondary); }

.ac__toast {
  background: #2a7a4a; color: #fff;
  font-size: 0.82rem; padding: 10px 18px;
  border-radius: 8px; margin-bottom: 20px; width: fit-content;
}

.toast-enter-active, .toast-leave-active { transition: opacity 0.3s; }
.toast-enter-from, .toast-leave-to { opacity: 0; }

.ac__error {
  font-size: 0.78rem; color: #c44;
  background: #fef2f2; padding: 10px 14px;
  border-radius: 8px; margin-bottom: 16px;
}

.ac__loading { color: var(--color-text-secondary); font-size: 0.88rem; }

.ac__sections { display: flex; flex-direction: column; gap: 28px; }

.ac__section {
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  padding: 28px;
}

.ac__section-header { margin-bottom: 24px; }

.ac__section-title {
  font-family: var(--font-serif);
  font-size: 1.15rem;
  font-weight: 400;
  color: var(--color-text);
  margin-bottom: 4px;
}

.ac__section-desc { font-size: 0.78rem; color: var(--color-text-secondary); }

.ac__fields {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-bottom: 24px;
}

.ac__field { display: flex; flex-direction: column; gap: 7px; }
.ac__field--full { grid-column: 1 / -1; }

.ac__label {
  font-family: var(--font-sans);
  font-size: 0.65rem;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--color-text-secondary);
}

.ac__hint {
  font-size: 0.6rem;
  font-weight: 300;
  text-transform: none;
  letter-spacing: 0;
}

.ac__input {
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

.ac__input:focus { border-color: var(--color-rose-mid); }
.ac__textarea { resize: vertical; min-height: 76px; }

.ac__img-row { display: flex; align-items: center; gap: 10px; }

.ac__img-thumb {
  width: 64px; height: 48px;
  object-fit: cover;
  object-position: center 20%;
  border-radius: 6px;
  border: 1px solid var(--color-border);
  flex-shrink: 0;
}

.ac__btn-upload {
  font-family: var(--font-sans);
  font-size: 0.72rem;
  font-weight: 500;
  color: var(--color-rose-dark);
  background: var(--color-rose-light);
  border: none;
  border-radius: 6px;
  padding: 7px 14px;
  cursor: pointer;
  transition: background var(--transition), color var(--transition);
  white-space: nowrap;
}

.ac__btn-upload:hover:not(:disabled) { background: var(--color-rose-mid); color: #fff; }
.ac__btn-upload:disabled { opacity: 0.6; cursor: wait; }

.ac__btn-save {
  font-family: var(--font-sans);
  font-size: 0.8rem;
  font-weight: 500;
  color: #fff;
  background: var(--color-rose-mid);
  border: none;
  border-radius: 8px;
  padding: 11px 24px;
  cursor: pointer;
  transition: background var(--transition);
}

.ac__btn-save:hover:not(:disabled) { background: var(--color-rose-dark); }
.ac__btn-save:disabled { opacity: 0.6; cursor: not-allowed; }

.ac__fields--reels { grid-template-columns: 1fr; }

.ac__reel-row {
  display: flex;
  gap: 8px;
  align-items: center;
}

.ac__btn-reel-remove {
  flex-shrink: 0;
  width: 32px; height: 32px;
  border-radius: 50%;
  border: 1px solid var(--color-border);
  background: var(--color-bg);
  color: var(--color-text-secondary);
  font-size: 1.1rem;
  line-height: 1;
  cursor: pointer;
  transition: background var(--transition), color var(--transition);
  display: flex; align-items: center; justify-content: center;
}
.ac__btn-reel-remove:hover { background: #fef2f2; color: #c44; border-color: #c44; }

.ac__btn-reel-add {
  font-family: var(--font-sans);
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--color-rose-mid);
  background: transparent;
  border: 1.5px dashed var(--color-rose-mid);
  border-radius: 8px;
  padding: 10px 20px;
  cursor: pointer;
  transition: background var(--transition);
  width: 100%;
}
.ac__btn-reel-add:hover { background: var(--color-rose-light); }

@media (max-width: 600px) {
  .ac__fields { grid-template-columns: 1fr; }
  .ac__field--full { grid-column: 1; }
}
</style>

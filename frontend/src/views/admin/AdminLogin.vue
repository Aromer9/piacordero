<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuth } from '../../composables/useAuth.js'

const router = useRouter()
const route = useRoute()
const { login } = useAuth()

const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  if (!password.value) return
  loading.value = true
  error.value = ''
  try {
    await login(password.value)
    const redirect = route.query.redirect || '/admin/productos'
    router.push(redirect)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Contraseña incorrecta'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login">
    <div class="login__card">
      <div class="login__brand">
        <span class="login__brand-name">Pía Cordero</span>
        <span class="login__brand-sub">panel de administración</span>
      </div>

      <form class="login__form" @submit.prevent="handleLogin">
        <div class="login__field">
          <label class="login__label">Contraseña</label>
          <input
            v-model="password"
            type="password"
            class="login__input"
            :class="{ error: error }"
            placeholder="••••••••••"
            autofocus
            autocomplete="current-password"
          />
        </div>

        <p v-if="error" class="login__error">{{ error }}</p>

        <button type="submit" class="login__btn" :disabled="loading">
          <span v-if="loading" class="login__spinner" />
          <span v-else>Ingresar</span>
        </button>
      </form>

      <a href="/" class="login__back">← Volver al sitio</a>
    </div>
  </div>
</template>

<style scoped>
.login {
  min-height: 100vh;
  background: var(--color-bg);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.login__card {
  width: 100%;
  max-width: 380px;
  background: var(--color-bg-card);
  border: 1px solid var(--color-border);
  border-radius: 16px;
  padding: 48px 40px;
  display: flex;
  flex-direction: column;
  gap: 32px;
  box-shadow: 0 4px 24px rgba(28,16,8,0.07);
}

.login__brand {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.login__brand-name {
  font-family: var(--font-serif);
  font-size: 1.5rem;
  font-weight: 500;
  font-style: italic;
  color: var(--color-text);
}

.login__brand-sub {
  font-family: var(--font-sans);
  font-size: 0.62rem;
  font-weight: 300;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--color-text-secondary);
}

.login__form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.login__field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.login__label {
  font-family: var(--font-sans);
  font-size: 0.72rem;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--color-text-secondary);
}

.login__input {
  font-family: var(--font-sans);
  font-size: 0.95rem;
  color: var(--color-text);
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  border-radius: 10px;
  padding: 12px 16px;
  outline: none;
  transition: border-color var(--transition);
  width: 100%;
}

.login__input:focus {
  border-color: var(--color-rose-mid);
}

.login__input.error {
  border-color: #e05c5c;
}

.login__error {
  font-size: 0.78rem;
  color: #c44;
  font-weight: 400;
}

.login__btn {
  font-family: var(--font-sans);
  font-size: 0.82rem;
  font-weight: 500;
  letter-spacing: 0.05em;
  color: var(--color-white);
  background: var(--color-rose-mid);
  border: none;
  border-radius: 10px;
  padding: 14px;
  cursor: pointer;
  transition: background var(--transition);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.login__btn:hover:not(:disabled) {
  background: var(--color-rose-dark);
}

.login__btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.login__spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.login__back {
  font-family: var(--font-sans);
  font-size: 0.75rem;
  color: var(--color-text-secondary);
  text-align: center;
  cursor: pointer;
  transition: color var(--transition);
}

.login__back:hover {
  color: var(--color-rose-mid);
}
</style>

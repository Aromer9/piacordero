<script setup>
import { useRouter, useRoute } from 'vue-router'
import { useAuth } from '../../composables/useAuth.js'

const router = useRouter()
const route = useRoute()
const { logout } = useAuth()

function handleLogout() {
  logout()
  router.push('/admin/login')
}

const nav = [
  { to: '/admin/productos', label: 'Catálogo', icon: '🎂' },
  { to: '/admin/contenido', label: 'Contenido', icon: '✏️' },
  { to: '/admin/analytics', label: 'Analytics', icon: '📊' },
]
</script>

<template>
  <div class="admin">
    <aside class="admin__sidebar">
      <div class="admin__brand">
        <span class="admin__brand-name">Pía Cordero</span>
        <span class="admin__brand-sub">Panel admin</span>
      </div>

      <nav class="admin__nav">
        <router-link
          v-for="item in nav"
          :key="item.to"
          :to="item.to"
          class="admin__nav-link"
          :class="{ active: route.path.startsWith(item.to) }"
        >
          <span class="admin__nav-icon">{{ item.icon }}</span>
          {{ item.label }}
        </router-link>
      </nav>

      <div class="admin__sidebar-footer">
        <a href="/" target="_blank" class="admin__view-site">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
          Ver sitio
        </a>
        <button class="admin__logout" @click="handleLogout">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
          Cerrar sesión
        </button>
      </div>
    </aside>

    <main class="admin__content">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.admin {
  display: flex;
  min-height: 100vh;
  background: #F4EDE6;
  font-family: var(--font-sans);
}

.admin__sidebar {
  width: 220px;
  flex-shrink: 0;
  background: var(--color-bg-dark);
  display: flex;
  flex-direction: column;
  padding: 32px 20px;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  z-index: 50;
}

.admin__brand {
  display: flex;
  flex-direction: column;
  gap: 3px;
  padding-bottom: 28px;
  border-bottom: 1px solid rgba(250,243,236,0.08);
  margin-bottom: 28px;
}

.admin__brand-name {
  font-family: var(--font-serif);
  font-size: 1rem;
  font-style: italic;
  font-weight: 500;
  color: var(--color-text-dark-bg);
}

.admin__brand-sub {
  font-size: 0.58rem;
  font-weight: 300;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: rgba(250,243,236,0.35);
}

.admin__nav {
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.admin__nav-link {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.82rem;
  font-weight: 400;
  color: rgba(250,243,236,0.5);
  padding: 10px 12px;
  border-radius: 8px;
  transition: background var(--transition), color var(--transition);
  text-decoration: none;
}

.admin__nav-link:hover,
.admin__nav-link.active {
  background: rgba(196,97,74,0.15);
  color: var(--color-text-dark-bg);
}

.admin__nav-link.active {
  color: var(--color-rose-mid);
}

.admin__nav-icon {
  font-size: 1rem;
}

.admin__sidebar-footer {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-top: 20px;
  border-top: 1px solid rgba(250,243,236,0.08);
}

.admin__view-site,
.admin__logout {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.75rem;
  color: rgba(250,243,236,0.35);
  background: none;
  border: none;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 6px;
  transition: color var(--transition);
  text-decoration: none;
  font-family: var(--font-sans);
}

.admin__view-site:hover,
.admin__logout:hover {
  color: rgba(250,243,236,0.7);
}

.admin__content {
  flex: 1;
  margin-left: 220px;
  padding: 40px;
  min-height: 100vh;
  overflow-y: auto;
}

@media (max-width: 768px) {
  .admin__sidebar {
    width: 100%;
    height: auto;
    position: static;
    flex-direction: row;
    align-items: center;
    padding: 16px 20px;
    gap: 20px;
  }

  .admin__brand { padding-bottom: 0; border-bottom: none; margin-bottom: 0; }
  .admin__nav { flex-direction: row; flex: initial; }
  .admin__sidebar-footer { flex-direction: row; padding-top: 0; border-top: none; margin-left: auto; }

  .admin__content {
    margin-left: 0;
    padding: 24px 20px;
  }
}
</style>

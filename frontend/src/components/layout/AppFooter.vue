<script setup>
const year = new Date().getFullYear()

function scrollTo(id) {
  const el = document.getElementById(id)
  if (el) {
    const top = el.getBoundingClientRect().top + window.scrollY - 68
    window.scrollTo({ top, behavior: 'smooth' })
  }
}
</script>

<template>
  <footer class="footer">
    <div class="footer__top container">

      <!-- Logo + descripción + sociales -->
      <div class="footer__brand">
        <button class="footer__logo" @click="scrollTo('hero')">
          <span class="footer__logo-name">Pía Cordero</span>
          <span class="footer__logo-sub">Pastelería Artesanal</span>
        </button>
        <p class="footer__desc">
          Tortas y pasteles artesanales hechos con amor en Santiago de Chile. Cada creación es única y especial.
        </p>
        <div class="footer__social">
          <a href="https://instagram.com/piacordero_pasteleria" target="_blank" rel="noopener noreferrer" class="footer__social-btn" aria-label="Instagram">ig</a>
          <a href="https://facebook.com" target="_blank" rel="noopener noreferrer" class="footer__social-btn" aria-label="Facebook">fb</a>
          <a href="https://wa.me/56989646783" target="_blank" rel="noopener noreferrer" class="footer__social-btn" aria-label="WhatsApp">wa</a>
        </div>
      </div>

      <!-- Productos -->
      <div class="footer__col">
        <h4 class="footer__col-title">Productos</h4>
        <ul class="footer__links">
          <li><button @click="scrollTo('creaciones')">Tortas de cumpleaños</button></li>
          <li><button @click="scrollTo('creaciones')">Tortas de matrimonio</button></li>
          <li><button @click="scrollTo('galeria')">Pasteles individuales</button></li>
          <li><button @click="scrollTo('galeria')">Cupcakes</button></li>
          <li><button @click="scrollTo('galeria')">Macarons</button></li>
          <li><button @click="scrollTo('galeria')">Galletas decoradas</button></li>
        </ul>
      </div>

      <!-- Información -->
      <div class="footer__col">
        <h4 class="footer__col-title">Información</h4>
        <ul class="footer__links">
          <li><button @click="scrollTo('sobre-mi')">Sobre mí</button></li>
          <li><button @click="scrollTo('proceso')">Cómo pedir</button></li>
          <li><button @click="scrollTo('proceso')">Preguntas frecuentes</button></li>
          <li><button @click="scrollTo('contacto')">Despacho</button></li>
          <li><button @click="scrollTo('galeria')">Galería</button></li>
        </ul>
      </div>

      <!-- Contacto -->
      <div class="footer__col">
        <h4 class="footer__col-title">Contacto</h4>
        <ul class="footer__links">
          <li>
            <a href="https://wa.me/56989646783" target="_blank" rel="noopener noreferrer">WhatsApp</a>
          </li>
          <li>
            <a href="mailto:hola@piacordero.cl">Email</a>
          </li>
          <li>
            <a href="https://instagram.com/piacordero_pasteleria" target="_blank" rel="noopener noreferrer">Instagram</a>
          </li>
          <li>
            <span class="footer__location">Santiago, Chile</span>
          </li>
        </ul>
      </div>
    </div>

    <div class="footer__bottom container">
      <p class="footer__copy">© {{ year }} Pía Cordero Pastelería · Todos los derechos reservados</p>
      <div class="footer__bottom-right">
        <p class="footer__made">Hecho con ♥ en Santiago</p>
        <router-link to="/admin/login" class="footer__admin-link">Admin</router-link>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background: var(--color-bg-dark);
  color: var(--color-text-dark-bg);
}

.footer__top {
  display: grid;
  grid-template-columns: 1.4fr 1fr 1fr 1fr;
  gap: 48px;
  padding-top: 60px;
  padding-bottom: 48px;
  border-bottom: 1px solid rgba(250,243,236,0.08);
}

.footer__brand {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.footer__logo {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 2px;
  background: none;
  border: none;
  cursor: none;
}

.footer__logo-name {
  font-family: var(--font-serif);
  font-size: 1rem;
  font-weight: 500;
  font-style: italic;
  color: var(--color-text-dark-bg);
}

.footer__logo-sub {
  font-size: 0.55rem;
  font-weight: 300;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: rgba(250,243,236,0.45);
}

.footer__desc {
  font-size: 0.82rem;
  color: rgba(250,243,236,0.45);
  line-height: 1.7;
  font-weight: 300;
  max-width: 240px;
}

.footer__social {
  display: flex;
  gap: 8px;
}

.footer__social-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 1px solid rgba(250,243,236,0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-sans);
  font-size: 0.62rem;
  font-weight: 400;
  color: rgba(250,243,236,0.5);
  text-transform: lowercase;
  transition: border-color var(--transition), color var(--transition);
  cursor: none;
}

.footer__social-btn:hover {
  border-color: var(--color-rose-mid);
  color: var(--color-rose-mid);
}

.footer__col-title {
  font-family: var(--font-sans);
  font-size: 0.62rem;
  font-weight: 500;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: rgba(250,243,236,0.35);
  margin-bottom: 20px;
}

.footer__links {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.footer__links li button,
.footer__links li a {
  font-family: var(--font-sans);
  font-size: 0.82rem;
  font-weight: 300;
  color: rgba(250,243,236,0.55);
  background: none;
  border: none;
  padding: 0;
  cursor: none;
  transition: color var(--transition);
  text-align: left;
}

.footer__links li button:hover,
.footer__links li a:hover {
  color: var(--color-text-dark-bg);
}

.footer__location {
  font-size: 0.82rem;
  font-weight: 300;
  color: rgba(250,243,236,0.35);
}

.footer__bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 20px;
  padding-bottom: 28px;
}

.footer__copy,
.footer__made {
  font-size: 0.68rem;
  color: rgba(250,243,236,0.25);
  font-weight: 300;
  letter-spacing: 0.04em;
}

.footer__bottom-right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.footer__admin-link {
  font-size: 0.62rem;
  color: rgba(250,243,236,0.15);
  font-weight: 300;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  transition: color var(--transition);
  cursor: none;
}

.footer__admin-link:hover {
  color: rgba(250,243,236,0.45);
}

@media (max-width: 1024px) {
  .footer__top {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 600px) {
  .footer__top {
    grid-template-columns: 1fr;
    gap: 36px;
  }

  .footer__bottom {
    flex-direction: column;
    gap: 8px;
    text-align: center;
  }

  .footer__bottom-right {
    flex-direction: column;
    gap: 6px;
  }
}
</style>

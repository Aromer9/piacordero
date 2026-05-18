<script setup>
defineProps({
  content: {
    type: Object,
    default: () => ({
      phone: '+56 9 8964 6783',
      email: 'hola@piacordero.cl',
      instagram: '@piacordero_pasteleria',
      whatsapp_number: '56989646783',
      whatsapp_message: 'Hola Pía! Me gustaría encargar un pedido especial 🎂',
      location: 'Santiago, Chile',
    }),
  },
})

function openWhatsApp(whatsapp_number, whatsapp_message) {
  const msg = encodeURIComponent(whatsapp_message)
  window.open(`https://wa.me/${whatsapp_number}?text=${msg}`, '_blank')
}
</script>

<template>
  <section id="contacto" class="contact">
    <div class="contact__deco" aria-hidden="true" />
    <div class="contact__inner container">
      <p class="contact__eyebrow fade-in">Pedidos</p>
      <h2 class="contact__title fade-up">
        ¿Tienes un evento <em>especial?</em>
      </h2>
      <p class="contact__desc fade-up" data-delay="100">
        Escríbeme con anticipación y creamos juntas la torta perfecta para tu cumpleaños,
        matrimonio, baby shower o lo que imagines.
      </p>
      <div class="contact__actions fade-up" data-delay="200">
        <button
          class="contact__btn-wa"
          @click="openWhatsApp(content.whatsapp_number, content.whatsapp_message)"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
            <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"/>
          </svg>
          Escribir por WhatsApp
        </button>
        <a
          :href="`https://instagram.com/${content.instagram.replace('@','')}`"
          target="_blank"
          rel="noopener noreferrer"
          class="contact__btn-ig"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <rect x="2" y="2" width="20" height="20" rx="5" ry="5"/>
            <circle cx="12" cy="12" r="4"/>
            <circle cx="17.5" cy="6.5" r="0.5" fill="currentColor" stroke="none"/>
          </svg>
          Ver Instagram
        </a>
      </div>
    </div>
  </section>
</template>

<style scoped>
.contact {
  background: var(--color-bg-dark);
  padding: clamp(80px, 12vw, 140px) 0;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.contact__deco {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: clamp(400px, 60vw, 700px);
  height: clamp(400px, 60vw, 700px);
  border-radius: 50%;
  border: 1px solid rgba(196,97,74,0.15);
  pointer-events: none;
}

.contact__deco::before {
  content: '';
  position: absolute;
  inset: 40px;
  border-radius: 50%;
  border: 1px solid rgba(196,97,74,0.08);
}

.contact__inner {
  position: relative;
  z-index: 2;
}

.contact__eyebrow {
  font-size: 0.65rem;
  letter-spacing: 0.3em;
  text-transform: uppercase;
  color: var(--color-rose-mid);
  font-weight: 400;
  font-family: var(--font-sans);
  margin-bottom: 20px;
}

.contact__title {
  font-family: var(--font-serif);
  font-size: clamp(2rem, 4vw, 3.4rem);
  font-weight: 400;
  color: var(--color-text-dark-bg);
  margin-bottom: 20px;
  line-height: 1.15;
}

.contact__title em {
  font-style: italic;
  color: var(--color-rose-mid);
}

.contact__desc {
  font-family: var(--font-sans);
  font-size: 0.95rem;
  color: rgba(250,243,236,0.55);
  font-weight: 300;
  max-width: 520px;
  margin: 0 auto 48px;
  line-height: 1.8;
}

.contact__actions {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  flex-wrap: wrap;
}

.contact__btn-wa {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: #25D366;
  color: #fff;
  font-family: var(--font-sans);
  font-size: 0.82rem;
  font-weight: 500;
  letter-spacing: 0.04em;
  padding: 14px 28px;
  border-radius: 40px;
  border: none;
  transition: background var(--transition);
  cursor: none;
}

.contact__btn-wa:hover {
  background: #1ebe5b;
}

.contact__btn-ig {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  background: rgba(250,243,236,0.08);
  color: var(--color-text-dark-bg);
  font-family: var(--font-sans);
  font-size: 0.82rem;
  font-weight: 400;
  letter-spacing: 0.04em;
  padding: 14px 28px;
  border-radius: 40px;
  border: 1px solid rgba(250,243,236,0.2);
  transition: background var(--transition), border-color var(--transition);
  cursor: none;
}

.contact__btn-ig:hover {
  background: rgba(250,243,236,0.14);
  border-color: rgba(250,243,236,0.35);
}

@media (max-width: 480px) {
  .contact__actions {
    flex-direction: column;
    align-items: stretch;
  }

  .contact__btn-wa,
  .contact__btn-ig {
    justify-content: center;
  }
}
</style>

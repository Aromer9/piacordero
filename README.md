# Pía Cordero · Pastelería Artesanal

Sitio web minimalista para Pía Cordero Pastelería Artesanal. Diseño editorial con tonos beige cálidos y terracota, tipografía serif elegante y fotografía como protagonista.

## Stack

| Capa | Tecnología |
|------|-----------|
| Frontend | Vue 3 + Vite |
| Backend | FastAPI (Python) |
| Base de datos | MongoDB |
| Driver async | Motor |

---

## Requisitos previos

- **Node.js** 18 o superior
- **Python** 3.11 o superior
- **MongoDB** corriendo localmente en `mongodb://localhost:27017`

---

## Levantar el proyecto

### 1. Backend (FastAPI)

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

# Instalar dependencias
pip install -r requirements.txt

# Copiar variables de entorno
cp .env.example .env

# Iniciar servidor (puerto 8000)
uvicorn app.main:app --reload --port 8000
```

La API queda disponible en `http://localhost:8000`
Documentación automática: `http://localhost:8000/docs`

### 2. Poblar base de datos (seed)

Con el backend corriendo y el entorno virtual activo:

```bash
cd backend
python -m app.seed
```

Esto inserta:
- 8 productos de ejemplo con imágenes de Unsplash
- Contenido de las 4 secciones del sitio (hero, about, process, contact)

### 3. Frontend (Vue 3)

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar dev server (puerto 5173)
npm run dev
```

El sitio queda disponible en `http://localhost:5173`

> El dev server de Vite proxea `/api` y `/uploads` al backend en el puerto 8000 automáticamente, sin problemas de CORS.

---

## Variables de entorno (backend/.env)

| Variable | Descripción | Default |
|----------|-------------|---------|
| `MONGODB_URI` | URI de conexión a MongoDB | `mongodb://localhost:27017` |
| `MONGODB_DB` | Nombre de la base de datos | `piacordero` |
| `UPLOAD_DIR` | Directorio para imágenes subidas | `uploads` |
| `ALLOWED_ORIGINS` | Orígenes CORS permitidos | `http://localhost:5173` |

---

## API Endpoints

### Productos
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/products` | Lista productos (filtros: `category`, `featured`) |
| GET | `/api/products/{id}` | Detalle de un producto |
| POST | `/api/products` | Crear producto |
| PUT | `/api/products/{id}` | Actualizar producto |
| DELETE | `/api/products/{id}` | Eliminar producto |

### Contenido del sitio
| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/api/site-content` | Todo el contenido del sitio |
| GET | `/api/site-content/{section}` | Sección específica (hero/about/process/contact) |
| PUT | `/api/site-content/{section}` | Actualizar contenido de una sección |

### Imágenes
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/upload` | Subir imagen (multipart/form-data) |
| GET | `/uploads/{filename}` | Servir imagen subida |

---

## Estructura del proyecto

```
piacordero/
  backend/
    app/
      main.py           FastAPI app principal
      config.py         Settings y conexión MongoDB
      models/
        product.py      Modelo Pydantic de productos
        site_content.py Modelo de contenido del sitio
      routes/
        products.py     CRUD de productos
        site_content.py Endpoints de contenido
        upload.py       Upload de imágenes
      seed.py           Script de datos iniciales
    uploads/            Imágenes subidas
    requirements.txt
    .env.example

  frontend/
    src/
      App.vue           Layout principal + cursor
      main.js           Entry point
      router/           Vue Router
      components/
        layout/
          AppHeader.vue Nav sticky con blur
          AppFooter.vue Footer oscuro multi-columna
        sections/
          HeroSection.vue      Hero split layout
          FeaturesStrip.vue    Barra de características
          CreationsGallery.vue Galería masonry + cards destacados
          AboutSection.vue     Sobre mí con fotos superpuestas
          ProcessSection.vue   3 pasos del proceso
          ContactSection.vue   CTA oscuro + WhatsApp
          InstagramSection.vue Grid de Instagram
      composables/
        useApi.js            Wrapper de Axios
        useScrollAnimation.js Intersection Observer
      assets/styles/
        variables.css    Paleta, tipografía, espaciado
        global.css       Reset, animaciones, utilidades
    vite.config.js       Proxy al backend
```

---

## Build para producción

```bash
# Frontend
cd frontend
npm run build         # Genera /frontend/dist/

# Backend
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Para producción, servir la carpeta `dist/` con Nginx o similar, y configurar el proxy reverso hacia FastAPI.

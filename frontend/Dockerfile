FROM node:20-alpine

WORKDIR /app

# Railway (y otros) suelen poner NODE_ENV=production durante el build de Docker.
# Eso hace que `npm ci` omita devDependencies → no se instala Vite y `npm run build` falla.
ENV NODE_ENV=development

COPY package.json package-lock.json ./
# npm ci es estricto con optional deps (p. ej. @emnapi/* en rolldown); en Alpine/Linux a veces falla aunque el lock se generó en macOS.
RUN npm install --no-audit --no-fund

COPY . .

# URL pública del API (sin /api al final). En Railway: variable en el servicio Front, disponible en build.
ARG VITE_BACKEND_ORIGIN
ENV VITE_BACKEND_ORIGIN=$VITE_BACKEND_ORIGIN
# Alternativa: URL absoluta del API (p. ej. https://back.up.railway.app/api). Si falta VITE_BACKEND_ORIGIN, el origen se deduce de aquí para /uploads y axios.
ARG VITE_API_ROOT
ENV VITE_API_ROOT=$VITE_API_ROOT

RUN npm run build

ENV NODE_ENV=production

EXPOSE 4173
# serve es más estable que vite preview detrás del healthcheck de Railway
CMD ["sh", "-c", "exec ./node_modules/.bin/serve dist -s -l tcp://0.0.0.0:${PORT:-4173}"]

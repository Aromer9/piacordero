FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

# URL pública del API (sin /api al final). En Railway: variable en el servicio Front, disponible en build.
ARG VITE_BACKEND_ORIGIN
ENV VITE_BACKEND_ORIGIN=$VITE_BACKEND_ORIGIN

RUN npm run build

EXPOSE 4173
CMD ["sh", "-c", "npx vite preview --host 0.0.0.0 --port ${PORT:-4173}"]

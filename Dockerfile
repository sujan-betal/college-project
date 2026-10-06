# syntax=docker/dockerfile:1

# ---------- frontend build ----------
FROM node:20-bookworm-slim AS frontend-deps
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

FROM node:20-bookworm-slim AS frontend-builder
WORKDIR /app/frontend
ENV NEXT_TELEMETRY_DISABLED=1
COPY --from=frontend-deps /app/frontend/node_modules ./node_modules
COPY frontend/ ./
RUN npm run build

# ---------- backend deps ----------
FROM python:3.11-slim-bookworm AS backend-deps
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app/backend
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---------- runtime: nginx + next + fastapi on ONE port ----------
FROM node:20-bookworm-slim AS runtime
ENV NODE_ENV=production \
    NEXT_TELEMETRY_DISABLED=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"
RUN apt-get update \
    && apt-get install -y --no-install-recommends nginx python3 bash \
    && rm -rf /var/lib/apt/lists/* \
    && rm -f /etc/nginx/sites-enabled/default

WORKDIR /app
COPY --from=backend-deps /opt/venv /opt/venv
COPY backend/ /app/backend/
COPY --from=frontend-builder /app/frontend/.next/standalone ./frontend/
COPY --from=frontend-builder /app/frontend/.next/static ./frontend/.next/static
COPY --from=frontend-builder /app/frontend/public ./frontend/public

# ---- nginx config: /api -> fastapi, everything else -> next ----
RUN printf '%s\n' \
  'server {' \
  '    listen 80;' \
  '    server_name _;' \
  '    client_max_body_size 25M;' \
  '    location /api/ {' \
  '        proxy_pass http://127.0.0.1:8000/;' \
  '        proxy_http_version 1.1;' \
  '        proxy_set_header Host $host;' \
  '        proxy_set_header X-Real-IP $remote_addr;' \
  '        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;' \
  '        proxy_set_header X-Forwarded-Proto $scheme;' \
  '    }' \
  '    location / {' \
  '        proxy_pass http://127.0.0.1:3000;' \
  '        proxy_http_version 1.1;' \
  '        proxy_set_header Upgrade $http_upgrade;' \
  "        proxy_set_header Connection 'upgrade';" \
  '        proxy_set_header Host $host;' \
  '        proxy_set_header X-Real-IP $remote_addr;' \
  '        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;' \
  '    }' \
  '}' \
  > /etc/nginx/conf.d/app.conf

# ---- entrypoint: run fastapi + next + nginx in one container ----
RUN printf '%s\n' \
  '#!/bin/bash' \
  'set -euo pipefail' \
  'cd /app/backend' \
  'uvicorn app.main:app --host 127.0.0.1 --port 8000 &' \
  'BACKEND_PID=$!' \
  'cd /app/frontend' \
  'PORT=3000 HOSTNAME=127.0.0.1 node server.js &' \
  'FRONTEND_PID=$!' \
  'nginx -g "daemon off;" &' \
  'NGINX_PID=$!' \
  'shutdown() {' \
  '  kill "$BACKEND_PID" "$FRONTEND_PID" "$NGINX_PID" 2>/dev/null || true' \
  '  exit 0' \
  '}' \
  'trap shutdown SIGTERM SIGINT' \
  'wait -n' \
  > /usr/local/bin/entrypoint.sh \
  && chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 80

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
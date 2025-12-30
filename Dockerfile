# Stage 1: Build Frontend (Astro)
FROM node:20-alpine AS frontend-build
WORKDIR /app/frontend

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Stage 2: Backend & Runtime (Python + Nginx)
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    nginx \
    supervisor \
    gettext-base \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy frontend build from Stage 1
COPY --from=frontend-build /app/frontend/dist /app/frontend/dist

# Setup Configs
COPY deployment/nginx.conf /etc/nginx/sites-available/default
RUN rm -f /etc/nginx/sites-enabled/default && \
    ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

COPY deployment/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY deployment/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Environment
ENV PORT=80
EXPOSE $PORT

ENTRYPOINT ["/entrypoint.sh"]

#!/bin/bash
set -e

echo "🚀 Starting Flacon-Cloud Container..."

# Set default PORT if not provided
export PORT=${PORT:-80}

# Substitute PORT in nginx config
echo "📝 Configuring nginx to listen on port $PORT..."
envsubst '${PORT}' < /etc/nginx/sites-available/default > /tmp/nginx.conf
mv /tmp/nginx.conf /etc/nginx/sites-available/default

# Initialize/Verify Database
echo "📦 Checking database..."
# Simple check or init script could go here. 
# main.py handles table creation on startup, so we just let it run.

echo "✅ Setup complete! Starting Supervisor..."
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf

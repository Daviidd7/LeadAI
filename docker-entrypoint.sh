#!/bin/sh
# Load Docker secrets (if present) into environment variables
set -eu
SECRETS_DIR=/run/secrets
load_secret() {
  name="$1"
  var="$2"
  if [ -f "$SECRETS_DIR/$name" ]; then
    export "$var"="$(cat "$SECRETS_DIR/$name")"
  fi
}

# Map secrets to env vars used by the app
load_secret openai_api_key OPENAI_API_KEY
load_secret smtp_password SMTP_PASSWORD
load_secret twilio_auth_token TWILIO_AUTH_TOKEN
load_secret crm_api_key CRM_API_KEY
load_secret secret_key SECRET_KEY
load_secret admin_password ADMIN_PASSWORD

# If POSTGRES password secret exists, construct DATABASE_URL
if [ -f "$SECRETS_DIR/db_password" ]; then
  DB_PASS="$(cat "$SECRETS_DIR/db_password")"
  # Default user/host/db from .env or defaults
  DB_USER="${POSTGRES_USER:-postgres}"
  DB_HOST="${DB_HOST:-db}"
  DB_NAME="${DB_NAME:-lead_qualifier}"
  export DATABASE_URL="postgresql+psycopg2://${DB_USER}:${DB_PASS}@${DB_HOST}:5432/${DB_NAME}"
fi

# Run the requested command (default to uvicorn)
if [ "$#" -eq 0 ]; then
  exec uvicorn app.main:app --host 0.0.0.0 --port 8000
else
  exec "$@"
fi

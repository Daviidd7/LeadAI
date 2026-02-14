#!/bin/bash
# Helper script to initialize and deploy to Railway using the Railway CLI.
# Requires: railway CLI installed and logged in.

set -euo pipefail

# 1. Login (interactive)
# railway login

# 2. Initialize project (interactive) or link to existing
# railway init

# 3. Add Postgres plugin (optional if you prefer dashboard)
# railway add plugin postgres

# 4. Set environment variables (example; replace values)
# railway variables set SECRET_KEY="$(openssl rand -hex 32)"
# railway variables set ADMIN_USERNAME=admin
# railway variables set ADMIN_PASSWORD="your-admin-password"
# railway variables set OPENAI_API_KEY="sk-..."

# 5. Deploy (builds from repo)
# railway up

# 6. Run migrations
# railway run alembic upgrade head

echo "This script is a guide; run the commented commands interactively after installing Railway CLI." 

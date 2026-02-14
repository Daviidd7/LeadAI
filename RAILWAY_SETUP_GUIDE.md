# Railway Auto-Setup Guide

Railway doesn't read `.env` files automatically. Use one of these methods to set variables:

## Method 1: Auto-Set Script (Recommended - Fastest)

Run this PowerShell script to bulk-set all variables from your `.env`:

```powershell
# First, make sure Railway CLI is installed and you're logged in
npm install -g railway
railway login

# Navigate to your project
cd C:\Users\b6\Desktop\LeadAI

# Run the auto-setter script
.\railway_set_vars.ps1
```

This script will:
- Parse your local `.env` file
- Auto-set all variables in your Railway project
- Skip auto-managed variables (DATABASE_URL, etc.)
- Show progress as it sets each one

## Method 2: Manual UI Setup

1. Go to **https://railway.app** → Your Project → Web Service
2. Click **"Variables"** tab
3. Click **"+"** to add each variable from `RAILWAY_ENV_VARS.md`
4. Click **"Deploy"** to restart

## Method 3: One-Liner (after `railway login`)

```powershell
# Set all variables in one go (replace values as needed)
$vars = @{
  SECRET_KEY = "your-strong-secret-key-here"
  ADMIN_USERNAME = "admin"
  ADMIN_PASSWORD = "your-secure-password"
  OPENAI_API_KEY = "sk-your-openai-key-here"
  SMTP_HOST = "smtp.example.com"
  SMTP_PORT = "587"
  SMTP_USERNAME = "your-email@example.com"
  SMTP_PASSWORD = "your-email-app-password"
  SMTP_FROM_EMAIL = "noreply@yourcompany.com"
  LEAD_NOTIFICATION_EMAIL = "sales@yourcompany.com"
  TWILIO_ACCOUNT_SID = "your-twilio-account-sid"
  TWILIO_AUTH_TOKEN = "your-twilio-auth-token"
  TWILIO_FROM_NUMBER = "+1234567890"
  TWILIO_SALES_NUMBER = "+yourphone"
  CRM_BASE_URL = "https://api.hubspot.com/crm/v3/objects/contacts"
  CRM_API_KEY = "your-crm-api-key-here"
  CRM_PIPELINE_ID = "default"
  RATE_LIMIT_REQUESTS_PER_MINUTE = "30"
}

foreach ($key in $vars.Keys) {
  railway variables set "$key=$($vars[$key])"
}
```

## After Setting Variables

1. **Trigger a Deploy** (Railway Dashboard → Deploy button)
2. **Wait for deployment** (watch the logs)
3. **Run migrations**:
   ```powershell
   railway run alembic upgrade head
   ```
4. **Verify the app**:
   - Check Railway Logs for any errors
   - Visit your Railway service URL: `https://<service-name>.railway.app`
   - Test: `https://<service-name>.railway.app/healthz` (should return `{"status":"ok"}`)

## Troubleshooting

**Script fails with "railway not recognized"?**
- Railway CLI may not be in PATH. Try:
  ```powershell
  npm list -g railway
  ```
- If not installed, run: `npm install -g railway --force`

**Still getting validation errors after setting variables?**
- Double-check `DATABASE_URL` is set (should be auto-set by Postgres plugin)
- Verify no typos in variable names (case-sensitive)
- Wait 30 seconds after setting variables before redeploy

**App still crashes after deploy?**
- Check Railway Build Logs (not just runtime logs)
- Verify Postgres plugin is added
- Ensure migrations ran: `railway run alembic upgrade head`

# Railway Environment Variables Setup

Copy-paste these variable names and set their values in Railway Dashboard:

## Web Service → Variables Tab

Set each of these:

| Variable Name | Value | Notes |
|---|---|---|
| `APP_ENV` | `production` | Required |
| `SECRET_KEY` | `your-strong-random-key-here` | Generate a strong key |
| `ADMIN_USERNAME` | `admin` | |
| `ADMIN_PASSWORD` | `your-strong-password` | Must be strong! |
| `OPENAI_API_KEY` | `sk-your-key-here` | Get from OpenAI Dashboard |
| `SMTP_HOST` | `smtp.gmail.com` | Email SMTP host |
| `SMTP_PORT` | `587` | SMTP port |
| `SMTP_USERNAME` | `your-email@gmail.com` | Email username |
| `SMTP_PASSWORD` | `your-app-password` | Gmail app password (not main password) |
| `SMTP_FROM_EMAIL` | `noreply@yourcompany.com` | Sender email |
| `LEAD_NOTIFICATION_EMAIL` | `sales@yourcompany.com` | Where leads go |
| `TWILIO_ACCOUNT_SID` | `your-account-sid` | Optional (leave blank if not using) |
| `TWILIO_AUTH_TOKEN` | `your-auth-token` | Optional |
| `TWILIO_FROM_NUMBER` | `+1234567890` | Optional |
| `TWILIO_SALES_NUMBER` | `+yourphone` | Optional |
| `CRM_BASE_URL` | `https://api.hubspot.com/crm/v3/objects/contacts` | Optional |
| `CRM_API_KEY` | `your-crm-api-key` | Optional |
| `CRM_PIPELINE_ID` | `default` | Optional |
| `RATE_LIMIT_REQUESTS_PER_MINUTE` | `30` | Optional |

**NOTE:** `DATABASE_URL` will be auto-set by the PostgreSQL plugin. Do NOT manually set it.

## Steps to Fix

1. **Go to Railway Dashboard** → Your Project → Web Service
2. **Click "Variables" tab**
3. **For each variable above**, click "+" and add:
   - Variable name (left column)
   - Value (right column)
4. **Scroll down and verify PostgreSQL plugin exists** (it auto-sets `DATABASE_URL`)
5. **Click "Deploy"** or the restart button
6. Wait for deployment to complete

## After Setting Variables

Once deployed, go to Railway Dashboard → "Run" tab and execute:
```
alembic upgrade head
```

This runs migrations on the Railway database.

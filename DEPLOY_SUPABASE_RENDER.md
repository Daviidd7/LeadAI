# Deploy LeadAI: Supabase DB + Render Web Service

**No credit card needed!** Supabase (free tier) + Render (free tier) = fully deployed app.

## Part 1: Set Up Supabase PostgreSQL (5 minutes)

### 1. Create Supabase Account
- Go to [supabase.com](https://supabase.com)
- Click **Sign Up**
- Use email or GitHub (GitHub is easiest)
- Verify email

### 2. Create a Project
- Click **New project**
- **Project name**: `lead-qualifier` (or anything)
- **Database password**: Make one up (write it down!)
- **Region**: Pick nearest to you or US-East (us-east-1)
- Click **Create new project**
- Wait 2-3 minutes for Postgres to initialize

### 3. Get Connection String
- Open your project
- Left sidebar → **Project Settings** → **Database**
- Look for **Connection string**
- Copy the **"Connection pooling"** URL (it's faster):
  ```
  postgresql://postgres.XXXXX:PASSWORD@aws-0-region.pooling.supabase.com:6543/postgres
  ```

### 4. Convert for SQLAlchemy
Add `+psycopg2` right after `postgresql`:
```
postgresql+psycopg2://postgres.XXXXX:PASSWORD@aws-0-region.pooling.supabase.com:6543/postgres
```

**Save this URL** — you'll paste it into Render next.

---

## Part 2: Deploy Web Service to Render (5 minutes)

### 1. Create Web Service on Render
- Go to [render.com](https://render.com)
- Sign up / login
- Click **New +** → **Web Service**
- **Connect repository** → select your **LeadAI** GitHub repo
- Click **Connect**

### 2. Configure Service
Fill in:
- **Name**: `leadai`
- **Region**: Same as Supabase if possible (e.g., us-east)
- **Branch**: `main`
- **Leave Build/Start commands empty** (uses Dockerfile)
- **Plan**: `Free`

Scroll down, click **Create Web Service**.

### 3. Add Environment Variables
**Important**: Don't add DATABASE_URL yet — Render needs to know what service to attach to.

On your Web Service page, go to **Environment** tab and add these:

| Key | Value |
|-----|-------|
| `APP_ENV` | `production` |
| `APP_NAME` | `AI Lead Qualifier` |
| `APP_HOST` | `0.0.0.0` |
| `APP_PORT` | `8000` |
| `SECRET_KEY` | (Use something random: `your-random-secret-key-123`) |
| `ADMIN_USERNAME` | `admin` |
| `ADMIN_PASSWORD` | (Use something secure) |
| `OPENAI_API_KEY` | Your OpenAI API key from platform.openai.com/api-keys |
| `OPENAI_MODEL` | `gpt-4o-mini` |
| `SMTP_HOST` | `smtp.gmail.com` |
| `SMTP_PORT` | `587` |
| `SMTP_USERNAME` | Your Gmail address |
| `SMTP_PASSWORD` | Your Gmail app password (get from myaccount.google.com/apppasswords) |
| `SMTP_FROM_EMAIL` | Your Gmail address |
| `LEAD_NOTIFICATION_EMAIL` | Your email |
| `RATE_LIMIT_REQUESTS_PER_MINUTE` | `30` |

**Optional** (Twilio/CRM):
| `TWILIO_ACCOUNT_SID` | Your Twilio SID |
| `TWILIO_AUTH_TOKEN` | Your Twilio token |
| `TWILIO_FROM_NUMBER` | Your Twilio number |
| `CRM_BASE_URL` | `https://api.hubspot.com/crm/v3/objects/contacts` |
| `CRM_API_KEY` | Your HubSpot private app token |
| `CRM_PIPELINE_ID` | `default` |

### 4. Add DATABASE_URL Last
After all other vars are set:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | Paste the `postgresql+psycopg2://...` string from Supabase (Part 1, step 3) |

**Save all variables.**

### 5. Wait for Deploy
- Render auto-builds and deploys
- Watch the logs (should show successful build)
- Once it shows a green checkmark, your app is LIVE!

You'll get a URL like: `https://leadai.onrender.com` (or similar)

---

## Part 3: Run Database Migrations (2 minutes)

### Option A: Using Render Shell (easiest)

1. On your Render Web Service page, click **Shell** (top-right)
2. Run:
   ```bash
   alembic upgrade head
   ```
3. Should show:
   ```
   INFO [alembic.runtime.migration] Running upgrade -> 0001_create_leads_table.py
   INFO [alembic.migration] Context impl PostgresqlImpl with target metadata
   INFO [alembic.migration] Will assume transactional DDL is supported by the context impl
   ```

### Option B: From Local Machine

Open terminal and run:
```bash
export DATABASE_URL="postgresql+psycopg2://postgres.XXXXX:PASSWORD@aws-0-region.pooling.supabase.com:6543/postgres"
alembic upgrade head
```

---

## Part 4: Verify It Works! (1 minute)

Visit these URLs in your browser:

| Endpoint | Expected | Notes |
|----------|----------|-------|
| `https://leadai.onrender.com/healthz` | `{"status":"ok"}` | App is running |
| `https://leadai.onrender.com/docs` | API docs page | Swagger UI |
| `https://leadai.onrender.com/` | Lead qualification form | Main page |
| `https://leadai.onrender.com/admin/login` | Admin login page | Admin dashboard |

If any fail:
- Check Render **Logs** tab
- Look for error messages
- Common issue: missing env var → go back to Environment and verify all vars are set

---

## Troubleshooting

**"Failed to connect to database"**
- Verify `DATABASE_URL` is pasted correctly (no typos)
- Check Supabase project is still running (dashboard → Project Settings → Status)
- Firewall: Supabase has IP allowlist — usually pre-allows all on free tier, but double-check Project Settings → Database → Firewall

**"alembic migration failed"**
- Run migrations again (idempotent)
- Check Supabase has space (free tier: 500MB)
- Verify connection string again

**"502 Bad Gateway"**
- App crashed — check Render logs
- Usually missing env var or connection issue
- Add all vars from the table above

---

## Next Steps

1. ✅ Share your deployed URL (e.g., `https://leadai.onrender.com`)
2. ✅ Test the endpoints above
3. ✅ Migrations complete = database initialized
4. ✅ You're live! 🚀

---

## Free Tier Limits

**Supabase PostgreSQL (free)**:
- 500 MB database
- 2GB file storage
- Great for development/small production loads

**Render (free)**:
- 512 MB RAM
- 0.5 CPU
- Auto-pauses after 15 min inactivity (takes ~30s to wake up on next request)
- 100GB/month bandwidth

These are plenty for a lead qualification app. Upgrade anytime if needed.

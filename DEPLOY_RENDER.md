# Deploy LeadAI to Render

Render is significantly simpler than Railway. It auto-detects Docker apps and handles environment variables beautifully.

## Step 1: Connect GitHub to Render (5 minutes)

1. Go to [render.com](https://render.com) and sign up (or login)
2. Click **"New +"** → **"Web Service"**
3. Click **"Connect a repository"**
4. Authorize GitHub if prompted
5. Find and select **`LeadAI`** repo
6. Click **"Connect"**

## Step 2: Configure the Service (2 minutes)

The form will auto-detect your Dockerfile. Configure:

| Field | Value |
|-------|-------|
| **Name** | `leadai` |
| **Region** | `Oregon` (us-west) or your preference |
| **Branch** | `main` |
| **Build Command** | *(leave empty - uses Dockerfile)* |
| **Start Command** | *(leave empty - uses Dockerfile CMD)* |
| **Plan** | `Free` ✓ |

## Step 3: Add Environment Variables (5 minutes)

Scroll down to **"Environment"** section and add these variables:

| Key | Value | Notes |
|-----|-------|-------|
| `APP_ENV` | `production` | |
| `APP_NAME` | `AI Lead Qualifier` | |
| `APP_HOST` | `0.0.0.0` | |
| `APP_PORT` | `8000` | |
| `SECRET_KEY` | Use a strong random string | Change to something secure! |
| `ADMIN_USERNAME` | `admin` | |
| `ADMIN_PASSWORD` | Use a strong password | Change to something secure! |
| `OPENAI_API_KEY` | `sk-proj-...` | **Your real OpenAI API key** - get from https://platform.openai.com/api-keys |
| `OPENAI_MODEL` | `gpt-4o-mini` | |
| `SMTP_HOST` | `smtp.gmail.com` | |
| `SMTP_PORT` | `587` | |
| `SMTP_USERNAME` | Your Gmail address | |
| `SMTP_PASSWORD` | Gmail app password | Get from https://myaccount.google.com/apppasswords |
| `SMTP_FROM_EMAIL` | Your Gmail address | |
| `LEAD_NOTIFICATION_EMAIL` | Your email | |

**Optional (Twilio/CRM):**
| `TWILIO_ACCOUNT_SID` | `AC...` | Your Twilio Account SID |
| `TWILIO_AUTH_TOKEN` | Use from Twilio console | Your Twilio Auth Token |
| `TWILIO_FROM_NUMBER` | `+234...` | Your Twilio phone number |
| `CRM_BASE_URL` | `https://api.hubspot.com/crm/v3/objects/contacts` | |
| `CRM_API_KEY` | Use from HubSpot settings | Your HubSpot private app token |
| `CRM_PIPELINE_ID` | `default` | |
| `RATE_LIMIT_REQUESTS_PER_MINUTE` | `30` | |

## Step 4: Add PostgreSQL Database (2 minutes)

1. Scroll down to **"Add Database"**
2. Click **"Create PostgreSQL"**
3. Database name: `lead_qualifier` (or anything)
4. Click **"Create"**

Render will automatically add `DATABASE_URL` environment variable.

## Step 5: Deploy! (1 minute)

1. Click **"Create Web Service"**
2. Render will start building and deploying (watch the logs)
3. Takes ~2-3 minutes
4. Once it shows a green checkmark, your app is LIVE!

## Step 6: Verify It's Working

Once deployed, you'll see a URL like: `https://leadai.onrender.com`

Test these endpoints:
```
https://leadai.onrender.com/healthz          # Should return {"status":"ok"}
https://leadai.onrender.com/docs              # API documentation
https://leadai.onrender.com/                  # Lead form
https://leadai.onrender.com/admin/login       # Admin dashboard
```

## Step 7: Run Database Migrations

Once the app is live, run migrations:

```bash
# Option A: Using Render shell (if available)
# In Render Dashboard → Shell → Run:
alembic upgrade head

# Option B: Or use curl to trigger via API (if you add a migration endpoint)
```

Or manually run:
```bash
cd /app
alembic upgrade head
```

## Troubleshooting

### "Build failed"
Check the build logs in Render. Usually means:
- Docker syntax issue
- Missing environment variables
- Dependency conflicts

**Solution**: Scroll to logs, see the error, fix, and push to GitHub - Render auto-redeploys.

### "Container crashed"
Check deploy logs. Usually means missing env vars.

**Check with**:
```
railway run python -c "from app.config import get_settings; print(get_settings())"
```

### Health check failed
Render might add health checks. Add to your app or disable in Render settings.

## Next Steps

1. Update your DNS or share the Render URL
2. Test all endpoints (admin, lead form, API)
3. Monitor logs in Render Dashboard
4. Set up custom domain (optional - paid feature)

That's it! 🎉

---

**Notes:**
- Free tier has limits (512MB RAM, 0.5 CPU)
- If you need more, upgrade to $7/month
- PostgreSQL free tier: 100MB storage, limits after 3 months
- Your app will spin down after 15 min inactivity (free tier) - takes ~30s to wake up on next request

# Railway Deployment Guide (Web Dashboard)

Since the Railway CLI had install issues, we'll use the Railway web dashboard to deploy — this is often simpler and more visual.

## Step 1: Push to GitHub

First, create a GitHub repo and push your code:

1. **Create a new repo on GitHub** (https://github.com/new):
   - Name: `leadai` (or your choice)
   - Public or Private (your preference)
   - Do NOT initialize with README, .gitignore, or license

2. **Push your local repo to GitHub**:
   ```powershell
   git remote add origin https://github.com/YOUR_USERNAME/leadai.git
   git branch -M main
   git push -u origin main
   ```

3. Verify on GitHub — you should see all your project files there.

---

## Step 2: Create a Railway Project and Connect GitHub

1. Go to **https://railway.app** and sign in (or create an account).
2. Click **"New Project"** button.
3. Select **"Deploy from GitHub"**.
4. Authorize Railway to access your GitHub account.
5. Select your `leadai` repository.
6. Select the `main` branch.
7. Railway will start building automatically; monitor the build logs.

---

## Step 3: Add PostgreSQL Database Plugin

1. In your Railway project dashboard, click **"Add"** (or the **+** button).
2. Select **"Add Plugin"** → **PostgreSQL**.
3. Railway will provision a database and automatically set `DATABASE_URL` environment variable.

---

## Step 4: Configure Environment Variables

In Railway Dashboard:
1. Click on your **Web Service** (the FastAPI app).
2. Go to the **"Variables"** tab.
3. Add the following environment variables (set values for your use case):

| Variable | Example Value | Notes |
|----------|---------------|-------|
| `SECRET_KEY` | `your-strong-random-hex-string-here` | Generate a strong random key |
| `ADMIN_USERNAME` | `admin` | Login username for admin dashboard |
| `ADMIN_PASSWORD` | `YourStrongPassword!` | Strong password for admin |
| `OPENAI_API_KEY` | `sk-...` | Your OpenAI API key |
| `SMTP_HOST` | `smtp.gmail.com` | Your email SMTP host |
| `SMTP_PORT` | `587` | SMTP port |
| `SMTP_USERNAME` | `your-email@gmail.com` | Email username |
| `SMTP_PASSWORD` | `app-password` | Email app password (NOT your main password) |
| `SMTP_FROM_EMAIL` | `noreply@yourcompany.com` | Sender email |
| `LEAD_NOTIFICATION_EMAIL` | `sales@yourcompany.com` | Email to receive lead notifications |
| `TWILIO_ACCOUNT_SID` | `AC...` | (Optional) Twilio account SID |
| `TWILIO_AUTH_TOKEN` | `...` | (Optional) Twilio auth token |
| `TWILIO_FROM_NUMBER` | `+1234567890` | (Optional) Twilio phone number |
| `TWILIO_SALES_NUMBER` | `+salesphone` | (Optional) Sales phone for SMS |
| `CRM_BASE_URL` | `https://api.hubspot.com/...` | (Optional) CRM API base URL |
| `CRM_API_KEY` | `pat-...` | (Optional) CRM API key |
| `CRM_PIPELINE_ID` | `default` | (Optional) CRM pipeline ID |
| `RATE_LIMIT_REQUESTS_PER_MINUTE` | `30` | Rate limiting (default: 30) |
| `APP_ENV` | `production` | Set to production for Railway |

**Note:** `DATABASE_URL` is already set by the PostgreSQL plugin; do NOT manually override it.

---

## Step 5: Run Database Migrations

After variables are set and the app is running:

1. In Railway Dashboard, click on your **Web Service**.
2. Go to the **"Build"** or **"Deployments"** tab.
3. Look for a **"Run"** or **"Execute"** option (or click the three-dot menu).
4. Run the command:
   ```
   alembic upgrade head
   ```

Alternatively, SSH into the container (if Railway supports it in your plan) or use the **Deploy Logs** to verify migrations ran.

---

## Step 6: Verify Deployment

Once the app is deployed and migrations are complete:

1. Go to **https://<your-service-name>.railway.app** (Railway provides this URL in the Dashboard).
2. Test endpoints:
   - Health check: `https://<your-service-name>.railway.app/healthz` → should return `{"status":"ok"}`
   - API docs: `https://<your-service-name>.railway.app/docs` → FastAPI Swagger UI
   - Lead form: `https://<your-service-name>.railway.app/` → lead capture form
   - Admin login: `https://<your-service-name>.railway.app/admin/login`

---

## Step 7: Configure Custom Domain (Optional)

1. In Railway Dashboard, go to **Settings** → **Networking**.
2. Add a **Custom Domain** (requires DNS records pointing to Railway).
3. Enable **HTTPS** (Railway auto-provisions SSL certificates).

---

## Step 8: Monitor and Maintain

- **Logs:** Watch the **Build** and **Deploy** tabs for errors.
- **Database Backups:** Configure regular backups in the PostgreSQL plugin settings.
- **Restarts:** Rail automatically restarts the app on code push; you can also manually restart via the Dashboard.
- **Secret Rotation:** When you need to rotate secrets, update the variable in Railway Dashboard and redeploy (or manual restart).

---

## Troubleshooting

- **Build fails:** Check the build logs in Railway. Ensure `Dockerfile` is correct and requirements.txt has all dependencies.
- **App crashes:** Check deployment logs. Ensure all required environment variables are set.
- **Database connection error:** Verify `DATABASE_URL` is set correctly (Railway auto-sets it, but double-check the PostgreSQL plugin is active).
- **Migrations not running:** Manually trigger migrations in the "Run" command after deployment is stable.

---

## Next Steps

- Monitor the app in production.
- Set up CI/CD for automatic deploys on GitHub push (Railway does this by default).
- Configure monitoring/alerting if needed.

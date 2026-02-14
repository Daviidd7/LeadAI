Railway deployment steps for AI Lead Qualifier

Prerequisites
- GitHub account and repo access
- Railway account (https://railway.app) and Railway CLI installed (`npm i -g railway`)
- Dockerfile is present (project already Dockerized)

1) Push code to GitHub

```bash
# from project root
git init
git add .
git commit -m "Initial LeadAI app for Railway"
# create a GitHub repo and push (replace <your-repo-url>)
git remote add origin <your-repo-url>
git branch -M main
git push -u origin main
```

2) Create a Railway project and connect your repo

- On Railway: click "New Project" → "Deploy from GitHub" → select your repository and branch.
- Railway will inspect the repo and (when possible) build using the `Dockerfile`.

3) Add PostgreSQL plugin on Railway

- In Railway project dashboard: "Add Plugin" → PostgreSQL.
- Railway will create a database and set a `DATABASE_URL` environment variable for your project.

4) Configure environment variables / secrets

Essential values (set in Railway Dashboard > Variables or via CLI)
- `SECRET_KEY` — strong random string
- `ADMIN_USERNAME` and `ADMIN_PASSWORD`
- `OPENAI_API_KEY`
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`, `SMTP_FROM_EMAIL`, `LEAD_NOTIFICATION_EMAIL`
- `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_FROM_NUMBER`, `TWILIO_SALES_NUMBER` (if using)
- `CRM_BASE_URL`, `CRM_API_KEY`, `CRM_PIPELINE_ID` (if using)
- `RATE_LIMIT_REQUESTS_PER_MINUTE` (optional)

Railway will already provide `DATABASE_URL` from the plugin. Remove any conflicting DB env you set manually.

5) Deploy

- After connecting repo and setting variables, Railway will start a build. Monitor logs in the Railway dashboard.

6) Run Alembic migrations (on Railway)

Either use Railway's console UI or the CLI to run migrations in the deployed environment:

```bash
# Using Railway CLI (after login and linked project)
railway run alembic upgrade head
```

Or use the Railway web Run command to execute `alembic upgrade head`.

7) Verify

- Visit the Railway-assigned URL (from the Dashboard) and check:
  - `https://<your-service>.railway.app/healthz`
  - `https://<your-service>.railway.app/docs`

8) Post-deploy

- Configure a custom domain (optional) and enable HTTPS in Railway settings.
- Set up monitoring, alerting, and backups for the database.

Notes & tips
- Keep secrets in Railway variables; do NOT upload `.env` with live secrets to GitHub.
- If you want CI-based deploys or more control, create a GitHub Actions workflow that builds/pushes a Docker image.
- If you prefer using Railway CLI: `railway login`, `railway init`, `railway up` can be used interactively.

If you'd like, I can:
- Create a small `railway_setup.sh` script with CLI commands you can run locally (I added a helper script),
- Or help you push this repo to GitHub from your machine and walk through the Railway dashboard steps interactively.

## AI Lead Qualifier – Production-Ready GPT-4 Lead Scoring Bot

This project is a **production-grade AI-powered lead qualification system** built with **FastAPI + PostgreSQL + OpenAI**.

- Public **lead capture form** → AI qualification via GPT-4 → **CRM + email/SMS** notifications.
- Designed so you can **deploy in 2–4 hours** and show to real clients.
- Easily white-label for multiple clients by changing env variables and branding.

---

### 1. Features

- **AI lead qualification** using GPT‑4-level model (`gpt-4.1-mini` by default).
- **Scoring (0–100), priority, disqualification flag, and summary**.
- **PostgreSQL storage** of all leads & AI results.
- **Responsive lead form** and **admin dashboard**.
- **Email and optional SMS notifications** to sales.
- **CRM integration hook** (HubSpot-style API, configurable).
- **Rate limiting**, input validation, logging, and .env-based config.
- **Dockerized**, with Alembic migrations and CI workflow.

---

### 2. Local Setup (Cursor-friendly)

1. **Clone or create project in Cursor**

   - In Cursor, open a new folder `ai-lead-qualifier`.
   - Create the files/folders exactly as in this README (or use the file tree to add them).

2. **Create virtual environment**

   cd ai-lead-qualifier
   python3.11 -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   
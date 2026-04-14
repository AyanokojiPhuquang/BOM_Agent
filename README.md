# Starlink

FastAPI backend + React (Vite) frontend + Postgres. Ships with Docker Compose
for both dev (hot-reload) and prod.

## Stack

- **backend/** – Python 3.11, FastAPI, SQLAlchemy (async), Alembic, uv
- **frontend/** – React + Vite + TypeScript, served by nginx in prod
- **postgres** – 16-alpine, with a separate checkpoint DB for the BOM agent

## Prerequisites

- Docker + Docker Compose v2 (`docker compose` CLI)
- That's it. Python / Node are only needed if you want to run without Docker.

## Quick start (Docker)

```bash
# 1. Clone and enter the repo
cd starlink

# 2. Create the backend env file from the example
cp backend/.env.example backend/.env.docker
# then edit backend/.env.docker and fill in secrets
# (OPENAI_API_KEY, SMTP creds, Langfuse keys, Nhanh keys, etc.)

# 3. Drop the product datasheets into backend/data/datasheets/
#    (see "Datasheets" section below)

# 4. Start everything
docker compose -f docker-compose.dev.yml up --build

# With hot-reload file watching:
docker compose -f docker-compose.dev.yml watch
```

Services:

| Service   | URL                      | Notes                              |
|-----------|--------------------------|------------------------------------|
| Frontend  | http://localhost:5173    | Vite dev server                    |
| Backend   | http://localhost:8030    | FastAPI, docs at `/docs`           |
| Postgres  | localhost:5437           | user/pass/db: `starlink`           |

After the services are up, run the **one-time bootstrap** below — without
this, the BOM assistant has no products or datasheets to reason over.

### Database migrations

The backend container does **not** auto-run migrations. On first boot (and any
time there are new revisions) run:

```bash
docker compose -f docker-compose.dev.yml exec backend uv run alembic upgrade head
```

### Production

```bash
cp backend/.env.example backend/.env.docker   # fill in real secrets
docker compose -f docker-compose.prod.yml up -d --build
```

Prod maps the frontend (nginx) to host port `5173` and the backend to `8030`;
Postgres stays internal. Override `POSTGRES_PASSWORD` via shell env.

## Environment variables

All backend config lives in `backend/.env.docker` (Docker) or `backend/.env`
(host). See `backend/.env.example` for the full list with comments. The most
important ones:

- `DATABASE__URL` / `CHECKPOINT_DB_URL` – Postgres DSNs. Use `postgres:5432`
  inside Docker, `localhost:5437` from the host.
- `OPENAI_API_KEY` + `OPENAI_API_BASE_URL` – any OpenAI-compatible endpoint
  (OpenRouter, Azure, etc.). Leave the key empty to run the BOM assistant in
  mock mode.
- `AUTH__JWT_SECRET_KEY` – change this for any non-local deploy.
- `CORS_ORIGINS` – comma-separated list of allowed frontend origins.
- `SMTP__*`, `ESCALATION_EMAIL`, `BOM_RECIPIENT_EMAIL` – email notifications.
- `LANGFUSE_*` – optional LLM tracing; leave empty to disable.
- `NHANH__APP_ID` / `NHANH__SECRET_KEY` – Nhanh.vn OAuth app credentials.
- `NHANH__REDIRECT_URL` – OAuth redirect target; must match the URL registered
  in the Nhanh app console. For local dev, override the default (which points
  at the hosted prod backend).
- `NHANH__WEBHOOKS_VERIFY_TOKEN` – shared secret for webhook `Authorization`
  header. Must match the token configured in the Nhanh app.

## Product catalog — first-time bootstrap

The BOM agent operates on two data sources that **must be wired up before it
can produce useful output**:

1. **Datasheets** — PDF spec sheets on disk, grouped by product family.
2. **Nhanh.vn products** — the live product catalog (SKU, name, pricing,
   stock) pulled from Nhanh.vn and cached in Postgres.

After each product is ingested from Nhanh, the matcher links it to a datasheet
PDF so the agent can cite specs in its answers.

Run steps 1 → 4 in order the first time you set up an environment.

### 1. Drop datasheets on disk

The backend reads PDFs from `DATASHEETS_DIR` (default `data/datasheets`,
resolved relative to the backend working dir — `/app/data/datasheets` in
Docker, `./backend/data/datasheets` on the host).

Docker Compose bind-mounts `./backend/data` into the container, so put the
catalog on the host at:

```
backend/data/datasheets/
├── AOC/
├── DAC/
├── MPO-MTP/
├── Media Converter/
├── QSFP/
├── SFP/
└── ... (one folder per product family; PDFs inside)
```

If you relocate the folder, update `DATASHEETS_DIR` **and** the volume mount
in `docker-compose.*.yml` to match.

Generated BOM outputs land in `backend/data/generated_boms/`, uploads in
`backend/data/uploads/` — both are also mounted, so files survive container
restarts.

### 2. Authorize Nhanh.vn (OAuth)

The backend needs an OAuth access token before it can call the Nhanh.vn API.
Configure the app credentials first, then run the interactive flow.

**Required env vars** (in `backend/.env.docker`):

```bash
NHANH__APP_ID=<your app id from the Nhanh developer console>
NHANH__SECRET_KEY=<your app secret>
# Where Nhanh should redirect after authorization. Must exactly match what's
# registered in the Nhanh app console. Default points at the hosted prod
# backend — override for local/staging.
NHANH__REDIRECT_URL=http://localhost:8030/api/nhanh/callback
NHANH__WEBHOOKS_VERIFY_TOKEN=<any string; must match the Nhanh app webhook config>
```

> ⚠️ For local development Nhanh must be able to reach your `redirect_url`
> over the public internet. Either (a) run the OAuth step on the deployed
> backend and share the token-backed DB, or (b) expose your local backend via
> a tunnel (ngrok, cloudflared) and register that URL in the Nhanh console.

Then **in a browser**, while logged into the Nhanh store account that owns
the catalog, visit:

```
{backend_domain}/api/nhanh/authorize
```

Examples:

- Local dev: <http://localhost:8030/api/nhanh/authorize>
- Hosted:    <https://api-starlink.yitec.dev/api/nhanh/authorize>

Nhanh will prompt for consent and redirect to `/api/nhanh/callback?accessCode=…`.
The backend exchanges the code for a token and persists it in Postgres.

Verify the token landed:

```bash
curl http://localhost:8030/api/nhanh/token/status
# → {"has_token": true, "business_id": ..., "expired_at": "..."}
```

Tokens expire — re-run `/api/nhanh/authorize` whenever `has_token` flips to
`false` or `expired_at` is in the past.

### 3. Sync products from Nhanh

Pull the product list into the local DB. This endpoint is auth-protected,
so you need a logged-in user's JWT:

```bash
# Full sync (first time, or when you want to re-fetch everything)
curl -X POST "http://localhost:8030/api/nhanh/products/sync?force_full=true" \
  -H "Authorization: Bearer $JWT"

# Incremental sync (subsequent runs — only products changed since last sync)
curl -X POST "http://localhost:8030/api/nhanh/products/sync" \
  -H "Authorization: Bearer $JWT"
```

Note: Nhanh's `updatedAt` covers product info (name, price) but **not**
inventory. For live inventory updates, register the webhook endpoint
`POST /api/nhanh/webhook` in the Nhanh app console — it handles
`productAdd/Update/Delete`, `inventoryChange`, and `orderAdd/Update/Delete`
events, authenticated via `NHANH__WEBHOOKS_VERIFY_TOKEN`.

### 4. Match products to datasheets

Link each Nhanh product to a PDF from step 1 so the agent can cite specs:

```bash
# Match only products that don't have a datasheet yet (default)
curl -X POST http://localhost:8030/api/nhanh/products/match-datasheets \
  -H "Authorization: Bearer $JWT"

# Re-match everything (use after updating datasheets or tweaking the matcher)
curl -X POST "http://localhost:8030/api/nhanh/products/match-datasheets?rematch_all=true" \
  -H "Authorization: Bearer $JWT"
```

Check coverage at any time:

```bash
curl http://localhost:8030/api/nhanh/products/match-status \
  -H "Authorization: Bearer $JWT"
# → {"total": ..., "matched": ..., "unmatched": ...}
```

Unmatched products usually mean (a) the datasheet PDF isn't under
`backend/data/datasheets/`, or (b) the product name in Nhanh doesn't line up
with the PDF filename. Fix either and re-run step 4.

### Re-running on an existing environment

- New datasheet PDFs added → run step 4.
- Products added/changed in Nhanh → run step 3 (incremental is fine), then
  step 4 to match any newcomers. Webhooks do this automatically once
  registered.
- Token expired → re-run step 2.

### Nhanh endpoint reference

All endpoints are under `/api/nhanh` (mounted by `src/app/routers/nhanh.py`).
Endpoints marked 🔒 require a logged-in user's JWT.

| Method | Path                              | Purpose                                 |
|--------|-----------------------------------|-----------------------------------------|
| GET    | `/authorize`                      | Kick off OAuth (open in browser)        |
| GET    | `/callback`                       | OAuth redirect target (Nhanh calls it)  |
| GET    | `/token/status`                   | Is there a valid token?                 |
| POST   | `/products`                       | Search/list products from Nhanh (live)  |
| POST   | `/products/sync` 🔒               | Sync Nhanh → local DB                   |
| POST   | `/products/match-datasheets` 🔒   | Link products to datasheet PDFs         |
| GET    | `/products/match-status` 🔒       | Matched / unmatched counts              |
| POST   | `/webhook`                        | Nhanh → backend event receiver          |

## Useful commands

```bash
# Tail backend logs
docker compose -f docker-compose.dev.yml logs -f backend

# Open a shell in the backend container
docker compose -f docker-compose.dev.yml exec backend bash

# Create a new Alembic migration
docker compose -f docker-compose.dev.yml exec backend \
  uv run alembic revision --autogenerate -m "your message"

# Reset the database (destroys data!)
docker compose -f docker-compose.dev.yml down -v
```

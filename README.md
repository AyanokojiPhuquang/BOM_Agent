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
- `NHANH__*` – Nhanh.vn inventory integration; optional.

## Datasheets

The BOM assistant reads its product catalog from the path set by
`DATASHEETS_DIR` (default: `data/datasheets`, resolved relative to the backend
working dir — i.e. `/app/data/datasheets` in Docker, `./backend/data/datasheets`
on the host).

Docker Compose bind-mounts `./backend/data` into the container, so **put the
catalog on the host at**:

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

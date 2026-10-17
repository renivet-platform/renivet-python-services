# Renivet Python services — Phase 0

Fresh private FastAPI foundation. No historical code or production AI behavior imported.

## Local start

`python -m venv .venv`

`python -m pip install -e '.[dev]'`

`uvicorn app.main:app --reload --port 8000`

Check `http://localhost:8000/health` and local docs at `/docs`.

Private-network authentication, embedding model selection, inference SLO and consent need Security/Privacy approval before production. No AI service is authorized to mutate checkout, pricing, inventory or payment state.

# Renivet Python services — Phase 0.5 configuration hardening

Fresh Python 3.12+ / FastAPI foundation for private **advisory** AI. No legacy code or inference behavior.

## Windows local start

After installing dependencies in a virtual environment:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

Service health: http://127.0.0.1:8000/health. Local OpenAPI: http://127.0.0.1:8000/docs.

## Validated runtime settings

`AppSettings` (`app/core/settings.py`) loads automatically when `app.main` is imported or `create_app()` is called, failing startup if a configured value is invalid. Local defaults require no secrets. Settings come from process environment or the ignored `.env` file; use `RENIVET_ENVIRONMENT` (one of `local`, `development`, `test`, `staging`, `production`) and `RENIVET_SERVICE_NAME` (a lowercase, hyphen-separated identifier). Unprefixed `ENVIRONMENT` from the older example is **not** read; update that name in existing local `.env` files if you need a non-default environment.

FastAPI's interactive docs, ReDoc and OpenAPI JSON are available during local/test development but disabled in staging and production. The health route remains liveness only. This is not a substitute for network isolation, service-to-service authentication or authorization: private AI inference endpoints remain intentionally unimplemented until approved.

The app factory composes API routers. Versioned AI routes are unimplemented and return 404. See `docs/architecture.md` for ownership, layering and privacy constraints.

CI runs `ruff check .` and `pytest -q`, including configuration validation and docs visibility checks. Python dependency lock, authenticated private-service contract tests and production hardening remain open.

# Renivet Python services — Phase 0.4

Fresh Python 3.12+ / FastAPI foundation for private **advisory** AI. No legacy code or inference behavior.

## Windows local start

After running the engineering-os PowerShell setup from the `phase0/foundation` branch:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

Service health: http://127.0.0.1:8000/health. Local OpenAPI: http://127.0.0.1:8000/docs.

The app factory in `app/main.py` composes API routers. Only liveness is active; versioned AI routes are unimplemented and return 404. See `docs/architecture.md` for ownership, layering and privacy constraints.

CI: `ruff check .` and `pytest -q`. Python dependency lock, authenticated private-service contract tests and production hardening remain open.

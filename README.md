# Renivet Python services — Phase 0.5 configuration hardening

Fresh Python 3.12+ / FastAPI foundation for private **advisory** AI. No legacy code or inference behavior.

## Windows local start

After installing dependencies in a virtual environment:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

Service health: http://127.0.0.1:8000/health. Local OpenAPI: http://127.0.0.1:8000/docs.

## Locked Python dependencies (Phase 0.5)

The committed `uv.lock` is the single resolved, hash-bearing dependency snapshot for
Python 3.12+ across supported platforms. GitHub CI checks it on Linux/Python 3.12
and Windows/Python 3.13, and the production Docker image installs from the same
lock without choosing new versions at build time.

- **GitHub CI:** `uv lock --check`, `uv sync --locked --extra dev`,
  `uv run --locked --extra dev ruff check .`, and
  `uv run --locked --extra dev python -m pytest -q`.
- **Production Docker build:** `uv sync --locked --no-dev --no-install-project`
  in an isolated builder; only its virtual environment and app files are copied
  into the runtime image. No datasets, model weights, secrets, or migrations.
- **Security:** GitHub exports exact version-pinned dependency lists from the
  committed lockfile, separately auditing runtime and full development trees.
  The export files are disposable CI inputs, not an alternative lockfile.
- **Update process:** edit the reviewed dependency declarations in
  `pyproject.toml`, run `uv lock` in a *disposable developer environment or
  CI review branch*, commit the updated `uv.lock`, and pass CI. Do not update
  only one side of the manifest/lock pair.

**Windows laptop safety:** Your already-running Python virtual environment does
**not** need to be changed to review this PR or continue local smoke tests.
An explicit `uv sync` manages the selected environment and may replace packages;
only run it after intentionally scheduling a local Python-environment migration.
No WSL update, Docker reset, local PostgreSQL/Redis/Typesense change or service
restart is needed for a GitHub-only lockfile review.

For a **fresh, separate** Windows checkout (not the running service), install
uv 0.12.15, then run `uv sync --locked --extra dev --python 3.13`;
afterward `uv run --locked --extra dev python -m pytest -q`.
Do not copy or commit your `.env` or `.venv` directory.

## Validated runtime settings

`AppSettings` (`app/core/settings.py`) loads automatically when `app.main` is imported or `create_app()` is called, failing startup if a configured value is invalid. Local defaults require no secrets. Settings come from process environment or the ignored `.env` file; use `RENIVET_ENVIRONMENT` (one of `local`, `development`, `test`, `staging`, `production`) and `RENIVET_SERVICE_NAME` (a lowercase, hyphen-separated identifier). Unprefixed `ENVIRONMENT` from the older example is **not** read; update that name in existing local `.env` files if you need a non-default environment.

FastAPI's interactive docs, ReDoc and OpenAPI JSON are available during local/test development but disabled in staging and production. The health route remains liveness only. This is not a substitute for network isolation, service-to-service authentication or authorization: private AI inference endpoints remain intentionally unimplemented until approved.

The app factory composes API routers. Versioned AI routes are unimplemented and return 404. See `docs/architecture.md` for ownership, layering and privacy constraints.

CI tests configuration validation, API liveness and docs isolation from locked dependencies. Authenticated private-service contract tests and production hardening remain open.

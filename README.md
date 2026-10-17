# Renivet Python services — Windows/local Phase 0.3

Fresh private FastAPI foundation; no legacy code or model weights imported.

## Recommended Windows workflow

From `renivet-engineering-os`, run `dev/scripts/setup-windows.ps1`; it installs Python 3.12 virtual environment under this repo. `dev/scripts/start-apps.ps1` opens a separate PowerShell window running FastAPI.

To run manually from `renivet-python-services`:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

Check http://127.0.0.1:8000/health and http://127.0.0.1:8000/docs. `pytest -q` and `ruff check .` are CI checks.

**Scope:** Health response only. Production inference remains private and must eventually use reviewed service authentication, model, privacy, memory/CPU and data-retention controls. No payment/checkout/inventory authority. Python dependencies are range-constrained, not hashed/locked yet.

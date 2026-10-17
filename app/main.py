from fastapi import FastAPI

app = FastAPI(title="Renivet Private AI Services", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "renivet-python-services"}

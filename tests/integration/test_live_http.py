"""Exercise FastAPI over an actual loopback HTTP socket, not only TestClient."""

import os
import socket
import subprocess
import sys
import time
from contextlib import closing

import httpx


def _available_port() -> int:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as server:
        server.bind(("127.0.0.1", 0))
        return int(server.getsockname()[1])


def test_staging_http_server_exposes_health_but_no_docs_or_inference() -> None:
    port = _available_port()
    environment = dict(os.environ)
    environment["RENIVET_ENVIRONMENT"] = "staging"
    environment["RENIVET_SERVICE_NAME"] = "renivet-python-services"
    process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "app.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
            "--no-access-log",
        ],
        env=environment,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    address = f"http://127.0.0.1:{port}"
    try:
        with httpx.Client(timeout=1.0, trust_env=False) as client:
            deadline = time.monotonic() + 12.0
            response = None
            while time.monotonic() < deadline:
                if process.poll() is not None:
                    break
                try:
                    response = client.get(f"{address}/health")
                    if response.status_code == 200:
                        break
                except httpx.TransportError:
                    pass
                time.sleep(0.1)
            assert response is not None and response.status_code == 200, "FastAPI never became ready"
            assert response.json() == {"status": "ok", "service": "renivet-python-services"}

            for path in (
                "/docs",
                "/redoc",
                "/openapi.json",
                "/api/v1/recommendations",
                "/api/v1/embeddings",
            ):
                assert client.get(f"{address}{path}").status_code == 404, path
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)

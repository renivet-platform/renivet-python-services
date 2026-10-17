from fastapi import APIRouter

# Empty on purpose: no public inference or model endpoints are authorized.
router = APIRouter(prefix="/api/v1")

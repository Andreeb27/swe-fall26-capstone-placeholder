from fastapi import APIRouter, Depends

from app.application.use_cases.get_health import GetHealth
from app.interfaces.api.dependencies import get_health_use_case

router = APIRouter(prefix="/api")


@router.get("/health")
def health(use_case: GetHealth = Depends(get_health_use_case)) -> dict:
    result = use_case.execute()
    return {"status": result.status, "scale_driver": result.scale_driver}

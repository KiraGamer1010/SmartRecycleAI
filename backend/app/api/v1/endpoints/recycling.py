from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.waste_scan import WasteScanCreate, WasteScanRead
from app.services.recycling_service import create_waste_scan, list_waste_scans


router = APIRouter()


@router.get("/scans", response_model=list[WasteScanRead])
def get_scans(
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db),
) -> list[WasteScanRead]:
    return list_waste_scans(db, limit=limit)


@router.post(
    "/scans",
    response_model=WasteScanRead,
    status_code=status.HTTP_201_CREATED,
)
def create_scan(
    payload: WasteScanCreate,
    db: Session = Depends(get_db),
) -> WasteScanRead:
    return create_waste_scan(db, payload)

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.waste_scan import WasteScan
from app.schemas.waste_scan import WasteScanCreate


def create_waste_scan(db: Session, payload: WasteScanCreate) -> WasteScan:
    scan = WasteScan(**payload.model_dump())
    db.add(scan)
    db.commit()
    db.refresh(scan)
    return scan


def list_waste_scans(db: Session, limit: int = 50) -> list[WasteScan]:
    statement = select(WasteScan).order_by(WasteScan.created_at.desc()).limit(limit)
    return list(db.scalars(statement))

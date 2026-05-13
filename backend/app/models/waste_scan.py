from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class WasteScan(Base):
    __tablename__ = "waste_scans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    material_type: Mapped[str] = mapped_column(String(120), index=True)
    confidence_score: Mapped[float] = mapped_column(Float)
    recyclable: Mapped[bool] = mapped_column(Boolean, default=True)
    image_reference: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

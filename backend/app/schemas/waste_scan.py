from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class WasteScanBase(BaseModel):
    material_type: str = Field(min_length=2, max_length=120)
    confidence_score: float = Field(ge=0, le=1)
    recyclable: bool = True
    image_reference: str | None = Field(default=None, max_length=500)


class WasteScanCreate(WasteScanBase):
    pass


class WasteScanRead(WasteScanBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

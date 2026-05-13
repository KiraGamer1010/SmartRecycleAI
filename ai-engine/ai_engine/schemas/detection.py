from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    x_min: float
    y_min: float
    x_max: float
    y_max: float


class Detection(BaseModel):
    label: str
    confidence: float = Field(ge=0, le=1)
    bounding_box: BoundingBox


class DetectionResponse(BaseModel):
    source: str
    model_name: str
    inference_ms: float
    detections: list[Detection]

from pathlib import Path
from typing import Any

from ai_engine.core.config import get_settings
from ai_engine.schemas.detection import BoundingBox, Detection


class RecyclingDetector:
    def __init__(self, model_path: Path | None = None) -> None:
        settings = get_settings()
        self.model_path = model_path or settings.model_path
        self._model: Any | None = None

    @property
    def model_name(self) -> str:
        return self.model_path.name

    def is_ready(self) -> bool:
        return self.model_path.exists()

    def _load_model(self) -> Any:
        if self._model is not None:
            return self._model

        if not self.model_path.exists():
            raise RuntimeError(
                "AI model file was not found. Place a YOLO model at "
                f"{self.model_path} or update AI_MODEL_PATH."
            )

        from ultralytics import YOLO

        self._model = YOLO(str(self.model_path))
        return self._model

    def predict_image(self, image_path: Path) -> list[Detection]:
        model = self._load_model()
        results = model(str(image_path), verbose=False)
        labels = getattr(model, "names", {})
        detections: list[Detection] = []

        for result in results:
            boxes = getattr(result, "boxes", None)
            if boxes is None:
                continue

            for box in boxes:
                x_min, y_min, x_max, y_max = [float(value) for value in box.xyxy[0]]
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                label = labels.get(class_id, str(class_id)) if isinstance(labels, dict) else str(class_id)
                detections.append(
                    Detection(
                        label=label,
                        confidence=confidence,
                        bounding_box=BoundingBox(
                            x_min=x_min,
                            y_min=y_min,
                            x_max=x_max,
                            y_max=y_max,
                        ),
                    )
                )

        return detections

from pathlib import Path
from time import perf_counter

from ai_engine.schemas.detection import DetectionResponse
from ai_engine.services.detector import RecyclingDetector
from ai_engine.services.preprocessing import read_image_shape, validate_image_path


class ClassificationPipeline:
    def __init__(self, detector: RecyclingDetector | None = None) -> None:
        self.detector = detector or RecyclingDetector()

    def classify_image(self, image_path: Path, source: str | None = None) -> DetectionResponse:
        validate_image_path(image_path)
        read_image_shape(image_path)

        started_at = perf_counter()
        detections = self.detector.predict_image(image_path)
        inference_ms = (perf_counter() - started_at) * 1000

        return DetectionResponse(
            source=source or image_path.name,
            model_name=self.detector.model_name,
            inference_ms=round(inference_ms, 3),
            detections=detections,
        )

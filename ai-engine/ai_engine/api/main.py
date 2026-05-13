from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import FastAPI, File, HTTPException, UploadFile, status

from ai_engine.core.config import get_settings
from ai_engine.pipelines.classification_pipeline import ClassificationPipeline
from ai_engine.services.detector import RecyclingDetector


settings = get_settings()
detector = RecyclingDetector()
pipeline = ClassificationPipeline(detector=detector)

app = FastAPI(
    title="SmartRecycleAI AI Engine",
    version="0.1.0",
    description="Servicio independiente de vision artificial para clasificacion de residuos.",
)


@app.get("/health")
def healthcheck() -> dict[str, str | bool]:
    return {
        "status": "ok",
        "service": "ai-engine",
        "environment": settings.environment,
        "model_available": detector.is_ready(),
        "model_path": str(detector.model_path),
    }


@app.post("/detect")
async def detect_image(file: UploadFile = File(...)):
    suffix = Path(file.filename or "").suffix.lower()
    try:
        content = await file.read()
        with NamedTemporaryFile(delete=False, suffix=suffix) as temporary_file:
            temporary_file.write(content)
            temporary_path = Path(temporary_file.name)

        return pipeline.classify_image(temporary_path, source=file.filename)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    finally:
        if "temporary_path" in locals() and temporary_path.exists():
            temporary_path.unlink()

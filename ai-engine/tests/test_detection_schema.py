from ai_engine.schemas.detection import BoundingBox, Detection, DetectionResponse


def test_detection_response_contract() -> None:
    response = DetectionResponse(
        source="sample.jpg",
        model_name="yolov8n.pt",
        inference_ms=12.5,
        detections=[
            Detection(
                label="plastic",
                confidence=0.92,
                bounding_box=BoundingBox(
                    x_min=1,
                    y_min=2,
                    x_max=20,
                    y_max=40,
                ),
            )
        ],
    )

    assert response.detections[0].label == "plastic"
    assert response.detections[0].confidence == 0.92

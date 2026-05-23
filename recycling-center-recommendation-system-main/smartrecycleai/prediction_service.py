from __future__ import annotations

import math
from typing import Any

from .data_pipeline import FRIENDLY_LABELS
from .model_training import CLASS_LABELS, get_model_training_context
from .model_utils import BEST_MODEL_FILE, MODEL_MANIFEST_FILE, read_json, read_pickle


FEATURE_HELP = {
    "total_population": "Total number of residents in the municipality.",
    "urbanization_ratio": "Share of population living in urban areas. Use a value between 0 and 1.",
    "population_density_per_km2": "Residents per square kilometer.",
    "municipal_multidimensional_poverty_index": "Municipal poverty index percentage.",
    "water_deprivation_percentage": "Percentage of population with water-related deprivation.",
    "waste_kg_per_capita_day": "Average daily waste generation per person in kilograms.",
    "recyclable_kg_day": "Estimated recyclable material generated each day.",
    "collection_coverage_percentage": "Waste collection service coverage percentage.",
    "collection_gap_percentage": "Uncovered collection percentage after current service coverage.",
    "collection_center_distance_km": "Average distance to a recycling collection center.",
    "existing_collection_centers": "Number of existing collection centers.",
    "road_access_score": "Road access score used by the modeling dataset.",
    "estimated_uncollected_recyclable_kg_day": "Estimated recyclable material not reached by current collection.",
    "center_capacity_pressure_score": "Recyclable volume divided by available collection center base.",
    "eca_facility_count": "Registered recycling collection and classification facilities.",
    "active_eca_facility_count": "Registered facilities currently operating.",
    "operation_capacity_tons": "Total registered operation capacity in tons.",
    "storage_capacity_tons": "Total registered storage capacity in tons.",
    "total_hazardous_waste_kg_latest": "Latest available hazardous waste pressure in kilograms.",
    "department_population_growth_2018_2030_pct": "Projected department population growth percentage.",
}

FEATURE_CONSTRAINTS = {
    "urbanization_ratio": {"minimum": 0.0, "maximum": 1.0},
    "municipal_multidimensional_poverty_index": {"minimum": 0.0, "maximum": 100.0},
    "water_deprivation_percentage": {"minimum": 0.0, "maximum": 100.0},
    "collection_coverage_percentage": {"minimum": 0.0, "maximum": 100.0},
    "collection_gap_percentage": {"minimum": 0.0, "maximum": 100.0},
    "department_population_growth_2018_2030_pct": {"minimum": -100.0, "maximum": 300.0},
}


def _resources() -> tuple[dict[str, Any] | None, dict[str, Any] | None, str | None]:
    context = get_model_training_context()
    if not context.get("available"):
        return None, None, context.get("error") or "Model artifacts are not available."

    manifest = read_json(MODEL_MANIFEST_FILE)
    if not manifest:
        return None, None, "The model manifest is missing. Run the model training pipeline first."
    if not BEST_MODEL_FILE.exists():
        return None, None, "The selected model artifact is missing. Run the model training pipeline first."
    try:
        model_payload = read_pickle(BEST_MODEL_FILE)
    except Exception as exc:
        return None, None, f"The selected model could not be loaded: {exc}"
    return manifest, model_payload, None


def _feature_rows_from_manifest(manifest: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not manifest:
        context = get_model_training_context()
        return context.get("feature_rows", [])
    rows = []
    for item in manifest.get("feature_summary", []):
        column = item["column"]
        rows.append(
            {
                "column": column,
                "label": item.get("label") or FRIENDLY_LABELS.get(column, column.replace("_", " ").title()),
                "description": FEATURE_HELP.get(column, "Numerical planning feature used by the selected model."),
                "default": item.get("default", 0),
                "minimum": item.get("minimum", ""),
                "maximum": item.get("maximum", ""),
                "median": item.get("median", ""),
            }
        )
    return rows


def prediction_form_context() -> dict[str, Any]:
    manifest, model_payload, error = _resources()
    context = get_model_training_context()
    best_model = context.get("best_model", {})
    return {
        "available": error is None,
        "error": error,
        "fields": _feature_rows_from_manifest(manifest),
        "best_model": best_model,
        "model_name": best_model.get("display_name") or (model_payload or {}).get("display_name", ""),
        "default_probability_chart": context.get("charts", {})
        .get("prediction_system", {})
        .get("default_probability_profile", ""),
    }


def validate_prediction_input(form_data) -> tuple[dict[str, float], list[str]]:
    manifest, _, error = _resources()
    if error:
        return {}, [error]

    values: dict[str, float] = {}
    errors: list[str] = []
    feature_rows = _feature_rows_from_manifest(manifest)
    for field in feature_rows:
        column = field["column"]
        label = field["label"]
        raw_value = form_data.get(column, field.get("default", ""))
        if raw_value is None or str(raw_value).strip() == "":
            raw_value = field.get("default", 0)
        try:
            value = float(str(raw_value).replace(",", "."))
        except ValueError:
            errors.append(f"{label} must be a valid number.")
            continue
        if math.isnan(value) or math.isinf(value):
            errors.append(f"{label} must be a finite number.")
            continue
        if value < 0 and column not in {"department_population_growth_2018_2030_pct"}:
            errors.append(f"{label} cannot be negative.")
            continue
        constraint = FEATURE_CONSTRAINTS.get(column, {})
        if "minimum" in constraint and value < constraint["minimum"]:
            errors.append(f"{label} must be at least {constraint['minimum']}.")
            continue
        if "maximum" in constraint and value > constraint["maximum"]:
            errors.append(f"{label} must be at most {constraint['maximum']}.")
            continue
        values[column] = value
    return values, errors


def predict_priority(values: dict[str, float]) -> dict[str, Any]:
    import pandas as pd

    manifest, model_payload, error = _resources()
    if error:
        return {"available": False, "error": error}

    feature_columns = manifest["feature_columns"]
    missing = [column for column in feature_columns if column not in values]
    if missing:
        return {
            "available": False,
            "error": f"The prediction input is missing required fields: {', '.join(missing)}.",
        }

    pipeline = model_payload["pipeline"]
    frame = pd.DataFrame([{column: values[column] for column in feature_columns}])
    prediction_id = int(pipeline.predict(frame)[0])
    probabilities = []
    confidence = None
    if hasattr(pipeline, "predict_proba"):
        raw_probabilities = pipeline.predict_proba(frame)[0]
        model_classes = list(pipeline.classes_)
        for class_id in manifest["class_order"]:
            probability = 0.0
            if class_id in model_classes:
                probability = float(raw_probabilities[model_classes.index(class_id)])
            probabilities.append(
                {
                    "class_id": int(class_id),
                    "label": CLASS_LABELS[int(class_id)],
                    "probability": round(probability, 4),
                    "percentage": round(probability * 100, 2),
                }
            )
        confidence = round(max(item["probability"] for item in probabilities), 4)

    return {
        "available": True,
        "model_name": model_payload["display_name"],
        "prediction_id": prediction_id,
        "prediction_label": CLASS_LABELS.get(prediction_id, "Unknown class"),
        "confidence": confidence,
        "confidence_percentage": round(confidence * 100, 2) if confidence is not None else "",
        "probabilities": probabilities,
        "input_rows": [
            {
                "feature": FRIENDLY_LABELS.get(column, column.replace("_", " ").title()),
                "value": round(values[column], 4),
            }
            for column in feature_columns
        ],
        "method_summary": (
            "The form values are converted into the same feature order used during training. "
            "The saved scikit-learn pipeline applies the same imputation and preprocessing steps before generating "
            "the priority prediction and class probabilities."
        ),
    }

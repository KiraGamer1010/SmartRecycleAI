from __future__ import annotations

import json
import math
import pickle
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = PROJECT_ROOT / "models"
REPORTS_DIR = PROJECT_ROOT / "reports"
MODEL_ENGINEERING_REPORT_DIR = REPORTS_DIR / "model_engineering"
MODEL_EVALUATION_REPORT_DIR = REPORTS_DIR / "model_evaluation"
STATIC_GENERATED_DIR = PROJECT_ROOT / "static" / "generated"
MODEL_ENGINEERING_STATIC_DIR = STATIC_GENERATED_DIR / "model_engineering"
MODEL_EVALUATION_STATIC_DIR = STATIC_GENERATED_DIR / "model_evaluation"
PREDICTION_STATIC_DIR = STATIC_GENERATED_DIR / "prediction_system"

MODEL_CONTEXT_FILE = MODEL_ENGINEERING_REPORT_DIR / "model_training_context.json"
MODEL_EVALUATION_FILE = MODEL_EVALUATION_REPORT_DIR / "model_evaluation_results.json"
MODEL_METRICS_CSV = MODEL_EVALUATION_REPORT_DIR / "model_metrics.csv"
PREDICTION_SAMPLE_CSV = MODEL_ENGINEERING_REPORT_DIR / "prediction_examples.csv"
MODEL_MANIFEST_FILE = MODELS_DIR / "model_manifest.json"
BEST_MODEL_FILE = MODELS_DIR / "best_model.pkl"

RANDOM_STATE = 42
TEST_SIZE = 0.2

CHART_BG = "#0b1716"
PANEL_BG = "#10211f"
GRID_COLOR = "#27413d"
TEXT_COLOR = "#e7fff7"
MUTED_TEXT_COLOR = "#9db9b3"
GREEN = "#31d17b"
CYAN = "#35d5ff"
BLUE = "#4c83ff"
AMBER = "#d9c768"
PINK = "#ff6bcb"
SLATE = "#93a5a2"
MODEL_COLORS = [GREEN, CYAN, AMBER, BLUE, PINK, SLATE]


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def ensure_model_directories() -> None:
    for path in (
        MODELS_DIR,
        MODEL_ENGINEERING_REPORT_DIR,
        MODEL_EVALUATION_REPORT_DIR,
        MODEL_ENGINEERING_STATIC_DIR,
        MODEL_EVALUATION_STATIC_DIR,
        PREDICTION_STATIC_DIR,
    ):
        path.mkdir(parents=True, exist_ok=True)


def json_value(value: Any) -> Any:
    try:
        import numpy as np
        import pandas as pd

        if pd.isna(value):
            return ""
        if isinstance(value, np.integer):
            return int(value)
        if isinstance(value, np.floating):
            number = float(value)
            if math.isnan(number) or math.isinf(number):
                return ""
            return round(number, 6)
    except Exception:
        pass

    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return ""
        return round(value, 6)
    if isinstance(value, (int, str, bool)) or value is None:
        return value
    return str(value)


def frame_records(frame, limit: int | None = None) -> list[dict[str, Any]]:
    if limit is not None:
        frame = frame.head(limit)
    return [
        {column: json_value(row[column]) for column in frame.columns}
        for _, row in frame.iterrows()
    ]


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def write_pickle(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as file:
        pickle.dump(payload, file)


def read_pickle(path: Path) -> Any:
    with path.open("rb") as file:
        return pickle.load(file)


def prepare_axis(ax, title: str, xlabel: str = "", ylabel: str = ""):
    fig = ax.figure
    fig.patch.set_facecolor(CHART_BG)
    ax.set_facecolor(PANEL_BG)
    ax.set_title(title, color=TEXT_COLOR, pad=16, fontsize=14, fontweight="bold")
    ax.set_xlabel(xlabel, color=MUTED_TEXT_COLOR, labelpad=10)
    ax.set_ylabel(ylabel, color=MUTED_TEXT_COLOR, labelpad=10)
    ax.tick_params(colors=MUTED_TEXT_COLOR, labelsize=9)
    ax.grid(True, color=GRID_COLOR, linewidth=0.8, alpha=0.5)
    for spine in ax.spines.values():
        spine.set_color(GRID_COLOR)
    return ax


def save_plot(fig, output_dir: Path, filename: str) -> str:
    import matplotlib.pyplot as plt

    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / filename
    fig.tight_layout()
    fig.savefig(output, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return f"generated/{output_dir.name}/{filename}"


def project_relative(path: Path) -> str:
    try:
        return path.relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def static_path_to_file(static_path: str) -> Path | None:
    if not static_path:
        return None
    normalized = str(static_path).strip().lstrip("/").replace("\\", "/")
    if normalized.startswith("static/"):
        normalized = normalized.removeprefix("static/")
    parts = PurePosixPath(normalized).parts
    if not parts or ".." in parts:
        return None
    return PROJECT_ROOT / "static" / Path(*parts)


def chart_exists(static_path: str) -> bool:
    path = static_path_to_file(static_path)
    return bool(path and path.exists())

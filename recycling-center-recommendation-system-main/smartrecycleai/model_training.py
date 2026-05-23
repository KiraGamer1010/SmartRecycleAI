from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

from .data_pipeline import FRIENDLY_LABELS, MODEL_FEATURE_COLUMNS, PROCESSED_DIR
from .model_utils import (
    AMBER,
    BEST_MODEL_FILE,
    BLUE,
    CYAN,
    GREEN,
    GRID_COLOR,
    MODEL_COLORS,
    MODEL_CONTEXT_FILE,
    MODEL_ENGINEERING_REPORT_DIR,
    MODEL_ENGINEERING_STATIC_DIR,
    MODEL_EVALUATION_FILE,
    MODEL_EVALUATION_REPORT_DIR,
    MODEL_EVALUATION_STATIC_DIR,
    MODEL_MANIFEST_FILE,
    MODEL_METRICS_CSV,
    MODELS_DIR,
    MUTED_TEXT_COLOR,
    PREDICTION_SAMPLE_CSV,
    PREDICTION_STATIC_DIR,
    RANDOM_STATE,
    SLATE,
    TEST_SIZE,
    TEXT_COLOR,
    chart_exists,
    ensure_model_directories,
    frame_records,
    json_value,
    prepare_axis,
    read_json,
    read_pickle,
    save_plot,
    utc_timestamp,
    write_json,
    write_pickle,
)


TARGET_COLUMN = "priority_class_id"
TARGET_LABEL_COLUMN = "priority_label"
CLASS_LABELS = {
    0: "Not priority",
    1: "Priority",
    2: "High priority",
}

MODEL_DEFINITIONS = {
    "logistic_regression": {
        "display_name": "Logistic Regression",
        "short_name": "Logistic",
        "artifact": "logistic_regression.pkl",
        "explanation": (
            "Logistic Regression is an interpretable linear classifier that estimates the probability of each "
            "municipality priority class from standardized planning features."
        ),
        "usefulness": (
            "It is useful for SmartRecycleAI because it provides a transparent baseline: the project can see how far "
            "a simple probabilistic model can go before using more flexible tree-based algorithms."
        ),
        "code_explanation": (
            "The training pipeline imputes missing numerical values with training-set medians, scales features with "
            "StandardScaler, and fits LogisticRegression with balanced class weights."
        ),
        "hyperparameters": {
            "max_iter": 2000,
            "class_weight": "balanced",
            "solver": "lbfgs",
            "random_state": RANDOM_STATE,
        },
    },
    "decision_tree": {
        "display_name": "Decision Tree",
        "short_name": "Decision Tree",
        "artifact": "decision_tree.pkl",
        "explanation": (
            "A Decision Tree learns rule-based splits that separate municipalities by waste, access, infrastructure, "
            "and vulnerability indicators."
        ),
        "usefulness": (
            "It is useful for academic review because its decisions can be explained as a sequence of conditions, "
            "which helps connect model behavior with recycling planning logic."
        ),
        "code_explanation": (
            "The training pipeline imputes missing values and fits a controlled DecisionTreeClassifier with maximum "
            "depth and minimum leaf restrictions to reduce overfitting."
        ),
        "hyperparameters": {
            "max_depth": 6,
            "min_samples_leaf": 8,
            "class_weight": "balanced",
            "random_state": RANDOM_STATE,
        },
    },
    "random_forest": {
        "display_name": "Random Forest",
        "short_name": "Random Forest",
        "artifact": "random_forest.pkl",
        "explanation": (
            "Random Forest combines many decision trees and averages their votes, improving stability and reducing "
            "the risk that one tree overfits the training data."
        ),
        "usefulness": (
            "It is useful for SmartRecycleAI because recycling priority depends on nonlinear interactions between "
            "demand, collection gaps, facility capacity, social vulnerability, and environmental pressure."
        ),
        "code_explanation": (
            "The training pipeline imputes missing values and fits a RandomForestClassifier with reproducible random "
            "state, balanced class weights, and controlled depth."
        ),
        "hyperparameters": {
            "n_estimators": 220,
            "max_depth": 10,
            "min_samples_leaf": 4,
            "class_weight": "balanced",
            "random_state": RANDOM_STATE,
            "n_jobs": -1,
        },
    },
}


def _load_feature_matrix():
    import pandas as pd

    feature_matrix_path = PROCESSED_DIR / "model_feature_matrix.csv"
    if not feature_matrix_path.exists():
        from .data_pipeline import run_full_pipeline

        run_full_pipeline()
    if not feature_matrix_path.exists():
        raise FileNotFoundError(
            "The model feature matrix was not found. Run python createDataset/create_dataset.py first."
        )
    return pd.read_csv(feature_matrix_path, encoding="utf-8")


def _training_frame():
    frame = _load_feature_matrix()
    features = [column for column in MODEL_FEATURE_COLUMNS if column in frame.columns]
    if not features:
        raise ValueError("No model features were found in the feature matrix.")
    if TARGET_COLUMN not in frame.columns:
        raise ValueError("The priority target column was not found in the feature matrix.")

    frame = frame.dropna(subset=[TARGET_COLUMN]).copy()
    frame[TARGET_COLUMN] = frame[TARGET_COLUMN].astype(int)
    return frame, features


def _make_pipeline(slug: str):
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    from sklearn.tree import DecisionTreeClassifier

    if slug == "logistic_regression":
        return Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                (
                    "classifier",
                    LogisticRegression(
                        max_iter=2000,
                        class_weight="balanced",
                        solver="lbfgs",
                        random_state=RANDOM_STATE,
                    ),
                ),
            ]
        )
    if slug == "decision_tree":
        return Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                (
                    "classifier",
                    DecisionTreeClassifier(
                        max_depth=6,
                        min_samples_leaf=8,
                        class_weight="balanced",
                        random_state=RANDOM_STATE,
                    ),
                ),
            ]
        )
    if slug == "random_forest":
        return Pipeline(
            [
                ("imputer", SimpleImputer(strategy="median")),
                (
                    "classifier",
                    RandomForestClassifier(
                        n_estimators=220,
                        max_depth=10,
                        min_samples_leaf=4,
                        class_weight="balanced",
                        random_state=RANDOM_STATE,
                        n_jobs=-1,
                    ),
                ),
            ]
        )
    raise ValueError(f"Unknown model slug: {slug}")


def _align_probabilities(model, probabilities, class_order: list[int]):
    import numpy as np

    aligned = np.zeros((probabilities.shape[0], len(class_order)))
    model_classes = list(model.classes_)
    for index, class_id in enumerate(class_order):
        if class_id in model_classes:
            aligned[:, index] = probabilities[:, model_classes.index(class_id)]
    return aligned


def _metric_rows(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for result in results:
        metrics = result["metrics"]
        rows.append(
            {
                "model": result["display_name"],
                "accuracy": metrics["accuracy"],
                "precision": metrics["precision"],
                "recall": metrics["recall"],
                "f1_score": metrics["f1_score"],
                "roc_auc_ovr": metrics.get("roc_auc_ovr", ""),
            }
        )
    return rows


def _plot_metric_bars(results: list[dict[str, Any]], output_dir: Path, filename: str, title: str) -> str:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    metrics = ["accuracy", "precision", "recall", "f1_score"]
    labels = [result["short_name"] for result in results]
    x_positions = np.arange(len(labels))
    width = 0.18

    fig, ax = plt.subplots(figsize=(9.2, 5.2))
    for index, metric in enumerate(metrics):
        values = [result["metrics"][metric] for result in results]
        ax.bar(
            x_positions + (index - 1.5) * width,
            values,
            width,
            color=MODEL_COLORS[index % len(MODEL_COLORS)],
            label=metric.replace("_", " ").title(),
        )
    ax.set_xticks(x_positions)
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 1.05)
    prepare_axis(ax, title, "Model", "Score")
    legend = ax.legend(facecolor="#10211f", edgecolor=GRID_COLOR, ncol=2)
    for text in legend.get_texts():
        text.set_color(MUTED_TEXT_COLOR)
    return save_plot(fig, output_dir, filename)


def _plot_prediction_distribution(results: list[dict[str, Any]], y_test, output_dir: Path) -> str:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd

    labels = [CLASS_LABELS[class_id] for class_id in sorted(CLASS_LABELS)]
    distribution = pd.DataFrame({"Actual": pd.Series(y_test).map(CLASS_LABELS).value_counts()})
    for result in results:
        distribution[result["short_name"]] = (
            pd.Series(result["predictions"]).map(CLASS_LABELS).value_counts()
        )
    distribution = distribution.reindex(labels).fillna(0)

    fig, ax = plt.subplots(figsize=(9.4, 5.2))
    x_positions = np.arange(len(labels))
    width = 0.18
    for index, column in enumerate(distribution.columns):
        ax.bar(
            x_positions + (index - 1.5) * width,
            distribution[column].values,
            width,
            color=MODEL_COLORS[index % len(MODEL_COLORS)],
            label=column,
        )
    ax.set_xticks(x_positions)
    ax.set_xticklabels(labels)
    prepare_axis(ax, "Prediction Distribution by Model", "Priority class", "Municipality count")
    legend = ax.legend(facecolor="#10211f", edgecolor=GRID_COLOR, ncol=2)
    for text in legend.get_texts():
        text.set_color(MUTED_TEXT_COLOR)
    return save_plot(fig, output_dir, "prediction_distribution.png")


def _plot_confusion_matrix(result: dict[str, Any], class_order: list[int]) -> str:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np

    matrix = np.array(result["confusion_matrix"])
    labels = [CLASS_LABELS[class_id] for class_id in class_order]
    fig, ax = plt.subplots(figsize=(6.8, 5.8))
    image = ax.imshow(matrix, cmap="viridis")
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=35, ha="right")
    ax.set_yticklabels(labels)
    for row in range(matrix.shape[0]):
        for column in range(matrix.shape[1]):
            ax.text(
                column,
                row,
                f"{matrix[row, column]:.0f}",
                ha="center",
                va="center",
                color=TEXT_COLOR,
                fontweight="bold",
            )
    prepare_axis(ax, f"{result['display_name']} Confusion Matrix", "Predicted class", "Actual class")
    ax.grid(False)
    colorbar = fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    colorbar.ax.yaxis.set_tick_params(color=MUTED_TEXT_COLOR)
    plt.setp(colorbar.ax.get_yticklabels(), color=MUTED_TEXT_COLOR)
    return save_plot(fig, MODEL_EVALUATION_STATIC_DIR, f"confusion_matrix_{result['slug']}.png")


def _plot_roc_curve(result: dict[str, Any], y_test, class_order: list[int]) -> str:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from sklearn.metrics import roc_curve
    from sklearn.preprocessing import label_binarize

    probabilities = result.get("probabilities")
    if probabilities is None:
        return ""
    y_test_bin = label_binarize(y_test, classes=class_order)
    fig, ax = plt.subplots(figsize=(7.2, 5.4))
    for index, class_id in enumerate(class_order):
        fpr, tpr, _ = roc_curve(y_test_bin[:, index], probabilities[:, index])
        ax.plot(
            fpr,
            tpr,
            color=MODEL_COLORS[index % len(MODEL_COLORS)],
            linewidth=2.1,
            label=CLASS_LABELS[class_id],
        )
    ax.plot([0, 1], [0, 1], color=SLATE, linestyle="--", linewidth=1.4)
    prepare_axis(ax, f"{result['display_name']} One-vs-Rest ROC", "False positive rate", "True positive rate")
    legend = ax.legend(facecolor="#10211f", edgecolor=GRID_COLOR)
    for text in legend.get_texts():
        text.set_color(MUTED_TEXT_COLOR)
    return save_plot(fig, MODEL_EVALUATION_STATIC_DIR, f"roc_curve_{result['slug']}.png")


def _plot_roc_comparison(results: list[dict[str, Any]], y_test, class_order: list[int]) -> str:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from sklearn.metrics import roc_curve
    from sklearn.preprocessing import label_binarize

    y_test_bin = label_binarize(y_test, classes=class_order)
    fig, ax = plt.subplots(figsize=(8.4, 5.4))
    for index, result in enumerate(results):
        probabilities = result.get("probabilities")
        if probabilities is None:
            continue
        fpr, tpr, _ = roc_curve(y_test_bin.ravel(), probabilities.ravel())
        auc_value = result["metrics"].get("roc_auc_ovr")
        label = result["short_name"]
        if auc_value != "":
            label = f"{label} AUC {auc_value:.3f}"
        ax.plot(fpr, tpr, color=MODEL_COLORS[index % len(MODEL_COLORS)], linewidth=2.2, label=label)
    ax.plot([0, 1], [0, 1], color=SLATE, linestyle="--", linewidth=1.4)
    prepare_axis(ax, "Multiclass One-vs-Rest ROC Comparison", "False positive rate", "True positive rate")
    legend = ax.legend(facecolor="#10211f", edgecolor=GRID_COLOR)
    for text in legend.get_texts():
        text.set_color(MUTED_TEXT_COLOR)
    return save_plot(fig, MODEL_EVALUATION_STATIC_DIR, "roc_curve_comparison.png")


def _plot_best_model(result: dict[str, Any]) -> str:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    metrics = ["accuracy", "precision", "recall", "f1_score"]
    values = [result["metrics"][metric] for metric in metrics]
    fig, ax = plt.subplots(figsize=(7.8, 4.8))
    ax.bar(
        [metric.replace("_", " ").title() for metric in metrics],
        values,
        color=[GREEN, CYAN, AMBER, BLUE],
        width=0.62,
    )
    ax.set_ylim(0, 1.05)
    prepare_axis(ax, f"Selected Model: {result['display_name']}", "Metric", "Score")
    return save_plot(fig, MODEL_EVALUATION_STATIC_DIR, "best_model_comparison.png")


def _plot_default_probability(result: dict[str, Any], class_order: list[int]) -> str:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    probabilities = result.get("example_probability")
    if not probabilities:
        return ""
    labels = [CLASS_LABELS[class_id] for class_id in class_order]
    fig, ax = plt.subplots(figsize=(7.8, 4.6))
    ax.barh(labels, probabilities, color=[SLATE, CYAN, GREEN])
    ax.set_xlim(0, 1.0)
    prepare_axis(ax, "Prediction Probability Profile", "Probability", "")
    return save_plot(fig, PREDICTION_STATIC_DIR, "default_probability_profile.png")


def _feature_summary(frame, features: list[str]) -> list[dict[str, Any]]:
    rows = []
    for column in features:
        values = frame[column]
        rows.append(
            {
                "column": column,
                "label": FRIENDLY_LABELS.get(column, column.replace("_", " ").title()),
                "minimum": json_value(values.min()),
                "median": json_value(values.median()),
                "maximum": json_value(values.max()),
                "default": json_value(values.median()),
            }
        )
    return rows


def train_supervised_models(force: bool = False) -> dict[str, Any]:
    if not force:
        cached = read_json(MODEL_CONTEXT_FILE)
        if cached and cached.get("available") and BEST_MODEL_FILE.exists():
            required_charts = cached.get("required_chart_paths", [])
            if all(chart_exists(path) for path in required_charts):
                return cached

    ensure_model_directories()

    import pandas as pd
    from sklearn.metrics import (
        accuracy_score,
        confusion_matrix,
        f1_score,
        precision_score,
        recall_score,
        roc_auc_score,
    )
    from sklearn.model_selection import train_test_split

    frame, features = _training_frame()
    X = frame[features].apply(pd.to_numeric, errors="coerce")
    y = frame[TARGET_COLUMN].astype(int)
    class_order = sorted(y.unique().tolist())

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    results = []
    prediction_rows = []
    for slug, definition in MODEL_DEFINITIONS.items():
        pipeline = _make_pipeline(slug)
        pipeline.fit(X_train, y_train)
        predictions = pipeline.predict(X_test)
        probabilities = None
        roc_auc = ""
        if hasattr(pipeline, "predict_proba"):
            raw_probabilities = pipeline.predict_proba(X_test)
            probabilities = _align_probabilities(pipeline, raw_probabilities, class_order)
            try:
                roc_auc = float(
                    roc_auc_score(
                        y_test,
                        probabilities,
                        multi_class="ovr",
                        average="macro",
                        labels=class_order,
                    )
                )
            except ValueError:
                roc_auc = ""

        metrics = {
            "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
            "precision": round(float(precision_score(y_test, predictions, average="weighted", zero_division=0)), 4),
            "recall": round(float(recall_score(y_test, predictions, average="weighted", zero_division=0)), 4),
            "f1_score": round(float(f1_score(y_test, predictions, average="weighted", zero_division=0)), 4),
            "roc_auc_ovr": round(roc_auc, 4) if isinstance(roc_auc, float) else "",
        }
        matrix = confusion_matrix(y_test, predictions, labels=class_order).tolist()
        artifact_path = MODELS_DIR / definition["artifact"]
        artifact_payload = {
            "pipeline": pipeline,
            "slug": slug,
            "display_name": definition["display_name"],
            "features": features,
            "class_labels": CLASS_LABELS,
            "class_order": class_order,
            "trained_at": utc_timestamp(),
        }
        write_pickle(artifact_path, artifact_payload)

        model_result = {
            "slug": slug,
            "display_name": definition["display_name"],
            "short_name": definition["short_name"],
            "artifact": definition["artifact"],
            "explanation": definition["explanation"],
            "usefulness": definition["usefulness"],
            "code_explanation": definition["code_explanation"],
            "hyperparameters": definition["hyperparameters"],
            "metrics": metrics,
            "confusion_matrix": matrix,
            "predictions": [int(value) for value in predictions],
            "probabilities": probabilities,
            "chart_paths": {},
        }
        if probabilities is not None and len(probabilities):
            model_result["example_probability"] = [round(float(value), 4) for value in probabilities[0]]

        for sample_position, original_index in enumerate(X_test.index[:12]):
            confidence = ""
            if probabilities is not None:
                confidence = round(float(probabilities[sample_position].max()), 4)
            prediction_rows.append(
                {
                    "model": definition["display_name"],
                    "municipality_code": frame.loc[original_index, "municipality_code"],
                    "municipality_name": frame.loc[original_index, "municipality_name"],
                    "actual_class": CLASS_LABELS[int(y_test.loc[original_index])],
                    "predicted_class": CLASS_LABELS[int(predictions[sample_position])],
                    "confidence": confidence,
                }
            )

        results.append(model_result)

    best_result = sorted(
        results,
        key=lambda item: (item["metrics"]["f1_score"], item["metrics"]["accuracy"]),
        reverse=True,
    )[0]
    best_artifact = MODELS_DIR / best_result["artifact"]
    write_pickle(BEST_MODEL_FILE, read_pickle(best_artifact))

    for result in results:
        result["chart_paths"]["confusion_matrix"] = _plot_confusion_matrix(result, class_order)
        result["chart_paths"]["roc_curve"] = _plot_roc_curve(result, y_test, class_order)

    engineering_charts = {
        "training_results_comparison": _plot_metric_bars(
            results,
            MODEL_ENGINEERING_STATIC_DIR,
            "training_results_comparison.png",
            "Training Results Comparison",
        ),
        "prediction_distribution": _plot_prediction_distribution(results, y_test, MODEL_ENGINEERING_STATIC_DIR),
        "model_performance_summary": _plot_metric_bars(
            results,
            MODEL_ENGINEERING_STATIC_DIR,
            "model_performance_summary.png",
            "Model-Specific Performance Summary",
        ),
    }
    evaluation_charts = {
        "metrics_comparison": _plot_metric_bars(
            results,
            MODEL_EVALUATION_STATIC_DIR,
            "metrics_comparison_chart.png",
            "Comparative Evaluation Metrics",
        ),
        "roc_curve_comparison": _plot_roc_comparison(results, y_test, class_order),
        "best_model_comparison": _plot_best_model(best_result),
    }
    prediction_charts = {
        "default_probability_profile": _plot_default_probability(best_result, class_order),
    }

    prediction_frame = pd.DataFrame(prediction_rows)
    prediction_frame.to_csv(PREDICTION_SAMPLE_CSV, index=False, encoding="utf-8")
    pd.DataFrame(_metric_rows(results)).to_csv(MODEL_METRICS_CSV, index=False, encoding="utf-8")

    feature_rows = _feature_summary(frame, features)
    class_distribution = (
        y.map(CLASS_LABELS)
        .value_counts()
        .rename_axis("class_label")
        .reset_index(name="records")
    )

    manifest = {
        "trained_at": utc_timestamp(),
        "best_model_slug": best_result["slug"],
        "best_model_name": best_result["display_name"],
        "best_model_file": BEST_MODEL_FILE.name,
        "feature_columns": features,
        "feature_summary": feature_rows,
        "class_labels": {str(key): value for key, value in CLASS_LABELS.items()},
        "class_order": class_order,
        "target_column": TARGET_COLUMN,
        "target_label_column": TARGET_LABEL_COLUMN,
        "test_size": TEST_SIZE,
        "random_state": RANDOM_STATE,
    }
    write_json(MODEL_MANIFEST_FILE, manifest)

    serializable_models = []
    for result in results:
        serializable_models.append(
            {
                key: value
                for key, value in result.items()
                if key not in {"predictions", "probabilities"}
            }
        )

    context = {
        "available": True,
        "generated_at": utc_timestamp(),
        "dataset_split": {
            "total_records": int(len(frame)),
            "train_records": int(len(X_train)),
            "test_records": int(len(X_test)),
            "test_size": TEST_SIZE,
            "random_state": RANDOM_STATE,
            "target_column": TARGET_COLUMN,
            "target_description": "Municipality recycling center priority class",
            "class_distribution": frame_records(class_distribution),
            "feature_count": int(len(features)),
        },
        "feature_rows": feature_rows,
        "models": serializable_models,
        "metric_rows": _metric_rows(results),
        "hyperparameter_rows": [
            {
                "model": definition["display_name"],
                "parameter": parameter,
                "value": json_value(value),
            }
            for definition in MODEL_DEFINITIONS.values()
            for parameter, value in definition["hyperparameters"].items()
        ],
        "prediction_examples": frame_records(prediction_frame, limit=12),
        "best_model": {
            "slug": best_result["slug"],
            "display_name": best_result["display_name"],
            "selection_metric": "Highest weighted F1-score, with accuracy as tie-breaker.",
            "metrics": best_result["metrics"],
            "artifact": BEST_MODEL_FILE.name,
            "explanation": (
                f"{best_result['display_name']} was selected because it achieved the strongest weighted F1-score "
                "on the held-out test data while preserving reliable precision and recall across priority classes."
            ),
        },
        "charts": {
            "model_engineering": engineering_charts,
            "model_evaluation": evaluation_charts,
            "prediction_system": prediction_charts,
        },
        "artifact_files": {
            "models": [definition["artifact"] for definition in MODEL_DEFINITIONS.values()] + [BEST_MODEL_FILE.name],
            "reports": [
                str(MODEL_CONTEXT_FILE.relative_to(MODEL_ENGINEERING_REPORT_DIR.parent)),
                str(MODEL_EVALUATION_FILE.relative_to(MODEL_EVALUATION_REPORT_DIR.parent)),
                str(MODEL_METRICS_CSV.relative_to(MODEL_EVALUATION_REPORT_DIR.parent)),
                str(PREDICTION_SAMPLE_CSV.relative_to(MODEL_ENGINEERING_REPORT_DIR.parent)),
            ],
        },
        "roc_strategy": (
            "The target has three classes, so ROC curves are calculated with a multiclass One-vs-Rest strategy "
            "using predicted probabilities when each model exposes predict_proba."
        ),
        "required_chart_paths": [
            *engineering_charts.values(),
            *evaluation_charts.values(),
            *prediction_charts.values(),
            *[result["chart_paths"].get("confusion_matrix", "") for result in serializable_models],
            *[result["chart_paths"].get("roc_curve", "") for result in serializable_models],
        ],
    }

    write_json(MODEL_CONTEXT_FILE, context)
    write_json(MODEL_EVALUATION_FILE, context)
    clear_model_training_cache()
    return context


@lru_cache(maxsize=1)
def get_model_training_context() -> dict[str, Any]:
    try:
        return train_supervised_models(force=False)
    except Exception as exc:
        return {
            "available": False,
            "error": str(exc),
            "models": [],
            "metric_rows": [],
            "prediction_examples": [],
            "charts": {"model_engineering": {}, "model_evaluation": {}, "prediction_system": {}},
        }


def clear_model_training_cache() -> None:
    get_model_training_context.cache_clear()

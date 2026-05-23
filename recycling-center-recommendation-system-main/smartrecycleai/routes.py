from __future__ import annotations

from pathlib import Path

from flask import abort, Blueprint, render_template, request, send_from_directory

from .data_pipeline import PROCESSED_DIR, get_dashboard_context
from .model_training import get_model_training_context
from .prediction_service import prediction_form_context, predict_priority, validate_prediction_input


main_bp = Blueprint("main", __name__)

DOWNLOADABLE_FILES = {
    "kmeans_clustered_municipalities.csv",
    "kmeans_operational_recommendations.csv",
    "kmeans_scaled_feature_matrix.csv",
    "kmeans_centroid_profiles.csv",
    "smartrecycleai_integrated_dataset.csv",
    "model_feature_matrix.csv",
}


def page_context(active_page: str, title: str) -> dict:
    context = get_dashboard_context().copy()
    context.update({"active_page": active_page, "page_title": title})
    return context


@main_bp.route("/")
def home():
    return render_template("home.html", **page_context("home", "Home"))


@main_bp.route("/crisp-ml-methodology")
def methodology():
    return render_template(
        "methodology.html",
        **page_context("methodology", "CRISP-ML Methodology"),
    )


@main_bp.route("/business-understanding")
def business_understanding():
    return render_template(
        "business_understanding.html",
        **page_context("business", "Business Understanding"),
    )


@main_bp.route("/data-understanding")
def data_understanding():
    return render_template(
        "data_understanding.html",
        **page_context("data_understanding", "Data Understanding"),
    )


@main_bp.route("/data-engineering")
def data_engineering():
    return render_template(
        "data_engineering.html",
        **page_context("data_engineering", "Data Engineering"),
    )


@main_bp.route("/model-engineering")
def model_engineering():
    context = page_context("model_engineering", "Model Engineering")
    context["supervised_modeling"] = get_model_training_context()
    return render_template(
        "model_engineering.html",
        **context,
    )


@main_bp.route("/k-means-clustering")
@main_bp.route("/kmeans-clustering")
def kmeans_clustering():
    return render_template(
        "kmeans_clustering.html",
        **page_context("machine_learning", "K-Means Clustering"),
    )


@main_bp.route("/download/<filename>")
def download_processed_file(filename: str):
    safe_name = Path(filename).name
    if safe_name != filename or safe_name not in DOWNLOADABLE_FILES:
        abort(404)
    if not (PROCESSED_DIR / safe_name).exists():
        abort(404)
    return send_from_directory(PROCESSED_DIR, safe_name, as_attachment=True)


@main_bp.route("/model-evaluation")
def model_evaluation():
    context = page_context("model_evaluation", "Model Evaluation")
    context["supervised_modeling"] = get_model_training_context()
    return render_template(
        "model_evaluation.html",
        **context,
    )


@main_bp.route("/prediction-system", methods=["GET", "POST"])
def prediction_system():
    context = page_context("prediction_system", "Prediction System")
    form_context = prediction_form_context()
    errors: list[str] = []
    prediction_result = None
    submitted_values = {}

    if request.method == "POST":
        submitted_values, errors = validate_prediction_input(request.form)
        if not errors:
            prediction_result = predict_priority(submitted_values)
            if not prediction_result.get("available"):
                errors.append(prediction_result.get("error", "The prediction could not be generated."))
                prediction_result = None

    context.update(
        {
            "prediction_form": form_context,
            "prediction_errors": errors,
            "prediction_result": prediction_result,
            "submitted_values": submitted_values,
        }
    )
    return render_template("prediction_system.html", **context)


@main_bp.route("/model-deployment")
def model_deployment():
    return render_template(
        "model_deployment.html",
        **page_context("model_deployment", "Model Deployment"),
    )


@main_bp.route("/monitoring-and-maintenance")
@main_bp.route("/monitoring-maintenance")
def monitoring_maintenance():
    return render_template(
        "monitoring_maintenance.html",
        **page_context("monitoring", "Monitoring and Maintenance"),
    )


@main_bp.route("/dataset-analysis")
def dataset_analysis():
    return render_template(
        "dataset_analysis.html",
        **page_context("dataset_analysis", "Dataset Analysis"),
    )


@main_bp.route("/data-pipeline")
def data_pipeline():
    return render_template(
        "data_pipeline.html",
        **page_context("data_pipeline", "Data Pipeline"),
    )


@main_bp.route("/conclusions")
def conclusions():
    return render_template(
        "conclusions.html",
        **page_context("conclusions", "Conclusions"),
    )


@main_bp.route("/about-project")
def about_project():
    return render_template(
        "about_project.html",
        **page_context("about", "About Project"),
    )

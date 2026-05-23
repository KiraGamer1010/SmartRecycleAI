# SmartRecycleAI

SmartRecycleAI is a production-ready Flask application for intelligent recycling center recommendation, sustainability analytics, environmental data analysis, recycling accessibility assessment, machine-learning-oriented data preparation, and real K-Means clustering analysis.

The project follows the CRISP-ML workflow and presents the work as a modern AI and sustainability platform. The application is designed for academic evaluation, local execution, and Render deployment.

## Academic Submission

- Deliverable: R2-A1-S6 Project Design and Production Plan.
- Project: SMARTRECYCLEAI.
- Course: Machine Learning.
- University: University of Cundinamarca.
- Campus: Chia, Cundinamarca.
- Date: May 16, 2026.
- Authors: Juan Esteban Castiblanco, Cristian Mauricio Muñoz, Jean Pierre Gonzalez, and Juan David Capera.

## Architecture

```text
.
|-- app.py
|-- wsgi.py
|-- requirements.txt
|-- Procfile
|-- render.yaml
|-- README.md
|-- smartrecycleai/
|   |-- __init__.py
|   |-- routes.py
|   |-- data_pipeline.py
|   `-- ml_pipeline.py
|-- templates/
|   |-- base.html
|   |-- home.html
|   |-- methodology.html
|   |-- business_understanding.html
|   |-- data_understanding.html
|   |-- data_engineering.html
|   |-- model_engineering.html
|   |-- kmeans_clustering.html
|   |-- model_evaluation.html
|   |-- model_deployment.html
|   |-- monitoring_maintenance.html
|   |-- dataset_analysis.html
|   |-- data_pipeline.html
|   |-- conclusions.html
|   `-- about_project.html
|-- static/
|   |-- css/
|   |   `-- styles.css
|   `-- generated/
|-- cleanData/
|   |-- cleaning_data_eca.py
|   |-- cleaning_data_population.py
|   `-- cleaning_data_poverty.py
|-- createDataset/
|   `-- create_dataset.py
|-- datasets/
|   |-- raw source files
|   |-- municipal recommendation dataset
|   `-- processed/
`-- reports/
```

## CRISP-ML Lifecycle Coverage

The Flask navigation covers the full instructor-required CRISP-ML lifecycle:

- Home
- CRISP-ML Methodology
- Business Understanding
- Data Understanding
- Data Engineering
- Model Engineering
- K-Means Clustering
- Model Evaluation
- Model Deployment
- Monitoring and Maintenance
- Dataset Analysis
- Data Pipeline
- Conclusions
- About Project

The academic implementation includes real dataset ingestion, EDA, feature engineering, model-ready preparation, and an actual K-Means clustering phase. The platform also documents the complete downstream lifecycle required by the instructor: training strategy, validation, model evaluation, production deployment, monitoring, maintenance, drift detection, and risk review.

## Dependency Strategy

The project supports Python 3.10+ locally and Python 3.11 on Render.

Core dependencies:

- Flask: web application framework.
- Gunicorn: Linux production WSGI server for Render.
- Pandas: tabular data processing.
- NumPy: numerical operations and feature preparation.
- Matplotlib: chart generation without a SciPy dependency chain.
- Scikit-learn: K-Means clustering and StandardScaler preprocessing.
- OpenPyXL: XLSX workbook support.
- XLRD: legacy XLS workbook support.

Seaborn was intentionally removed from the runtime dependency list because current Seaborn imports SciPy at import time. On Windows, that can slow command-line scripts or appear to hang during startup. SmartRecycleAI now uses Matplotlib directly and imports heavy analytics libraries lazily, so Flask startup stays fast and preprocessing scripts do not load plotting code until charts are generated.

## Dataset Explanation

### Municipal Recommendation Dataset

This is the existing municipal modeling dataset. It contains 1,122 municipality records with accessibility, waste generation, recyclable potential, social vulnerability, collection coverage, collection center distance, existing collection center counts, road access, and recommendation target classes.

Contribution:

- Provides the supervised learning target for recycling center prioritization.
- Defines the municipality-level analytical base.
- Supplies waste, accessibility, and vulnerability features.

Quality notes:

- No missing values were detected.
- No duplicate rows were detected.
- Population scale should be interpreted together with official census references.

### Recycling Facility Registry

This source contains recycling collection and classification facility records, including company, department, municipality, facility name, operation capacity, storage capacity, compatibility, authorization, and operational status.

Contribution:

- Measures existing recycling infrastructure.
- Adds facility count, active facility count, capacity, authorization, and compatibility features.
- Supports analysis of infrastructure sufficiency against recyclable waste potential.

Quality notes:

- Capacity columns include locale-specific numeric formats.
- Some fields contain unavailable-value markers.
- Facility records are aggregated into municipality-level indicators.

### Municipal Hazardous Waste Records

This source contains municipal hazardous waste records by reporting year and physical state.

Contribution:

- Adds environmental pressure indicators.
- Supports sustainability analysis and risk-aware recycling planning.

Quality notes:

- Numeric fields require locale-aware parsing.
- The source has no department column, so the pipeline joins it only to the unambiguous municipality subset.

### Population and Housing Census Workbook

This national census workbook provides population, household, and housing unit references.

Contribution:

- Adds official census population and household context.
- Provides reliable municipality codes for integration.
- Supports consistency checks against the modeling dataset.

Quality notes:

- The workbook contains totals, municipal rows, and footer notes.
- The pipeline keeps rows with valid five-digit municipality codes.

### Department Population Projection Workbook

This workbook provides department population projections from 2018 through 2050.

Contribution:

- Adds long-term demographic pressure.
- Generates department growth features for strategic recycling infrastructure planning.

Quality notes:

- The workbook contains several geographic area categories.
- The pipeline uses total department projections for model-level features.

### Capital Household Projection Workbook

This workbook provides household projections for the capital by locality and planning zone.

Contribution:

- Adds high-resolution urban growth context.
- Supports locality-level household growth visual analysis.
- Adds city household growth features to the capital municipality record.

Quality notes:

- Locality data covers 2018 through 2035.
- Planning-zone data covers 2018 through 2024.

## Data Pipeline

The reusable pipeline is implemented in `smartrecycleai/data_pipeline.py`. The legacy preprocessing scripts remain available and now call the shared pipeline instead of duplicating logic.

Pipeline stages:

1. Source ingestion from CSV, XLS, and XLSX files.
2. English-facing column standardization for processed outputs.
3. Locale-aware numeric parsing.
4. Text normalization for geographic joins.
5. Missing value handling.
6. Duplicate detection and municipality-level aggregation.
7. Dataset integration across municipal, census, facility, waste, projection, and capital household sources.
8. Feature engineering.
9. Target encoding and numerical scaling.
10. Chart, CSV, and JSON report generation.

Run the full pipeline:

```bash
python createDataset/create_dataset.py
```

Run individual preprocessing wrappers:

```bash
python cleanData/cleaning_data_eca.py
python cleanData/cleaning_data_population.py
python cleanData/cleaning_data_poverty.py
```

Generated outputs:

- `datasets/processed/smartrecycleai_integrated_dataset.csv`
- `datasets/processed/model_feature_matrix.csv`
- Source-specific clean CSV files in `datasets/processed/`
- Chart images in `static/generated/`
- Dataset profile report in `reports/dataset_profile.json`

## Feature Engineering

The feature matrix includes:

- Total population.
- Urbanization ratio.
- Rurality ratio.
- Population density.
- Poverty and deprivation indicators.
- Waste generation and recyclable waste indicators.
- Collection coverage and collection gap.
- Distance to collection center.
- Road access score.
- Existing center count.
- Estimated uncollected recyclable waste.
- Center capacity pressure.
- Registered and active recycling facilities.
- Operation and storage capacity.
- Hazardous waste pressure.
- Department population growth.
- Encoded recommendation priority class.
- Standardized numerical features.

These features represent demand, accessibility, vulnerability, infrastructure capacity, and environmental pressure.

## Model Lifecycle Documentation

SmartRecycleAI now includes dedicated pages for the model lifecycle phases that follow data engineering:

- Model Engineering: algorithm selection, training, validation, hyperparameter tuning, and the implemented K-Means clustering workflow.
- K-Means Clustering: real unsupervised ML analysis with feature selection, median imputation, logarithmic compression, StandardScaler, elbow method, cluster assignment, centroid analysis, and strategic recycling center recommendations.
- Model Evaluation: performance metrics, cross validation, risk analysis, and expert review.
- Model Deployment: Render deployment, Flask integration, future API endpoints, documentation, staff training, and operational protocols.
- Monitoring and Maintenance: continuous supervision, model updating, data drift, concept drift, degradation detection, and ongoing risk review.

These pages explain and demonstrate how the prepared data supports recycling center recommendation, waste management analysis, sustainability scoring, and environmental decision support in institutional or municipal settings.

## K-Means Machine Learning Pipeline

The project implements a real K-Means clustering phase in `smartrecycleai/ml_pipeline.py`.

Selected feature domains:

- Population demand and population density.
- Urbanization and projected population growth.
- Recyclable waste generation and estimated uncollected recyclable waste.
- Collection gap, distance to collection center, and existing center availability.
- Active recycling facility count and operating capacity.
- Poverty and water deprivation indicators.
- Latest hazardous waste pressure.

Pipeline steps:

1. Select numerical planning features from the integrated municipal dataset.
2. Convert features to numeric values and impute missing values with medians.
3. Apply logarithmic compression to skewed population, waste, capacity, facility, and hazardous waste variables.
4. Apply `StandardScaler`.
5. Run K-Means for K=2 through K=8.
6. Select the elbow K from the inertia curve.
7. Fit the final K-Means model with a fixed random state.
8. Evaluate Silhouette Score, Davies-Bouldin Index, inertia, and WCSS.
9. Export cluster assignments, operational recommendations, scaled features, centroid profiles, and professional charts.

Implemented evaluation metrics:

- Silhouette Score: validates whether municipalities are closer to their assigned cluster than to neighboring clusters.
- Davies-Bouldin Index: evaluates compactness and separation; lower values are better.
- Inertia: reports the sum of squared distances from municipalities to their assigned centroids.
- WCSS: within-cluster sum of squares, equivalent to K-Means inertia in scikit-learn.

Generated ML artifacts:

- `datasets/processed/kmeans_clustered_municipalities.csv`
- `datasets/processed/kmeans_operational_recommendations.csv`
- `datasets/processed/kmeans_scaled_feature_matrix.csv`
- `datasets/processed/kmeans_centroid_profiles.csv`
- `static/generated/kmeans_elbow_method.png`
- `static/generated/kmeans_validation_metrics.png`
- `static/generated/kmeans_cluster_scatter.png`
- `static/generated/kmeans_centroid_profiles.png`
- `static/generated/kmeans_department_distribution.png`

Limitations:

- Clustering depends on the quality and consistency of source features.
- Unsupervised learning discovers similarity groups but does not prove causality.
- Municipal data reporting can be uneven across territories and sources.
- Recycling infrastructure, population pressure, and waste generation can change over time.
- Geographic boundary files are not included; the current geographic view summarizes clusters by department.

Future work:

- Supervised recommendation models using validated intervention outcomes.
- Predictive waste forecasting by municipality and material stream.
- Geospatial optimization with municipality boundaries and travel-time constraints.
- IoT-enabled real-time facility and collection monitoring.
- Route optimization for collection logistics.
- Reinforcement learning for adaptive policy simulations.

## R3 Supervised Model Engineering, Evaluation, and Prediction System

The final CRISP-ML academic phases are implemented as supervised model workflows inside the same Flask application.

### R3A2 Model Engineering

The supervised training pipeline is implemented in:

- `smartrecycleai/model_utils.py`
- `smartrecycleai/model_training.py`
- `smartrecycleai/prediction_service.py`

The pipeline uses the existing processed feature matrix:

- `datasets/processed/model_feature_matrix.csv`

The target variable is:

- `priority_class_id`

The implemented supervised models are:

- Logistic Regression.
- Decision Tree.
- Random Forest.

Training uses `train_test_split` with `test_size=0.2`, stratified target classes, and `random_state=42`. Each model is stored as a reusable scikit-learn pipeline so preprocessing and prediction remain consistent.

Generated model artifacts:

- `models/logistic_regression.pkl`
- `models/decision_tree.pkl`
- `models/random_forest.pkl`
- `models/best_model.pkl`
- `models/model_manifest.json`

Generated model engineering reports:

- `reports/model_engineering/model_training_context.json`
- `reports/model_engineering/prediction_examples.csv`
- `static/generated/model_engineering/training_results_comparison.png`
- `static/generated/model_engineering/prediction_distribution.png`
- `static/generated/model_engineering/model_performance_summary.png`

### R3A3 Model Evaluation

The Model Evaluation page calculates test-set metrics only after the training split has been created. The page reports:

- Accuracy.
- Precision.
- Recall.
- F1-score.
- Confusion matrix.
- Multiclass One-vs-Rest ROC curves when predicted probabilities are available.
- Best model selection explanation.

Generated model evaluation reports:

- `reports/model_evaluation/model_evaluation_results.json`
- `reports/model_evaluation/model_metrics.csv`
- `static/generated/model_evaluation/metrics_comparison_chart.png`
- `static/generated/model_evaluation/best_model_comparison.png`
- `static/generated/model_evaluation/roc_curve_comparison.png`
- `static/generated/model_evaluation/confusion_matrix_logistic_regression.png`
- `static/generated/model_evaluation/confusion_matrix_decision_tree.png`
- `static/generated/model_evaluation/confusion_matrix_random_forest.png`
- `static/generated/model_evaluation/roc_curve_logistic_regression.png`
- `static/generated/model_evaluation/roc_curve_decision_tree.png`
- `static/generated/model_evaluation/roc_curve_random_forest.png`

### R3A4 Prediction System

The Prediction System page loads `models/best_model.pkl` and validates user input through the same feature list used during training. It displays:

- Input form with realistic default values.
- Friendly validation messages.
- Predicted priority class.
- Prediction probabilities.
- Confidence score.
- Academic explanation of the prediction workflow.

Generated prediction evidence:

- `static/generated/prediction_system/default_probability_profile.png`

The prediction system is available at:

```text
/prediction-system
```

## Visual Analytics

The application renders professional Matplotlib charts:

- Recommendation priority distribution.
- Missing value rate by dataset.
- Monthly recycling potential distribution.
- Feature correlation heatmap.
- Social vulnerability and recycling access scatter plot.
- Top departments by registered recycling facilities.
- Hazardous waste reporting trend.
- Capital locality household growth.
- Normalized feature profile.
- K-Means elbow method.
- K-Means validation metrics.
- K-Means cluster scatter plot.
- K-Means centroid heatmap.
- Department-level cluster distribution.
- Supervised model training comparison.
- Supervised prediction distribution.
- Model evaluation metrics comparison.
- Confusion matrices for Logistic Regression, Decision Tree, and Random Forest.
- Multiclass One-vs-Rest ROC curves.
- Prediction probability profile.

## Screenshots

The application generates visual assets automatically in `static/generated/` when the pipeline runs. These assets are used inside the Flask pages and can also support academic reports:

- `target_distribution.png`
- `missing_values.png`
- `correlation_heatmap.png`
- `poverty_access.png`
- `feature_scaling.png`
- `kmeans_elbow_method.png`
- `kmeans_validation_metrics.png`
- `kmeans_cluster_scatter.png`
- `kmeans_centroid_profiles.png`
- `kmeans_department_distribution.png`

## Export Capabilities

The Flask application exposes guarded downloads for generated CSV artifacts:

- `/download/kmeans_clustered_municipalities.csv`
- `/download/kmeans_operational_recommendations.csv`
- `/download/kmeans_scaled_feature_matrix.csv`
- `/download/kmeans_centroid_profiles.csv`
- `/download/smartrecycleai_integrated_dataset.csv`
- `/download/model_feature_matrix.csv`

Only approved processed files can be downloaded; arbitrary file paths are rejected.

## Methodology References

- Studer et al. (2021), [CRISP-ML(Q): a machine learning process model with quality assurance](https://www.mdpi.com/2504-4990/3/2/392).
- MacQueen (1967), [original K-Means clustering methodology](https://digicoll.lib.berkeley.edu/record/113015?ln=en&v=pdf).
- scikit-learn [KMeans](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html), [Silhouette Score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.silhouette_score.html), and [Davies-Bouldin Index](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.davies_bouldin_score.html) documentation.
- World Bank [What a Waste solid waste management analytics](https://datatopics.worldbank.org/what-a-waste/).

## Local Execution

From the project directory:

```powershell
cd C:\SmartRecycleAI\recycling-center-recommendation-system-main
```

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Generate processed datasets, charts, and reports:

```powershell
python createDataset\create_dataset.py
```

This command also trains the supervised models, stores model artifacts, creates evaluation reports, and generates the R3 charts required for the Model Engineering, Model Evaluation, and Prediction System pages.

Run Flask:

```powershell
flask --app app run
```

Open:

```text
http://127.0.0.1:5000
```

## Render Deployment

Render build command:

```bash
pip install -r requirements.txt && python createDataset/create_dataset.py
```

Render start command:

```bash
gunicorn wsgi:app
```

The repository includes:

- `requirements.txt`
- `wsgi.py`
- `Procfile`
- `render.yaml`
- `.python-version`

The Render build step generates the processed datasets, charts, and cached dashboard context before the web process starts. That keeps the first production request fast and avoids chart generation during page rendering when build artifacts already exist.

The same build command also generates the supervised model artifacts required by the Prediction System. No additional heavy dependency is required beyond the existing scikit-learn stack.

Deployment steps:

1. Push the project to GitHub.
2. Create a Render Web Service.
3. Select Python as the runtime.
4. Use the build and start commands above, or deploy with `render.yaml`.
5. Confirm `PYTHON_VERSION=3.11.9`.
6. Deploy the service.

## GitHub Push Instructions

```bash
git status
git add .
git commit -m "Build production SmartRecycleAI Flask platform"
git push origin main
```

Recommended commit sequence:

1. `Flatten SmartRecycleAI Flask project structure`
2. `Optimize analytics imports and dependency compatibility`
3. `Implement CRISP-ML data engineering pipeline`
4. `Redesign AI sustainability dashboard UI`
5. `Add K-Means clustering analysis`
6. `Add Render deployment and academic documentation`

## Validation Checklist

Validated project expectations:

- Modular Flask architecture.
- Fast startup without heavy scientific imports during app import.
- Full dataset integration.
- Full CRISP-ML lifecycle navigation.
- Real K-Means clustering with StandardScaler, elbow method, cluster visualization, and centroid analysis.
- K-Means evaluation metrics, operational recommendations, export links, and academic references.
- Modern AI and sustainability themed UI.
- Responsive layouts and reveal animations.
- Matplotlib chart generation.
- Preprocessing script compatibility.
- Render-ready WSGI entry point.
- English user-facing templates, chart labels, and documentation.
- R3A2 Model Engineering page with Logistic Regression, Decision Tree, and Random Forest.
- R3A3 Model Evaluation page with comparative metrics, confusion matrices, ROC curves, and best model selection.
- R3A4 Prediction System page with form input, validation, prediction result, probability display, and confidence score.

## Final Teacher Checklist

Before final submission, collect evidence for:

- Business Understanding page.
- Data Understanding page.
- Data Engineering page.
- Model Engineering page.
- Model Evaluation page.
- Prediction System page.
- Public GitHub repository URL.
- Public Render URL.
- Final PDF report.
- Screenshots of all required Flask pages.
- Video presentation in English.
- YouTube presentation link.

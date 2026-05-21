from __future__ import annotations

from pathlib import Path
from typing import Any


KMEANS_FEATURES = [
    {
        "column": "total_population",
        "domain": "Population demand",
        "reason": "Represents the size of the potential recycling service population.",
    },
    {
        "column": "population_density_per_km2",
        "domain": "Population density",
        "reason": "Identifies dense municipalities where collection center accessibility has high impact.",
    },
    {
        "column": "urbanization_ratio",
        "domain": "Urban growth",
        "reason": "Separates urban service patterns from dispersed rural service needs.",
    },
    {
        "column": "department_population_growth_2018_2030_pct",
        "domain": "Urban growth",
        "reason": "Adds forward-looking demographic pressure for infrastructure planning.",
    },
    {
        "column": "recyclable_kg_day",
        "domain": "Waste generation",
        "reason": "Measures daily recyclable material that could be recovered.",
    },
    {
        "column": "estimated_uncollected_recyclable_kg_day",
        "domain": "Waste generation",
        "reason": "Captures recyclable material likely missed by current collection coverage.",
    },
    {
        "column": "collection_gap_percentage",
        "domain": "Recycling coverage",
        "reason": "Quantifies the remaining service gap after current collection coverage.",
    },
    {
        "column": "collection_center_distance_km",
        "domain": "Recycling accessibility",
        "reason": "Highlights access friction for residents and collection routes.",
    },
    {
        "column": "existing_collection_centers",
        "domain": "Recycling infrastructure",
        "reason": "Represents existing service availability inside the municipality.",
    },
    {
        "column": "active_eca_facility_count",
        "domain": "Recycling infrastructure",
        "reason": "Measures active registered recycling facilities connected to operational capacity.",
    },
    {
        "column": "operation_capacity_tons",
        "domain": "Recycling infrastructure",
        "reason": "Represents installed operating capacity for recyclable material handling.",
    },
    {
        "column": "center_capacity_pressure_score",
        "domain": "Infrastructure pressure",
        "reason": "Relates recyclable waste volume to the available collection center base.",
    },
    {
        "column": "municipal_multidimensional_poverty_index",
        "domain": "Social vulnerability",
        "reason": "Adds equity context for recycling access and environmental service quality.",
    },
    {
        "column": "water_deprivation_percentage",
        "domain": "Social vulnerability",
        "reason": "Provides an additional deprivation signal linked to municipal vulnerability.",
    },
    {
        "column": "total_hazardous_waste_kg_latest",
        "domain": "Environmental pressure",
        "reason": "Captures recent hazardous waste pressure where available.",
    },
]

LOG_TRANSFORM_COLUMNS = {
    "total_population",
    "population_density_per_km2",
    "recyclable_kg_day",
    "estimated_uncollected_recyclable_kg_day",
    "existing_collection_centers",
    "active_eca_facility_count",
    "operation_capacity_tons",
    "center_capacity_pressure_score",
    "total_hazardous_waste_kg_latest",
}

DEMAND_COLUMNS = [
    "total_population",
    "population_density_per_km2",
    "urbanization_ratio",
    "department_population_growth_2018_2030_pct",
    "recyclable_kg_day",
    "estimated_uncollected_recyclable_kg_day",
    "center_capacity_pressure_score",
]

SERVICE_GAP_POSITIVE_COLUMNS = [
    "collection_gap_percentage",
    "collection_center_distance_km",
    "center_capacity_pressure_score",
]

SERVICE_GAP_NEGATIVE_COLUMNS = [
    "existing_collection_centers",
    "active_eca_facility_count",
    "operation_capacity_tons",
]

SOCIAL_COLUMNS = [
    "municipal_multidimensional_poverty_index",
    "water_deprivation_percentage",
]

ENVIRONMENTAL_COLUMNS = [
    "total_hazardous_waste_kg_latest",
]

CENTROID_DISPLAY_COLUMNS = [
    "total_population",
    "population_density_per_km2",
    "recyclable_kg_day",
    "estimated_uncollected_recyclable_kg_day",
    "collection_gap_percentage",
    "collection_center_distance_km",
    "existing_collection_centers",
    "active_eca_facility_count",
    "operation_capacity_tons",
    "municipal_multidimensional_poverty_index",
    "total_hazardous_waste_kg_latest",
    "department_population_growth_2018_2030_pct",
]

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
CLUSTER_COLORS = [GREEN, CYAN, AMBER, BLUE, PINK, "#9bff9d", "#8da2ff", SLATE]


def _json_value(value: Any) -> Any:
    import math
    import numpy as np
    import pandas as pd

    if pd.isna(value):
        return ""
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating, float)):
        number = float(value)
        if math.isnan(number) or math.isinf(number):
            return ""
        return round(number, 4)
    return value


def _records(frame) -> list[dict[str, Any]]:
    return [
        {column: _json_value(row[column]) for column in frame.columns}
        for _, row in frame.iterrows()
    ]


def _friendly(column: str, friendly_labels: dict[str, str]) -> str:
    return friendly_labels.get(column, column.replace("_", " ").title())


def _prepare_axis(ax, title: str, xlabel: str = "", ylabel: str = ""):
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


def _save_plot(fig, static_generated_dir: Path, filename: str) -> str:
    import matplotlib.pyplot as plt

    static_generated_dir.mkdir(parents=True, exist_ok=True)
    output = static_generated_dir / filename
    fig.tight_layout()
    fig.savefig(output, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return filename


def _choose_elbow_k(k_values: list[int], inertias: list[float]) -> int:
    import numpy as np

    if len(k_values) <= 2:
        return k_values[-1]

    points = np.column_stack(
        [
            (np.array(k_values) - min(k_values)) / (max(k_values) - min(k_values)),
            (np.array(inertias) - min(inertias)) / (max(inertias) - min(inertias)),
        ]
    )
    start = points[0]
    end = points[-1]
    line = end - start
    distances = np.abs(np.cross(line, start - points)) / np.linalg.norm(line)
    return int(k_values[int(np.argmax(distances))])


def _signed_average(frame, positive_columns: list[str], negative_columns: list[str] | None = None):
    import pandas as pd

    columns = []
    if positive_columns:
        columns.extend([frame[column] for column in positive_columns if column in frame])
    if negative_columns:
        columns.extend([-frame[column] for column in negative_columns if column in frame])
    if not columns:
        return pd.Series(0, index=frame.index)
    return pd.concat(columns, axis=1).mean(axis=1)


def _cluster_text(priority_rank: int, dominant_signal: str) -> tuple[str, str, str]:
    if priority_rank == 1:
        return (
            "Strategic expansion priority",
            "Immediate recycling center expansion or new collection center feasibility study.",
            f"This group has the strongest combined planning pressure, led by {dominant_signal.lower()}.",
        )
    if priority_rank == 2:
        return (
            "Targeted infrastructure reinforcement",
            "Increase coverage, strengthen facility capacity, and evaluate satellite collection points.",
            f"This group shows meaningful opportunity for service improvement, especially through {dominant_signal.lower()}.",
        )
    if priority_rank == 3:
        return (
            "Managed optimization zone",
            "Monitor service gaps and prioritize route optimization before major infrastructure investment.",
            f"This group requires selective action because {dominant_signal.lower()} remains the main differentiator.",
        )
    return (
        "Stable or lower immediate need",
        "Maintain coverage, monitor demand growth, and redirect capital investment to higher-pressure clusters.",
        f"This group is comparatively less urgent, although {dominant_signal.lower()} should remain under review.",
    )


def run_kmeans_analysis(
    integrated,
    static_generated_dir: Path,
    processed_dir: Path,
    friendly_labels: dict[str, str],
) -> dict[str, Any]:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from sklearn.cluster import KMeans
    from sklearn.metrics import davies_bouldin_score, silhouette_score
    from sklearn.preprocessing import StandardScaler

    selected_features = [item["column"] for item in KMEANS_FEATURES if item["column"] in integrated.columns]
    if len(selected_features) < 3:
        raise ValueError("K-Means requires at least three available numerical features.")

    identity_columns = [
        column
        for column in ["municipality_code", "municipality_name", "department_name", "priority_label"]
        if column in integrated.columns
    ]
    raw_features = integrated[selected_features].apply(pd.to_numeric, errors="coerce")
    missing_counts = raw_features.isna().sum()
    medians = raw_features.median(numeric_only=True).fillna(0)
    imputed_features = raw_features.fillna(medians).fillna(0)

    transformed_features = imputed_features.copy()
    transformed_columns = []
    for column in selected_features:
        if column in LOG_TRANSFORM_COLUMNS:
            transformed_features[column] = np.log1p(transformed_features[column].clip(lower=0))
            transformed_columns.append(column)

    scaler = StandardScaler()
    scaled_array = scaler.fit_transform(transformed_features)
    scaled_features = pd.DataFrame(
        scaled_array,
        columns=selected_features,
        index=integrated.index,
    )

    max_k = min(8, len(scaled_features) - 1)
    k_values = list(range(2, max_k + 1))
    inertias = []
    silhouette_values = []
    davies_bouldin_values = []
    for k in k_values:
        model = KMeans(n_clusters=k, random_state=42, n_init=20)
        labels = model.fit_predict(scaled_features)
        inertias.append(float(model.inertia_))
        silhouette_values.append(float(silhouette_score(scaled_features, labels)))
        davies_bouldin_values.append(float(davies_bouldin_score(scaled_features, labels)))

    selected_k = _choose_elbow_k(k_values, inertias)
    kmeans = KMeans(n_clusters=selected_k, random_state=42, n_init=20)
    original_cluster_labels = kmeans.fit_predict(scaled_features)
    selected_silhouette = float(silhouette_score(scaled_features, original_cluster_labels))
    selected_davies_bouldin = float(davies_bouldin_score(scaled_features, original_cluster_labels))
    selected_inertia = float(kmeans.inertia_)

    demand_score = _signed_average(scaled_features, DEMAND_COLUMNS)
    service_gap_score = _signed_average(
        scaled_features,
        SERVICE_GAP_POSITIVE_COLUMNS,
        SERVICE_GAP_NEGATIVE_COLUMNS,
    )
    social_score = _signed_average(scaled_features, SOCIAL_COLUMNS)
    environmental_score = _signed_average(scaled_features, ENVIRONMENTAL_COLUMNS)
    strategic_need_score = (
        0.38 * service_gap_score
        + 0.32 * demand_score
        + 0.18 * social_score
        + 0.12 * environmental_score
    )

    working = integrated[identity_columns + selected_features].copy()
    working["original_cluster"] = original_cluster_labels
    working["demand_pressure_score"] = demand_score
    working["service_gap_score"] = service_gap_score
    working["social_vulnerability_score"] = social_score
    working["environmental_pressure_score"] = environmental_score
    working["strategic_need_score"] = strategic_need_score

    raw_summary = (
        working.groupby("original_cluster")
        .agg(
            municipalities=("municipality_code", "count"),
            average_strategic_need_score=("strategic_need_score", "mean"),
        )
        .sort_values("average_strategic_need_score", ascending=False)
        .reset_index()
    )
    original_to_rank = {
        int(row.original_cluster): int(index + 1)
        for index, row in raw_summary.iterrows()
    }
    working["cluster_id"] = working["original_cluster"].map(original_to_rank)
    working["cluster_label"] = working["cluster_id"].map(lambda value: f"Cluster {int(value)}")

    cluster_centers = pd.DataFrame(kmeans.cluster_centers_, columns=selected_features)
    ranked_centers = cluster_centers.rename(index=original_to_rank).sort_index()
    ranked_centers.index = [f"Cluster {int(index)}" for index in ranked_centers.index]

    domain_rows = []
    for cluster_id, group in working.groupby("cluster_id"):
        domain_scores = {
            "Demand and growth": float(group["demand_pressure_score"].mean()),
            "Service gap": float(group["service_gap_score"].mean()),
            "Social vulnerability": float(group["social_vulnerability_score"].mean()),
            "Environmental pressure": float(group["environmental_pressure_score"].mean()),
        }
        dominant_signal = max(domain_scores, key=domain_scores.get)
        name, recommendation, interpretation = _cluster_text(int(cluster_id), dominant_signal)
        domain_rows.append(
            {
                "cluster_id": int(cluster_id),
                "cluster_label": f"Cluster {int(cluster_id)}",
                "cluster_name": name,
                "municipalities": int(group.shape[0]),
                "municipality_share_pct": round(float(group.shape[0] / len(working) * 100), 2),
                "priority_rank": int(cluster_id),
                "average_strategic_need_score": round(float(group["strategic_need_score"].mean()), 3),
                "demand_pressure_score": round(domain_scores["Demand and growth"], 3),
                "service_gap_score": round(domain_scores["Service gap"], 3),
                "social_vulnerability_score": round(domain_scores["Social vulnerability"], 3),
                "environmental_pressure_score": round(domain_scores["Environmental pressure"], 3),
                "dominant_signal": dominant_signal,
                "recommendation": recommendation,
                "interpretation": interpretation,
            }
        )

    cluster_summary = pd.DataFrame(domain_rows).sort_values("cluster_id")
    cluster_labels = cluster_summary.set_index("cluster_id")["cluster_name"].to_dict()
    cluster_recommendations = cluster_summary.set_index("cluster_id")["recommendation"].to_dict()
    working["cluster_name"] = working["cluster_id"].map(cluster_labels)
    working["cluster_recommendation"] = working["cluster_id"].map(cluster_recommendations)

    centroid_rows = []
    for cluster_id, group in working.groupby("cluster_id"):
        row = {
            "Cluster": f"Cluster {int(cluster_id)}",
            "Interpretation": cluster_labels[int(cluster_id)],
        }
        for column in CENTROID_DISPLAY_COLUMNS:
            if column in group:
                row[_friendly(column, friendly_labels)] = float(group[column].mean())
        centroid_rows.append(row)
    centroid_table = pd.DataFrame(centroid_rows).sort_values("Cluster")

    scaled_feature_output = integrated[identity_columns].copy()
    scaled_feature_output = pd.concat(
        [
            scaled_feature_output.reset_index(drop=True),
            scaled_features.add_prefix("scaled_").reset_index(drop=True),
            working[
                [
                    "cluster_id",
                    "cluster_label",
                    "demand_pressure_score",
                    "service_gap_score",
                    "social_vulnerability_score",
                    "environmental_pressure_score",
                    "strategic_need_score",
                ]
            ].reset_index(drop=True),
        ],
        axis=1,
    )

    cluster_output_columns = identity_columns + selected_features + [
        "cluster_id",
        "cluster_label",
        "cluster_name",
        "cluster_recommendation",
        "demand_pressure_score",
        "service_gap_score",
        "social_vulnerability_score",
        "environmental_pressure_score",
        "strategic_need_score",
    ]
    processed_dir.mkdir(parents=True, exist_ok=True)
    working[cluster_output_columns].sort_values(
        ["cluster_id", "strategic_need_score"],
        ascending=[True, False],
    ).to_csv(processed_dir / "kmeans_clustered_municipalities.csv", index=False, encoding="utf-8")
    centroid_table.to_csv(processed_dir / "kmeans_centroid_profiles.csv", index=False, encoding="utf-8")
    scaled_feature_output.to_csv(processed_dir / "kmeans_scaled_feature_matrix.csv", index=False, encoding="utf-8")

    recommendation_columns = [
        column
        for column in [
            "municipality_code",
            "municipality_name",
            "department_name",
            "cluster_label",
            "cluster_name",
            "cluster_recommendation",
            "strategic_need_score",
            "collection_gap_percentage",
            "collection_center_distance_km",
            "recyclable_kg_day",
            "estimated_uncollected_recyclable_kg_day",
            "existing_collection_centers",
            "active_eca_facility_count",
            "operation_capacity_tons",
            "municipal_multidimensional_poverty_index",
            "total_hazardous_waste_kg_latest",
        ]
        if column in working.columns
    ]
    working[recommendation_columns].sort_values(
        "strategic_need_score",
        ascending=False,
    ).head(100).to_csv(
        processed_dir / "kmeans_operational_recommendations.csv",
        index=False,
        encoding="utf-8",
    )

    fig, ax = plt.subplots(figsize=(8.4, 4.8))
    ax.plot(k_values, inertias, color=CYAN, linewidth=2.4, marker="o", markersize=7)
    ax.axvline(selected_k, color=GREEN, linestyle="--", linewidth=2.1, label=f"Selected K = {selected_k}")
    _prepare_axis(ax, "K-Means Elbow Method", "Number of clusters", "Within-cluster sum of squares")
    legend = ax.legend(facecolor=PANEL_BG, edgecolor=GRID_COLOR)
    for text in legend.get_texts():
        text.set_color(MUTED_TEXT_COLOR)
    elbow_chart = _save_plot(fig, static_generated_dir, "kmeans_elbow_method.png")

    fig, ax = plt.subplots(figsize=(8.6, 4.9))
    _prepare_axis(ax, "K-Means Validation Metrics", "Number of clusters", "Silhouette Score")
    ax.plot(k_values, silhouette_values, color=GREEN, marker="o", linewidth=2.2, label="Silhouette Score")
    ax.set_ylabel("Silhouette Score", color=GREEN, labelpad=10)
    ax.tick_params(axis="y", colors=GREEN)
    ax2 = ax.twinx()
    ax2.plot(
        k_values,
        davies_bouldin_values,
        color=AMBER,
        marker="s",
        linewidth=2.2,
        label="Davies-Bouldin Index",
    )
    ax2.set_ylabel("Davies-Bouldin Index", color=AMBER, labelpad=10)
    ax2.tick_params(axis="y", colors=AMBER)
    for spine in ax2.spines.values():
        spine.set_color(GRID_COLOR)
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    legend = ax.legend(lines + lines2, labels + labels2, facecolor=PANEL_BG, edgecolor=GRID_COLOR)
    for text in legend.get_texts():
        text.set_color(MUTED_TEXT_COLOR)
    validation_chart = _save_plot(fig, static_generated_dir, "kmeans_validation_metrics.png")

    fig, ax = plt.subplots(figsize=(8.6, 5.2))
    for index, (cluster_id, group) in enumerate(working.groupby("cluster_id")):
        color = CLUSTER_COLORS[index % len(CLUSTER_COLORS)]
        ax.scatter(
            group["demand_pressure_score"],
            group["service_gap_score"],
            s=34,
            alpha=0.72,
            color=color,
            edgecolors=CHART_BG,
            linewidths=0.25,
            label=f"Cluster {int(cluster_id)}",
        )
        ax.scatter(
            group["demand_pressure_score"].mean(),
            group["service_gap_score"].mean(),
            s=190,
            marker="X",
            color=color,
            edgecolors=TEXT_COLOR,
            linewidths=1.2,
        )
    _prepare_axis(
        ax,
        "Municipality Clusters by Demand and Service Gap",
        "Demand and growth pressure score",
        "Service gap and infrastructure pressure score",
    )
    legend = ax.legend(title="K-Means cluster", facecolor=PANEL_BG, edgecolor=GRID_COLOR, ncol=2)
    legend.get_title().set_color(TEXT_COLOR)
    for text in legend.get_texts():
        text.set_color(MUTED_TEXT_COLOR)
    cluster_chart = _save_plot(fig, static_generated_dir, "kmeans_cluster_scatter.png")

    fig, ax = plt.subplots(figsize=(12, max(4.8, selected_k * 0.82 + 2.6)))
    heatmap_values = ranked_centers.values
    image = ax.imshow(heatmap_values, cmap="viridis", aspect="auto", vmin=-2.2, vmax=2.2)
    ax.set_xticks(range(len(selected_features)))
    ax.set_yticks(range(len(ranked_centers.index)))
    ax.set_xticklabels([_friendly(column, friendly_labels) for column in selected_features], rotation=45, ha="right")
    ax.set_yticklabels(ranked_centers.index)
    _prepare_axis(ax, "Standardized K-Means Centroid Profiles")
    ax.grid(False)
    colorbar = fig.colorbar(image, ax=ax, fraction=0.035, pad=0.03)
    colorbar.set_label("Standard score", color=MUTED_TEXT_COLOR)
    colorbar.ax.yaxis.set_tick_params(color=MUTED_TEXT_COLOR)
    plt.setp(colorbar.ax.get_yticklabels(), color=MUTED_TEXT_COLOR)
    centroid_chart = _save_plot(fig, static_generated_dir, "kmeans_centroid_profiles.png")

    if "department_name" in working.columns:
        department_rows = []
        for department_name, group in working.groupby("department_name"):
            counts = group["cluster_label"].value_counts()
            dominant_cluster = counts.index[0]
            department_rows.append(
                {
                    "department_name": department_name,
                    "municipalities": int(group.shape[0]),
                    "dominant_cluster": dominant_cluster,
                    "dominant_cluster_share_pct": round(float(counts.iloc[0] / group.shape[0] * 100), 2),
                    "average_strategic_need_score": round(float(group["strategic_need_score"].mean()), 3),
                }
            )
        geographic_summary = (
            pd.DataFrame(department_rows)
            .sort_values("average_strategic_need_score", ascending=False)
            .head(12)
        )
        top_departments = geographic_summary["department_name"].tolist()
        department_distribution = pd.crosstab(
            working.loc[working["department_name"].isin(top_departments), "department_name"],
            working.loc[working["department_name"].isin(top_departments), "cluster_label"],
        ).reindex(top_departments)
        ordered_cluster_columns = [f"Cluster {cluster_id}" for cluster_id in range(1, selected_k + 1)]
        department_distribution = department_distribution.reindex(columns=ordered_cluster_columns, fill_value=0)

        fig, ax = plt.subplots(figsize=(9.4, 5.6))
        left = np.zeros(len(department_distribution))
        y_positions = np.arange(len(department_distribution))
        for index, cluster_column in enumerate(department_distribution.columns):
            values = department_distribution[cluster_column].to_numpy()
            ax.barh(
                y_positions,
                values,
                left=left,
                color=CLUSTER_COLORS[index % len(CLUSTER_COLORS)],
                edgecolor=CHART_BG,
                label=cluster_column,
            )
            left += values
        ax.set_yticks(y_positions)
        ax.set_yticklabels(department_distribution.index)
        ax.invert_yaxis()
        _prepare_axis(
            ax,
            "Department-Level K-Means Cluster Distribution",
            "Municipality count",
            "",
        )
        legend = ax.legend(title="Dominant profile", facecolor=PANEL_BG, edgecolor=GRID_COLOR, ncol=2)
        legend.get_title().set_color(TEXT_COLOR)
        for text in legend.get_texts():
            text.set_color(MUTED_TEXT_COLOR)
        geography_chart = _save_plot(fig, static_generated_dir, "kmeans_department_distribution.png")
    else:
        geographic_summary = pd.DataFrame()
        geography_chart = ""

    elbow_table = pd.DataFrame(
        {
            "K": k_values,
            "Inertia": inertias,
            "Silhouette Score": silhouette_values,
            "Davies-Bouldin Index": davies_bouldin_values,
        }
    )
    selected_feature_rows = []
    for item in KMEANS_FEATURES:
        column = item["column"]
        if column not in selected_features:
            continue
        selected_feature_rows.append(
            {
                "feature": _friendly(column, friendly_labels),
                "domain": item["domain"],
                "reason": item["reason"],
                "missing_values_imputed": int(missing_counts[column]),
                "transformation": "Median imputation, logarithmic compression, StandardScaler"
                if column in transformed_columns
                else "Median imputation, StandardScaler",
            }
        )

    top_municipalities = (
        working.sort_values("strategic_need_score", ascending=False)
        .head(15)
        [
            [
                column
                for column in [
                    "municipality_name",
                    "department_name",
                    "cluster_label",
                    "cluster_name",
                    "strategic_need_score",
                    "collection_gap_percentage",
                    "collection_center_distance_km",
                    "recyclable_kg_day",
                    "existing_collection_centers",
                    "total_hazardous_waste_kg_latest",
                ]
                if column in working.columns
            ]
        ]
    )

    operational_recommendations = []
    for row in cluster_summary.to_dict("records"):
        cluster_id = int(row["cluster_id"])
        group = working[working["cluster_id"].eq(cluster_id)].sort_values(
            "strategic_need_score",
            ascending=False,
        )
        example_names = ", ".join(group["municipality_name"].head(4).astype(str).tolist())
        if cluster_id == 1:
            investment_focus = "Prioritize feasibility studies for new recycling centers and immediate service expansion."
            policy_use = "Use this cluster to justify high-priority capital allocation and equity-oriented intervention."
        elif cluster_id == 2:
            investment_focus = "Reinforce existing networks with satellite collection points and additional operating capacity."
            policy_use = "Use this cluster for medium-term infrastructure budgeting and growth-driven coverage planning."
        elif cluster_id == 3:
            investment_focus = "Target selective route optimization, hazardous pressure review, and periodic field validation."
            policy_use = "Use this cluster to coordinate environmental monitoring with service quality controls."
        else:
            investment_focus = "Maintain service levels, monitor growth, and redirect major investment to higher-pressure clusters."
            policy_use = "Use this cluster as a baseline group for efficiency benchmarking and preventive maintenance."
        operational_recommendations.append(
            {
                "cluster_label": row["cluster_label"],
                "cluster_name": row["cluster_name"],
                "investment_focus": investment_focus,
                "policy_use": policy_use,
                "sustainability_implication": (
                    "The recommendation supports recyclable recovery, service accessibility, and environmental risk reduction."
                ),
                "example_municipalities": example_names,
            }
        )

    preprocessing_steps = [
        "Selected numerical features connected to population density, waste generation, infrastructure coverage, poverty, urban growth, and environmental pressure.",
        "Converted selected fields to numeric values and imputed missing values with feature medians to preserve all municipality records.",
        "Applied logarithmic compression to highly skewed population, waste, capacity, facility, and hazardous waste variables.",
        "Applied StandardScaler so K-Means compares municipalities on standardized feature space rather than raw units.",
        "Ran the elbow method from K=2 through K=8 and selected the K with the strongest distance from the inertia trend line.",
        "Fitted K-Means with a fixed random state and exported cluster assignments, scaled features, and centroid profiles.",
    ]

    evaluation_metrics = [
        {
            "metric": "Silhouette Score",
            "value": round(selected_silhouette, 4),
            "direction": "Higher is better; values near 1 indicate clearer separation.",
            "meaning": "Compares average distance inside each cluster with distance to the nearest neighboring cluster.",
            "validation_use": "Validates whether municipalities are more similar to their assigned cluster than to other clusters.",
        },
        {
            "metric": "Davies-Bouldin Index",
            "value": round(selected_davies_bouldin, 4),
            "direction": "Lower is better; lower values indicate compact and separated clusters.",
            "meaning": "Measures the average similarity between each cluster and its most similar neighboring cluster.",
            "validation_use": "Checks whether the discovered planning profiles are sufficiently distinct.",
        },
        {
            "metric": "Inertia",
            "value": round(selected_inertia, 4),
            "direction": "Lower is better for a fixed K, but it naturally decreases as K increases.",
            "meaning": "Sum of squared distances from each municipality to its assigned centroid.",
            "validation_use": "Supports elbow-method analysis by showing how compactness improves as more clusters are added.",
        },
        {
            "metric": "WCSS",
            "value": round(selected_inertia, 4),
            "direction": "Lower values indicate tighter clusters; interpretation must be balanced with model simplicity.",
            "meaning": "Within-cluster sum of squares; in scikit-learn K-Means this is the same objective reported as inertia.",
            "validation_use": "Explains the clustering objective optimized by K-Means and why the elbow curve matters.",
        },
    ]

    return {
        "algorithm": "K-Means clustering",
        "records_used": int(len(working)),
        "selected_k": int(selected_k),
        "k_range_tested": f"{min(k_values)} to {max(k_values)}",
        "k_selection_reason": (
            f"The selected value K={selected_k} is the strongest elbow point in the inertia curve. "
            "It balances compact clusters with interpretability for municipal recycling planning."
        ),
        "features_used_count": int(len(selected_features)),
        "selected_features": selected_feature_rows,
        "preprocessing_steps": preprocessing_steps,
        "evaluation_metrics": evaluation_metrics,
        "cluster_summary": _records(cluster_summary),
        "centroid_table": _records(centroid_table),
        "elbow_table": _records(elbow_table),
        "geographic_summary": _records(geographic_summary) if not geographic_summary.empty else [],
        "operational_recommendations": operational_recommendations,
        "top_priority_municipalities": _records(top_municipalities),
        "charts": {
            "kmeans_elbow": elbow_chart,
            "kmeans_validation": validation_chart,
            "kmeans_clusters": cluster_chart,
            "kmeans_centroids": centroid_chart,
            "kmeans_geography": geography_chart,
        },
        "generated_files": [
            "kmeans_clustered_municipalities.csv",
            "kmeans_operational_recommendations.csv",
            "kmeans_centroid_profiles.csv",
            "kmeans_scaled_feature_matrix.csv",
        ],
        "download_files": [
            {
                "label": "Cluster results CSV",
                "filename": "kmeans_clustered_municipalities.csv",
                "description": "Municipality-level K-Means cluster assignments and planning scores.",
            },
            {
                "label": "Operational recommendations CSV",
                "filename": "kmeans_operational_recommendations.csv",
                "description": "Top-ranked municipalities for practical recycling center planning.",
            },
            {
                "label": "Scaled K-Means matrix CSV",
                "filename": "kmeans_scaled_feature_matrix.csv",
                "description": "Standardized feature matrix used by the clustering model.",
            },
            {
                "label": "Integrated dataset CSV",
                "filename": "smartrecycleai_integrated_dataset.csv",
                "description": "Full processed municipal dataset used by the analytics platform.",
            },
            {
                "label": "Model feature matrix CSV",
                "filename": "model_feature_matrix.csv",
                "description": "Model-ready engineered features for downstream experiments.",
            },
        ],
    }

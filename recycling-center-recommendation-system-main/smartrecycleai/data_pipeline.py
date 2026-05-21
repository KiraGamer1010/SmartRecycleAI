from __future__ import annotations

import json
import math
import re
import unicodedata
from functools import lru_cache
from importlib import import_module
from pathlib import Path
from typing import Any

from .ml_pipeline import run_kmeans_analysis


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASETS_DIR = PROJECT_ROOT / "datasets"
PROCESSED_DIR = DATASETS_DIR / "processed"
STATIC_GENERATED_DIR = PROJECT_ROOT / "static" / "generated"
REPORTS_DIR = PROJECT_ROOT / "reports"
DATASET_PROFILE_FILE = REPORTS_DIR / "dataset_profile.json"
DASHBOARD_CONTEXT_FILE = REPORTS_DIR / "dashboard_context.json"


class LazyModule:
    def __init__(self, module_name: str):
        self.module_name = module_name
        self._module = None

    def _load(self):
        if self._module is None:
            if self.module_name == "matplotlib.pyplot":
                matplotlib = import_module("matplotlib")
                matplotlib.use("Agg")
            self._module = import_module(self.module_name)
        return self._module

    def __getattr__(self, name: str):
        return getattr(self._load(), name)


pd = LazyModule("pandas")
np = LazyModule("numpy")
plt = LazyModule("matplotlib.pyplot")

FINAL_DATASET_FILE = DATASETS_DIR / "dataset_final.csv"
ECA_FILE = DATASETS_DIR / "Superservicios_ECA.csv"
HAZARDOUS_WASTE_FILE = DATASETS_DIR / "Residuos_peligrosos_por_municipio_20260515.csv"
CNPV_FILE = DATASETS_DIR / "CNPV-2018-VIHOPE-v2.xls"
DEPARTMENT_POPULATION_FILE = DATASETS_DIR / "PPED-AreaDep-2018-2050_VP.xlsx"
BOGOTA_HOUSEHOLDS_FILE = (
    DATASETS_DIR
    / "anexo-proyecciones-bogota-hogares-desagreacion-loc-2018-2035-UPZ-2018-2024.xlsx"
)

FINAL_COLUMNS = [
    "municipality_code",
    "municipality_name",
    "department_code",
    "total_population",
    "urban_population",
    "rural_population",
    "urban_percentage",
    "area_km2",
    "population_density_per_km2",
    "municipal_multidimensional_poverty_index",
    "overcrowding_deprivation_percentage",
    "water_deprivation_percentage",
    "health_deprivation_percentage",
    "informal_work_percentage",
    "waste_kg_per_capita_day",
    "waste_kg_day",
    "waste_ton_day",
    "recyclable_percentage",
    "recyclable_kg_day",
    "collection_coverage_percentage",
    "collection_center_distance_km",
    "existing_collection_centers",
    "road_access_score",
    "needs_collection_center",
    "recycling_potential_kg_month",
    "priority_label",
]

PRIORITY_CLASS_LABELS = {
    0: "Not priority",
    1: "Priority",
    2: "High priority",
}

MODEL_FEATURE_COLUMNS = [
    "total_population",
    "urbanization_ratio",
    "population_density_per_km2",
    "municipal_multidimensional_poverty_index",
    "water_deprivation_percentage",
    "waste_kg_per_capita_day",
    "recyclable_kg_day",
    "collection_coverage_percentage",
    "collection_gap_percentage",
    "collection_center_distance_km",
    "existing_collection_centers",
    "road_access_score",
    "estimated_uncollected_recyclable_kg_day",
    "center_capacity_pressure_score",
    "eca_facility_count",
    "active_eca_facility_count",
    "operation_capacity_tons",
    "storage_capacity_tons",
    "total_hazardous_waste_kg_latest",
    "department_population_growth_2018_2030_pct",
]

FRIENDLY_LABELS = {
    "total_population": "Total population",
    "urbanization_ratio": "Urbanization ratio",
    "population_density_per_km2": "Population density",
    "municipal_multidimensional_poverty_index": "Poverty index",
    "water_deprivation_percentage": "Water deprivation",
    "waste_kg_per_capita_day": "Waste per capita",
    "recyclable_kg_day": "Recyclable waste per day",
    "collection_coverage_percentage": "Collection coverage",
    "collection_gap_percentage": "Collection gap",
    "collection_center_distance_km": "Distance to center",
    "existing_collection_centers": "Existing centers",
    "road_access_score": "Road access score",
    "estimated_uncollected_recyclable_kg_day": "Uncollected recyclable waste",
    "center_capacity_pressure_score": "Center pressure",
    "eca_facility_count": "Registered facilities",
    "active_eca_facility_count": "Active facilities",
    "operation_capacity_tons": "Operation capacity",
    "storage_capacity_tons": "Storage capacity",
    "total_hazardous_waste_kg_latest": "Latest hazardous waste",
    "department_population_growth_2018_2030_pct": "Department growth",
    "priority_class_id": "Priority class",
    "recycling_potential_kg_month": "Monthly recycling potential",
}


def ensure_directories() -> None:
    for path in (PROCESSED_DIR, STATIC_GENERATED_DIR, REPORTS_DIR):
        path.mkdir(parents=True, exist_ok=True)


def normalize_key(value: Any) -> str:
    if pd.isna(value):
        return ""
    text = str(value).strip()
    text = unicodedata.normalize("NFKD", text)
    text = "".join(char for char in text if not unicodedata.combining(char))
    text = text.upper()
    text = re.sub(r"[^A-Z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def parse_locale_number(value: Any) -> float:
    if pd.isna(value):
        return np.nan
    text = str(value).strip()
    if not text:
        return np.nan

    normalized = normalize_key(text)
    if normalized in {"NO REPORTA", "SIN INFORMACION", "NAN", "NONE", "NULL"}:
        return np.nan

    text = text.replace(" ", "")
    if "," in text:
        text = text.replace(".", "").replace(",", ".")
    elif re.fullmatch(r"-?\d{1,3}(\.\d{3})+", text):
        text = text.replace(".", "")

    try:
        return float(text)
    except ValueError:
        return np.nan


def _safe_ratio(numerator: pd.Series, denominator: pd.Series) -> pd.Series:
    denominator = denominator.replace({0: np.nan})
    return (numerator / denominator).replace([np.inf, -np.inf], np.nan)


def _format_code(value: Any, width: int) -> str:
    if pd.isna(value):
        return ""
    text = str(value).strip().replace(".0", "")
    digits = re.sub(r"\D", "", text)
    if not digits:
        return ""
    return digits.zfill(width)


def _read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, sep=None, engine="python", encoding="utf-8-sig")


def _write_csv(df: pd.DataFrame, filename: str) -> Path:
    ensure_directories()
    output_path = PROCESSED_DIR / filename
    df.to_csv(output_path, index=False, encoding="utf-8")
    return output_path


def load_final_modeling_dataset() -> pd.DataFrame:
    df = pd.read_csv(FINAL_DATASET_FILE, encoding="utf-8-sig")
    if len(df.columns) == len(FINAL_COLUMNS):
        df.columns = FINAL_COLUMNS
    else:
        raise ValueError("The existing final dataset does not match the expected schema.")

    df["municipality_code"] = df["municipality_code"].map(lambda value: _format_code(value, 5))
    df["department_code"] = df["department_code"].map(lambda value: _format_code(value, 2))
    df["priority_class_id"] = pd.to_numeric(df["needs_collection_center"], errors="coerce")
    df["priority_label"] = df["priority_class_id"].map(PRIORITY_CLASS_LABELS).fillna("Not classified")
    df["municipality_key"] = df["municipality_name"].map(normalize_key)

    for column in df.columns:
        if column not in {
            "municipality_code",
            "department_code",
            "municipality_name",
            "priority_label",
            "municipality_key",
        }:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    df["urbanization_ratio"] = _safe_ratio(df["urban_population"], df["total_population"])
    df["rurality_ratio"] = _safe_ratio(df["rural_population"], df["total_population"])
    df["collection_gap_percentage"] = (100 - df["collection_coverage_percentage"]).clip(lower=0, upper=100)
    df["estimated_uncollected_recyclable_kg_day"] = (
        df["recyclable_kg_day"] * df["collection_gap_percentage"] / 100
    )
    df["center_capacity_pressure_score"] = _safe_ratio(
        df["recyclable_kg_day"], df["existing_collection_centers"] + 1
    )
    df["access_need_score"] = (
        df["collection_center_distance_km"]
        + df["collection_gap_percentage"] / 10
        + df["municipal_multidimensional_poverty_index"] / 10
        - df["road_access_score"]
    )
    return df


def clean_eca_data() -> pd.DataFrame:
    raw = _read_csv(ECA_FILE)
    frame = pd.DataFrame(
        {
            "company_id": raw.iloc[:, 0],
            "company_name": raw.iloc[:, 1],
            "facility_id": raw.iloc[:, 2],
            "department_name": raw.iloc[:, 3],
            "municipality_name": raw.iloc[:, 4],
            "facility_name": raw.iloc[:, 5],
            "operation_start_date": pd.to_datetime(raw.iloc[:, 6], errors="coerce"),
            "operation_capacity_tons": raw.iloc[:, 8].map(parse_locale_number),
            "storage_capacity_tons": raw.iloc[:, 9].map(parse_locale_number),
            "storage_capacity_m3": raw.iloc[:, 10].map(parse_locale_number),
            "soil_compatible": raw.iloc[:, 11].map(normalize_key).eq("SI"),
            "environmental_authorization": raw.iloc[:, 12].map(normalize_key).eq("SI"),
            "facility_status": raw.iloc[:, 13].map(normalize_key),
        }
    )
    frame["department_key"] = frame["department_name"].map(normalize_key)
    frame["municipality_key"] = frame["municipality_name"].map(normalize_key)
    frame["is_active"] = frame["facility_status"].eq("EN OPERACION")

    grouped = (
        frame.groupby(["department_key", "municipality_key"], dropna=False)
        .agg(
            department_name=("department_name", "first"),
            municipality_name=("municipality_name", "first"),
            eca_facility_count=("facility_id", "size"),
            active_eca_facility_count=("is_active", "sum"),
            authorized_eca_facility_count=("environmental_authorization", "sum"),
            soil_compatible_facility_count=("soil_compatible", "sum"),
            operation_capacity_tons=("operation_capacity_tons", "sum"),
            storage_capacity_tons=("storage_capacity_tons", "sum"),
            storage_capacity_m3=("storage_capacity_m3", "sum"),
            missing_operation_capacity_count=("operation_capacity_tons", lambda value: int(value.isna().sum())),
            missing_storage_capacity_count=("storage_capacity_tons", lambda value: int(value.isna().sum())),
        )
        .reset_index()
    )

    _write_csv(frame, "eca_records_clean.csv")
    _write_csv(grouped, "eca_municipality_summary.csv")
    return grouped


def clean_hazardous_waste_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    raw = _read_csv(HAZARDOUS_WASTE_FILE)
    frame = pd.DataFrame(
        {
            "year": pd.to_numeric(raw.iloc[:, 0], errors="coerce").astype("Int64"),
            "municipality_name": raw.iloc[:, 1],
            "solid_or_semisolid_kg": raw.iloc[:, 2].map(parse_locale_number),
            "liquid_kg": raw.iloc[:, 3].map(parse_locale_number),
            "gaseous_kg": raw.iloc[:, 4].map(parse_locale_number),
        }
    )
    frame["municipality_key"] = frame["municipality_name"].map(normalize_key)
    frame["total_hazardous_waste_kg"] = frame[
        ["solid_or_semisolid_kg", "liquid_kg", "gaseous_kg"]
    ].sum(axis=1, min_count=1)

    latest = (
        frame.dropna(subset=["year"])
        .sort_values(["municipality_key", "year"])
        .groupby("municipality_key")
        .tail(1)[["municipality_key", "year", "total_hazardous_waste_kg"]]
        .rename(
            columns={
                "year": "latest_hazardous_waste_year",
                "total_hazardous_waste_kg": "total_hazardous_waste_kg_latest",
            }
        )
    )
    summary = (
        frame.groupby("municipality_key")
        .agg(
            municipality_name=("municipality_name", "first"),
            hazardous_waste_record_count=("year", "size"),
            total_hazardous_waste_kg_all_years=("total_hazardous_waste_kg", "sum"),
            average_annual_hazardous_waste_kg=("total_hazardous_waste_kg", "mean"),
        )
        .reset_index()
        .merge(latest, on="municipality_key", how="left")
    )

    _write_csv(frame, "hazardous_waste_clean.csv")
    _write_csv(summary, "hazardous_waste_municipality_summary.csv")
    return frame, summary


def clean_census_data() -> pd.DataFrame:
    housing = pd.read_excel(CNPV_FILE, sheet_name=1, header=8)
    housing.columns = [
        "municipality_code",
        "department_name",
        "census_municipality_name",
        "housing_absent_units",
        "housing_temporary_units",
        "housing_vacant_units",
        "housing_occupied_units",
        "census_housing_units_2018",
        "census_households_2018",
        "census_population_housing_sheet",
    ]

    population = pd.read_excel(CNPV_FILE, sheet_name=2, header=8)
    population.columns = [
        "municipality_code",
        "department_name",
        "census_municipality_name",
        "private_household_population_2018",
        "special_accommodation_population_2018",
        "census_total_population_2018",
    ]

    for frame in (housing, population):
        frame["municipality_code"] = frame["municipality_code"].map(lambda value: _format_code(value, 5))
        frame.dropna(subset=["municipality_code"], inplace=True)
        frame.drop(frame[~frame["municipality_code"].str.fullmatch(r"\d{5}")].index, inplace=True)
        frame["department_code"] = frame["municipality_code"].str[:2]
        frame["department_key"] = frame["department_name"].map(normalize_key)
        frame["municipality_key"] = frame["census_municipality_name"].map(normalize_key)

    numeric_columns = [column for column in housing.columns if column.endswith("_2018") or column.endswith("_sheet")]
    for column in numeric_columns:
        housing[column] = pd.to_numeric(housing[column], errors="coerce")
    for column in [
        "private_household_population_2018",
        "special_accommodation_population_2018",
        "census_total_population_2018",
    ]:
        population[column] = pd.to_numeric(population[column], errors="coerce")

    census = housing.merge(
        population[
            [
                "municipality_code",
                "private_household_population_2018",
                "special_accommodation_population_2018",
                "census_total_population_2018",
            ]
        ],
        on="municipality_code",
        how="left",
    )
    census["households_per_housing_unit"] = _safe_ratio(
        census["census_households_2018"], census["census_housing_units_2018"]
    )
    _write_csv(census, "cnpv_2018_municipality_clean.csv")
    return census


def clean_department_population_projections() -> tuple[pd.DataFrame, pd.DataFrame]:
    frame = pd.read_excel(DEPARTMENT_POPULATION_FILE, sheet_name=0, header=7)
    frame = frame.iloc[:, :5]
    frame.columns = [
        "department_code",
        "department_name",
        "year",
        "geographic_area",
        "projected_population",
    ]
    frame["department_code"] = frame["department_code"].map(lambda value: _format_code(value, 2))
    frame["year"] = pd.to_numeric(frame["year"], errors="coerce")
    frame["projected_population"] = pd.to_numeric(frame["projected_population"], errors="coerce")
    frame["geographic_area_key"] = frame["geographic_area"].map(normalize_key)
    frame["department_key"] = frame["department_name"].map(normalize_key)
    frame = frame.dropna(subset=["year", "projected_population"])
    frame["year"] = frame["year"].astype(int)

    total = frame[frame["geographic_area_key"].eq("TOTAL")].copy()
    wide = total.pivot_table(
        index=["department_code", "department_name", "department_key"],
        columns="year",
        values="projected_population",
        aggfunc="first",
    ).reset_index()

    summary = wide[["department_code", "department_name", "department_key"]].copy()
    for year in [2018, 2026, 2030, 2050]:
        if year in wide.columns:
            summary[f"department_population_{year}"] = wide[year]
    if {2018, 2030}.issubset(wide.columns):
        summary["department_population_growth_2018_2030_pct"] = (
            (wide[2030] - wide[2018]) / wide[2018] * 100
        )

    _write_csv(frame, "department_population_projection_clean.csv")
    _write_csv(summary, "department_population_projection_summary.csv")
    return frame, summary


def clean_bogota_household_projections() -> tuple[pd.DataFrame, pd.DataFrame, dict[str, float]]:
    locality = pd.read_excel(BOGOTA_HOUSEHOLDS_FILE, sheet_name=0, header=8)
    locality = locality.rename(
        columns={
            locality.columns[0]: "area_type",
            locality.columns[1]: "locality_name",
            locality.columns[2]: "locality_code",
        }
    )
    locality_long = locality.melt(
        id_vars=["area_type", "locality_name", "locality_code"],
        var_name="year",
        value_name="projected_households",
    )
    locality_long["year"] = pd.to_numeric(locality_long["year"], errors="coerce")
    locality_long["projected_households"] = pd.to_numeric(
        locality_long["projected_households"], errors="coerce"
    )
    locality_long = locality_long.dropna(subset=["year", "projected_households"])
    locality_long["year"] = locality_long["year"].astype(int)
    locality_long["locality_key"] = locality_long["locality_name"].map(normalize_key)

    upz = pd.read_excel(BOGOTA_HOUSEHOLDS_FILE, sheet_name=1, header=8)
    upz = upz.rename(
        columns={
            upz.columns[0]: "planning_zone_name",
            upz.columns[1]: "planning_zone_code",
            upz.columns[2]: "locality_code",
        }
    )
    upz_long = upz.melt(
        id_vars=["planning_zone_name", "planning_zone_code", "locality_code"],
        var_name="year",
        value_name="projected_households",
    )
    upz_long["year"] = pd.to_numeric(upz_long["year"], errors="coerce")
    upz_long["projected_households"] = pd.to_numeric(upz_long["projected_households"], errors="coerce")
    upz_long = upz_long.dropna(subset=["year", "projected_households"])
    upz_long["year"] = upz_long["year"].astype(int)
    upz_long["planning_zone_key"] = upz_long["planning_zone_name"].map(normalize_key)

    official_locality_rows = locality_long.dropna(subset=["locality_code"]).copy()
    totals = (
        official_locality_rows.groupby("year")["projected_households"]
        .sum()
        .rename("projected_households")
    )
    summary = {
        "bogota_households_2024": float(totals.get(2024, np.nan)),
        "bogota_households_2035": float(totals.get(2035, np.nan)),
    }
    if not math.isnan(summary["bogota_households_2024"]) and not math.isnan(
        summary["bogota_households_2035"]
    ):
        summary["bogota_household_growth_2024_2035_pct"] = (
            (summary["bogota_households_2035"] - summary["bogota_households_2024"])
            / summary["bogota_households_2024"]
            * 100
        )
    else:
        summary["bogota_household_growth_2024_2035_pct"] = np.nan

    _write_csv(locality_long, "bogota_household_locality_projection_clean.csv")
    _write_csv(upz_long, "bogota_household_planning_zone_projection_clean.csv")
    return locality_long, upz_long, summary


def build_integrated_dataset() -> tuple[pd.DataFrame, pd.DataFrame]:
    base = load_final_modeling_dataset()
    eca = clean_eca_data()
    _, hazardous_summary = clean_hazardous_waste_data()
    census = clean_census_data()
    _, department_summary = clean_department_population_projections()
    _, _, bogota_summary = clean_bogota_household_projections()

    census_merge = census[
        [
            "municipality_code",
            "department_name",
            "department_key",
            "census_municipality_name",
            "census_housing_units_2018",
            "census_households_2018",
            "census_total_population_2018",
            "households_per_housing_unit",
        ]
    ].copy()

    integrated = base.merge(census_merge, on="municipality_code", how="left")
    integrated = integrated.merge(
        department_summary.drop(columns=["department_name", "department_key"], errors="ignore"),
        on="department_code",
        how="left",
    )
    integrated = integrated.merge(
        eca.drop(columns=["department_name", "municipality_name"], errors="ignore"),
        on=["department_key", "municipality_key"],
        how="left",
    )

    antioquia_map = base.loc[
        base["department_code"].eq("05"), ["municipality_code", "municipality_key"]
    ].drop_duplicates()
    hazardous_join = hazardous_summary.merge(antioquia_map, on="municipality_key", how="inner")
    integrated = integrated.merge(
        hazardous_join.drop(columns=["municipality_name", "municipality_key"], errors="ignore"),
        on="municipality_code",
        how="left",
    )

    count_columns = [
        "eca_facility_count",
        "active_eca_facility_count",
        "authorized_eca_facility_count",
        "soil_compatible_facility_count",
        "hazardous_waste_record_count",
    ]
    amount_columns = [
        "operation_capacity_tons",
        "storage_capacity_tons",
        "storage_capacity_m3",
        "total_hazardous_waste_kg_all_years",
        "average_annual_hazardous_waste_kg",
        "total_hazardous_waste_kg_latest",
    ]
    for column in count_columns + amount_columns:
        if column in integrated.columns:
            integrated[column] = integrated[column].fillna(0)

    integrated["has_registered_eca"] = (integrated["eca_facility_count"] > 0).astype(int)
    integrated["has_hazardous_waste_records"] = (
        integrated["hazardous_waste_record_count"] > 0
    ).astype(int)

    for key, value in bogota_summary.items():
        integrated[key] = np.nan
        integrated.loc[integrated["municipality_code"].eq("11001"), key] = value

    available_features = [column for column in MODEL_FEATURE_COLUMNS if column in integrated.columns]
    for column in available_features:
        values = pd.to_numeric(integrated[column], errors="coerce")
        mean = values.mean()
        std = values.std(ddof=0)
        if not std or pd.isna(std):
            integrated[f"scaled_{column}"] = 0
        else:
            integrated[f"scaled_{column}"] = (values - mean) / std

    feature_matrix_columns = (
        ["municipality_code", "municipality_name", "department_code"]
        + available_features
        + [f"scaled_{column}" for column in available_features]
        + ["priority_class_id", "priority_label", "needs_collection_center"]
    )
    feature_matrix = integrated[feature_matrix_columns].copy()

    _write_csv(integrated, "smartrecycleai_integrated_dataset.csv")
    _write_csv(feature_matrix, "model_feature_matrix.csv")
    return integrated, feature_matrix


def profile_dataframe(name: str, df: pd.DataFrame) -> dict[str, Any]:
    numeric_count = int(df.select_dtypes(include=np.number).shape[1])
    categorical_count = int(df.shape[1] - numeric_count)
    missing_cells = int(df.isna().sum().sum())
    total_cells = int(df.shape[0] * df.shape[1]) if df.shape[0] and df.shape[1] else 0
    missing_rate = (missing_cells / total_cells * 100) if total_cells else 0
    return {
        "name": name,
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "numeric_variables": numeric_count,
        "categorical_variables": categorical_count,
        "missing_cells": missing_cells,
        "missing_rate": round(missing_rate, 2),
        "duplicate_rows": int(df.duplicated().sum()),
    }


def _round_value(value: Any) -> Any:
    if pd.isna(value):
        return ""
    if isinstance(value, (float, np.floating)):
        return round(float(value), 3)
    if isinstance(value, (int, np.integer)):
        return int(value)
    return value


def dataframe_records(df: pd.DataFrame, limit: int = 10) -> list[dict[str, Any]]:
    return [
        {column: _round_value(value) for column, value in row.items()}
        for row in df.head(limit).to_dict(orient="records")
    ]


def build_dataset_catalog(data: dict[str, pd.DataFrame]) -> list[dict[str, Any]]:
    catalog = [
        {
            "file": "Municipal recommendation dataset CSV",
            "display_name": "Municipal modeling dataset",
            "source": "Existing municipal modeling dataset in the project repository.",
            "role": "Base supervised learning table with target labels, accessibility variables, waste indicators, and social vulnerability features.",
            "contribution": "Defines the recommendation target and provides one row per municipality for model-oriented preparation.",
            "quality_notes": "Complete table with no missing values; population scale must be compared with official census values before interpretation.",
            "profile": profile_dataframe("Modeling dataset", data["base"]),
        },
        {
            "file": "Recycling facility registry CSV",
            "display_name": "Recycling facility registry",
            "source": "Recycling collection and classification facility registry.",
            "role": "Operational infrastructure evidence for recycling center availability and capacity.",
            "contribution": "Adds facility counts, active facility counts, capacity, authorization, and compatibility indicators.",
            "quality_notes": "Capacity fields contain locale-specific number formats and text markers for unavailable values.",
            "profile": profile_dataframe("Recycling facility records", data["eca_records"]),
        },
        {
            "file": "Municipal hazardous waste CSV",
            "display_name": "Municipal hazardous waste records",
            "source": "Municipal hazardous waste reporting file.",
            "role": "Environmental pressure indicator for waste management planning.",
            "contribution": "Adds latest and historical hazardous waste quantities for matching municipalities.",
            "quality_notes": "The file lacks a department column, so the pipeline joins it only to the Antioquia municipality subset to avoid ambiguous matches.",
            "profile": profile_dataframe("Hazardous waste records", data["hazardous_records"]),
        },
        {
            "file": "Population and housing census workbook",
            "display_name": "Population and housing census workbook",
            "source": "National population and housing census workbook.",
            "role": "Official reference for population, households, and housing units.",
            "contribution": "Validates municipal scale and adds census household and housing features.",
            "quality_notes": "Workbook includes national and department totals plus footer notes; the pipeline keeps only five-digit municipal codes.",
            "profile": profile_dataframe("Census municipality records", data["census"]),
        },
        {
            "file": "Department population projection workbook",
            "display_name": "Department population projection workbook",
            "source": "Department population projections for 2018 through 2050.",
            "role": "Forward-looking demographic pressure signal.",
            "contribution": "Adds department-level projected population and growth features for long-term planning.",
            "quality_notes": "The workbook includes multiple geographic areas; the model feature pipeline uses total department projections.",
            "profile": profile_dataframe("Department projection records", data["department_projection"]),
        },
        {
            "file": "Capital household projection workbook",
            "display_name": "Capital household projection workbook",
            "source": "Capital household projections by locality and planning zone.",
            "role": "High-resolution urban household growth context.",
            "contribution": "Supports local analysis for the capital and adds city household growth features to the capital municipality row.",
            "quality_notes": "The workbook has different year horizons by sheet; locality data supports 2018-2035, while planning-zone data supports 2018-2024.",
            "profile": profile_dataframe("Capital locality projections", data["bogota_locality"]),
        },
    ]
    return catalog


def build_statistical_summary(df: pd.DataFrame) -> list[dict[str, Any]]:
    selected = [
        "total_population",
        "population_density_per_km2",
        "municipal_multidimensional_poverty_index",
        "waste_kg_per_capita_day",
        "recyclable_kg_day",
        "collection_coverage_percentage",
        "collection_center_distance_km",
        "eca_facility_count",
        "operation_capacity_tons",
        "total_hazardous_waste_kg_latest",
    ]
    available = [column for column in selected if column in df.columns]
    summary = df[available].describe().T.reset_index().rename(columns={"index": "feature"})
    summary["feature"] = summary["feature"].map(lambda column: FRIENDLY_LABELS.get(column, column))
    return dataframe_records(summary[["feature", "mean", "std", "min", "50%", "max"]], limit=len(summary))


CHART_BG = "#0b1716"
PANEL_BG = "#10211f"
GRID_COLOR = "#27413d"
TEXT_COLOR = "#e7fff7"
MUTED_TEXT_COLOR = "#9db9b3"
GREEN = "#31d17b"
CYAN = "#35d5ff"
BLUE = "#4c83ff"
AMBER = "#d9c768"
SLATE = "#93a5a2"


def _prepare_chart_axis(ax, title: str, xlabel: str = "", ylabel: str = ""):
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


def _add_value_labels(ax, orientation: str = "vertical"):
    for patch in ax.patches:
        if orientation == "vertical":
            value = patch.get_height()
            ax.text(
                patch.get_x() + patch.get_width() / 2,
                value,
                f"{value:,.0f}",
                ha="center",
                va="bottom",
                color=TEXT_COLOR,
                fontsize=9,
                fontweight="bold",
            )
        else:
            value = patch.get_width()
            ax.text(
                value,
                patch.get_y() + patch.get_height() / 2,
                f"{value:,.0f}",
                ha="left",
                va="center",
                color=TEXT_COLOR,
                fontsize=8,
                fontweight="bold",
            )


def _save_plot(fig: plt.Figure, filename: str) -> str:
    ensure_directories()
    output = STATIC_GENERATED_DIR / filename
    fig.tight_layout()
    fig.savefig(output, dpi=160, bbox_inches="tight")
    plt.close(fig)
    return filename


def generate_charts(data: dict[str, pd.DataFrame], catalog: list[dict[str, Any]]) -> dict[str, str]:
    integrated = data["integrated"]

    charts: dict[str, str] = {}

    order = ["High priority", "Priority", "Not priority"]
    counts = integrated["priority_label"].value_counts().reindex(order).dropna()

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.bar(counts.index, counts.values, color=[GREEN, CYAN, SLATE], width=0.62)
    _prepare_chart_axis(ax, "Municipality Recommendation Priority", "Priority class", "Municipalities")
    _add_value_labels(ax)
    charts["target_distribution"] = _save_plot(fig, "target_distribution.png")

    fig, ax = plt.subplots(figsize=(8, 4.8))
    missing = pd.DataFrame(
        {
            "dataset": [item["profile"]["name"] for item in catalog],
            "missing_rate": [item["profile"]["missing_rate"] for item in catalog],
        }
    ).sort_values("missing_rate", ascending=False)
    ax.barh(missing["dataset"], missing["missing_rate"], color=CYAN)
    ax.invert_yaxis()
    _prepare_chart_axis(ax, "Missing Value Rate by Dataset", "Missing cells (%)", "")
    charts["missing_values"] = _save_plot(fig, "missing_values.png")

    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.hist(
        integrated["recycling_potential_kg_month"].dropna(),
        bins=35,
        color=GREEN,
        edgecolor=CHART_BG,
        alpha=0.86,
    )
    _prepare_chart_axis(
        ax,
        "Monthly Recycling Potential Distribution",
        "Recycling potential (kg/month)",
        "Municipality count",
    )
    charts["recycling_distribution"] = _save_plot(fig, "recycling_distribution.png")

    corr_cols = [
        "total_population",
        "population_density_per_km2",
        "municipal_multidimensional_poverty_index",
        "waste_kg_per_capita_day",
        "recyclable_kg_day",
        "collection_coverage_percentage",
        "collection_center_distance_km",
        "existing_collection_centers",
        "eca_facility_count",
        "operation_capacity_tons",
        "priority_class_id",
    ]
    corr_cols = [column for column in corr_cols if column in integrated.columns]
    corr = integrated[corr_cols].corr(numeric_only=True)
    fig, ax = plt.subplots(figsize=(9, 7))
    image = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
    labels = [FRIENDLY_LABELS.get(column, column) for column in corr_cols]
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_yticklabels(labels)
    _prepare_chart_axis(ax, "Feature Correlation Heatmap")
    ax.grid(False)
    colorbar = fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    colorbar.set_label("Correlation", color=MUTED_TEXT_COLOR)
    colorbar.ax.yaxis.set_tick_params(color=MUTED_TEXT_COLOR)
    plt.setp(colorbar.ax.get_yticklabels(), color=MUTED_TEXT_COLOR)
    charts["correlation_heatmap"] = _save_plot(fig, "correlation_heatmap.png")

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = {"High priority": GREEN, "Priority": CYAN, "Not priority": SLATE}
    for label in order:
        segment = integrated[integrated["priority_label"].eq(label)]
        ax.scatter(
            segment["municipal_multidimensional_poverty_index"],
            segment["collection_center_distance_km"],
            label=label,
            color=colors[label],
            alpha=0.72,
            s=28,
            edgecolors=CHART_BG,
            linewidths=0.25,
        )
    _prepare_chart_axis(ax, "Social Vulnerability and Recycling Access", "Poverty index", "Distance to collection center (km)")
    legend = ax.legend(title="Priority class", facecolor=PANEL_BG, edgecolor=GRID_COLOR)
    legend.get_title().set_color(TEXT_COLOR)
    for text in legend.get_texts():
        text.set_color(MUTED_TEXT_COLOR)
    charts["poverty_access"] = _save_plot(fig, "poverty_access.png")

    fig, ax = plt.subplots(figsize=(8, 5))
    eca_by_department = (
        data["eca_records"]
        .groupby("department_name")
        .size()
        .sort_values(ascending=False)
        .head(10)
    )
    ax.barh(eca_by_department.index, eca_by_department.values, color=GREEN)
    ax.invert_yaxis()
    _prepare_chart_axis(ax, "Top Departments by Registered Recycling Facilities", "Facility records", "")
    charts["eca_departments"] = _save_plot(fig, "eca_departments.png")

    fig, ax = plt.subplots(figsize=(8, 4.8))
    hazardous_trend = (
        data["hazardous_records"].groupby("year")["total_hazardous_waste_kg"].sum().reset_index()
    )
    ax.plot(
        hazardous_trend["year"],
        hazardous_trend["total_hazardous_waste_kg"],
        color=CYAN,
        marker="o",
        linewidth=2.4,
    )
    ax.fill_between(
        hazardous_trend["year"],
        hazardous_trend["total_hazardous_waste_kg"],
        color=CYAN,
        alpha=0.16,
    )
    _prepare_chart_axis(ax, "Hazardous Waste Reporting Trend", "Year", "Total hazardous waste (kg)")
    charts["hazardous_trend"] = _save_plot(fig, "hazardous_trend.png")

    locality = data["bogota_locality"].dropna(subset=["locality_code"]).copy()
    pivot = locality[locality["year"].isin([2018, 2035])].pivot_table(
        index="locality_name",
        columns="year",
        values="projected_households",
        aggfunc="sum",
    )
    if {2018, 2035}.issubset(pivot.columns):
        growth = ((pivot[2035] - pivot[2018]) / pivot[2018] * 100).sort_values(ascending=False).head(10)
    else:
        growth = pd.Series(dtype=float)
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.barh(growth.index, growth.values, color=AMBER)
    ax.invert_yaxis()
    _prepare_chart_axis(ax, "Capital Localities with Highest Household Growth", "Projected growth 2018-2035 (%)", "")
    charts["bogota_growth"] = _save_plot(fig, "bogota_growth.png")

    scaled_columns = [f"scaled_{column}" for column in MODEL_FEATURE_COLUMNS[:8] if f"scaled_{column}" in integrated]
    scaled = integrated[scaled_columns].rename(
        columns={f"scaled_{column}": FRIENDLY_LABELS.get(column, column) for column in MODEL_FEATURE_COLUMNS}
    )
    fig, ax = plt.subplots(figsize=(9, 4.8))
    box = ax.boxplot(
        [scaled[column].dropna() for column in scaled.columns],
        vert=False,
        patch_artist=True,
        labels=list(scaled.columns),
    )
    for patch in box["boxes"]:
        patch.set_facecolor(BLUE)
        patch.set_alpha(0.58)
        patch.set_edgecolor(CYAN)
    for element in ["whiskers", "caps", "medians"]:
        for artist in box[element]:
            artist.set_color(TEXT_COLOR if element == "medians" else CYAN)
    _prepare_chart_axis(ax, "Normalized Feature Profile", "Standard score", "")
    charts["feature_scaling"] = _save_plot(fig, "feature_scaling.png")

    return charts


def build_relationships() -> list[dict[str, str]]:
    return [
        {
            "relationship": "Municipality code",
            "datasets": "Final modeling dataset + CNPV census",
            "purpose": "Creates a reliable official join between the supervised target table and census household/population features.",
        },
        {
            "relationship": "Department code",
            "datasets": "Final modeling dataset + department projections",
            "purpose": "Adds projected demographic pressure for 2026, 2030, and 2050.",
        },
        {
            "relationship": "Department and municipality normalized keys",
            "datasets": "Final modeling dataset + facility registry",
            "purpose": "Connects municipal rows to recycling infrastructure counts and capacities.",
        },
        {
            "relationship": "Antioquia municipality normalized keys",
            "datasets": "Final modeling dataset + hazardous waste records",
            "purpose": "Adds environmental pressure indicators while avoiding ambiguous joins for duplicated municipality names.",
        },
        {
            "relationship": "Capital municipality code",
            "datasets": "Final modeling dataset + capital household projections",
            "purpose": "Adds high-resolution urban growth context to the capital city record and supports separate locality analysis.",
        },
    ]


def build_engineering_steps() -> list[dict[str, str]]:
    return [
        {
            "step": "Source ingestion",
            "action": "Read CSV, XLS, and XLSX files with explicit header handling and locale-aware numeric parsing.",
            "impact": "Prevents silent data corruption from mixed number formats and non-tabular workbook headers.",
        },
        {
            "step": "Text normalization",
            "action": "Create uppercase accent-insensitive keys for municipality and department joins.",
            "impact": "Improves matching across sources that use different punctuation or accent conventions.",
        },
        {
            "step": "Data cleaning",
            "action": "Convert unavailable value markers to missing values, remove footer rows, keep municipal records, and aggregate facility records.",
            "impact": "Produces reproducible tables that are suitable for EDA and machine learning preparation.",
        },
        {
            "step": "Dataset integration",
            "action": "Merge base municipal records with census, department projections, recycling facility capacity, hazardous waste, and capital household projections.",
            "impact": "Combines demand, accessibility, vulnerability, infrastructure, and environmental pressure in one analytical table.",
        },
        {
            "step": "Feature engineering",
            "action": "Create urbanization, collection gap, uncollected recyclable waste, center pressure, access need, and population growth features.",
            "impact": "Transforms raw attributes into signals aligned with recommendation and prioritization decisions.",
        },
        {
            "step": "Feature preparation",
            "action": "Encode priority labels and generate standardized numerical feature columns.",
            "impact": "Creates a model-ready feature matrix for classification or recommendation experiments.",
        },
    ]


def build_script_explanations() -> list[dict[str, str]]:
    return [
        {
            "script": "cleanData/cleaning_data_eca.py",
            "previous_role": "Aggregated recycling facility capacity by municipality.",
            "improvement": "Now delegates to the shared pipeline, fixes encoding assumptions, parses locale numbers, and preserves active, authorization, compatibility, and capacity indicators.",
        },
        {
            "script": "cleanData/cleaning_data_population.py",
            "previous_role": "Attempted to extract population from the department projection workbook.",
            "improvement": "Now produces clean department projections and official CNPV municipal census outputs through the same reusable pipeline.",
        },
        {
            "script": "cleanData/cleaning_data_poverty.py",
            "previous_role": "Referenced a poverty workbook that is not present in the repository.",
            "improvement": "Now extracts poverty-related features from the existing modeling dataset and writes a clean municipal social vulnerability table.",
        },
        {
            "script": "createDataset/create_dataset.py",
            "previous_role": "Merged a small set of cleaned files with an inner join.",
            "improvement": "Now builds the full integrated SmartRecycleAI dataset and the model feature matrix from every available source.",
        },
    ]


def build_project_context(
    data: dict[str, pd.DataFrame],
    catalog: list[dict[str, Any]],
    charts: dict[str, str],
    kmeans_analysis: dict[str, Any],
) -> dict[str, Any]:
    integrated = data["integrated"]
    feature_matrix = data["feature_matrix"]

    preview_columns = [
        "municipality_code",
        "municipality_name",
        "department_name",
        "total_population",
        "census_total_population_2018",
        "municipal_multidimensional_poverty_index",
        "recyclable_kg_day",
        "collection_coverage_percentage",
        "eca_facility_count",
        "total_hazardous_waste_kg_latest",
        "priority_label",
    ]
    preview_columns = [column for column in preview_columns if column in integrated.columns]

    high_priority = int(integrated["priority_label"].eq("High priority").sum())
    priority = int(integrated["priority_label"].eq("Priority").sum())
    not_priority = int(integrated["priority_label"].eq("Not priority").sum())

    context = {
        "metrics": {
            "municipalities": int(integrated["municipality_code"].nunique()),
            "model_features": int(len([column for column in MODEL_FEATURE_COLUMNS if column in integrated.columns])),
            "high_priority_municipalities": high_priority,
            "priority_municipalities": priority + high_priority,
            "registered_recycling_facilities": int(data["eca_records"].shape[0]),
            "processed_artifacts": len(list(PROCESSED_DIR.glob("*.csv"))),
            "kmeans_clusters": int(kmeans_analysis["selected_k"]),
        },
        "priority_counts": {
            "High priority": high_priority,
            "Priority": priority,
            "Not priority": not_priority,
        },
        "dataset_catalog": catalog,
        "relationships": build_relationships(),
        "engineering_steps": build_engineering_steps(),
        "script_explanations": build_script_explanations(),
        "statistical_summary": build_statistical_summary(integrated),
        "dataset_preview": dataframe_records(integrated[preview_columns], limit=12),
        "dataset_preview_columns": [FRIENDLY_LABELS.get(column, column.replace("_", " ").title()) for column in preview_columns],
        "feature_matrix_preview": dataframe_records(feature_matrix.head(8), limit=8),
        "feature_matrix_columns": list(feature_matrix.columns[:12]),
        "charts": charts,
        "kmeans_analysis": kmeans_analysis,
        "generated_files": sorted(path.name for path in PROCESSED_DIR.glob("*.csv")),
        "model_feature_columns": [FRIENDLY_LABELS.get(column, column) for column in MODEL_FEATURE_COLUMNS if column in integrated.columns],
    }
    return context


def write_reports(context: dict[str, Any]) -> None:
    ensure_directories()
    serializable = {
        "metrics": context["metrics"],
        "priority_counts": context["priority_counts"],
        "dataset_catalog": context["dataset_catalog"],
        "relationships": context["relationships"],
        "engineering_steps": context["engineering_steps"],
        "model_feature_columns": context["model_feature_columns"],
        "kmeans_analysis": {
            "algorithm": context["kmeans_analysis"]["algorithm"],
            "records_used": context["kmeans_analysis"]["records_used"],
            "selected_k": context["kmeans_analysis"]["selected_k"],
            "features_used_count": context["kmeans_analysis"]["features_used_count"],
            "evaluation_metrics": context["kmeans_analysis"]["evaluation_metrics"],
            "cluster_summary": context["kmeans_analysis"]["cluster_summary"],
            "operational_recommendations": context["kmeans_analysis"]["operational_recommendations"],
            "generated_files": context["kmeans_analysis"]["generated_files"],
        },
        "generated_files": context["generated_files"],
    }
    DATASET_PROFILE_FILE.write_text(json.dumps(serializable, indent=2), encoding="utf-8")
    DASHBOARD_CONTEXT_FILE.write_text(json.dumps(context, indent=2), encoding="utf-8")


def prepare_dataframes() -> dict[str, pd.DataFrame]:
    base = load_final_modeling_dataset()
    eca_summary = clean_eca_data()
    eca_records = pd.read_csv(PROCESSED_DIR / "eca_records_clean.csv", encoding="utf-8")
    hazardous_records, hazardous_summary = clean_hazardous_waste_data()
    census = clean_census_data()
    department_projection, department_summary = clean_department_population_projections()
    bogota_locality, bogota_upz, _ = clean_bogota_household_projections()
    integrated, feature_matrix = build_integrated_dataset()
    return {
        "base": base,
        "eca_summary": eca_summary,
        "eca_records": eca_records,
        "hazardous_records": hazardous_records,
        "hazardous_summary": hazardous_summary,
        "census": census,
        "department_projection": department_projection,
        "department_summary": department_summary,
        "bogota_locality": bogota_locality,
        "bogota_upz": bogota_upz,
        "integrated": integrated,
        "feature_matrix": feature_matrix,
    }


def build_dashboard_context() -> dict[str, Any]:
    ensure_directories()
    data = prepare_dataframes()
    catalog = build_dataset_catalog(data)
    charts = generate_charts(data, catalog)
    kmeans_analysis = run_kmeans_analysis(
        data["integrated"],
        STATIC_GENERATED_DIR,
        PROCESSED_DIR,
        FRIENDLY_LABELS,
    )
    charts.update(kmeans_analysis["charts"])
    context = build_project_context(data, catalog, charts, kmeans_analysis)
    write_reports(context)
    return context


def load_cached_dashboard_context() -> dict[str, Any] | None:
    if not DASHBOARD_CONTEXT_FILE.exists():
        return None
    try:
        context = json.loads(DASHBOARD_CONTEXT_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    if "kmeans_analysis" not in context:
        return None
    if "kmeans_elbow" not in context.get("charts", {}):
        return None
    chart_files = context.get("charts", {}).values()
    if not all((STATIC_GENERATED_DIR / filename).exists() for filename in chart_files):
        return None
    return context


@lru_cache(maxsize=1)
def get_dashboard_context() -> dict[str, Any]:
    ensure_directories()
    cached_context = load_cached_dashboard_context()
    if cached_context is not None:
        return cached_context
    return build_dashboard_context()


def run_full_pipeline() -> dict[str, Any]:
    get_dashboard_context.cache_clear()
    return build_dashboard_context()

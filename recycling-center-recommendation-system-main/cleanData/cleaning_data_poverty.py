from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from smartrecycleai.data_pipeline import _write_csv, load_final_modeling_dataset


def clean_social_vulnerability_data():
    dataset = load_final_modeling_dataset()
    columns = [
        "municipality_code",
        "municipality_name",
        "department_code",
        "municipal_multidimensional_poverty_index",
        "overcrowding_deprivation_percentage",
        "water_deprivation_percentage",
        "health_deprivation_percentage",
        "informal_work_percentage",
    ]
    output = dataset[columns].copy()
    _write_csv(output, "social_vulnerability_clean.csv")
    return output


def main():
    output = clean_social_vulnerability_data()
    print("Social vulnerability data cleaned successfully.")
    print(f"Municipal records created: {len(output)}")
    return output


if __name__ == "__main__":
    main()

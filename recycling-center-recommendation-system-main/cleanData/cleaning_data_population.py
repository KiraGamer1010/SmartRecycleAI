from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from smartrecycleai.data_pipeline import (
    clean_census_data,
    clean_department_population_projections,
)


def main():
    census = clean_census_data()
    _, department_summary = clean_department_population_projections()
    print("Population and census data cleaned successfully.")
    print(f"Municipal census records created: {len(census)}")
    print(f"Department projection summaries created: {len(department_summary)}")
    return census, department_summary


if __name__ == "__main__":
    main()

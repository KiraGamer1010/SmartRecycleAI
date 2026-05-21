from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from smartrecycleai.data_pipeline import clean_eca_data


def main():
    summary = clean_eca_data()
    print("Recycling facility data cleaned successfully.")
    print(f"Municipality summaries created: {len(summary)}")
    return summary


if __name__ == "__main__":
    main()

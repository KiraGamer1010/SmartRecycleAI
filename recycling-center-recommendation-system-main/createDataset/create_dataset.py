from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from smartrecycleai.data_pipeline import run_full_pipeline


def create_dataset():
    context = run_full_pipeline()
    print("Integrated SmartRecycleAI dataset created successfully.")
    print(f"Processed artifacts created: {context['metrics']['processed_artifacts']}")
    print(f"Model features prepared: {context['metrics']['model_features']}")
    return context


if __name__ == "__main__":
    create_dataset()

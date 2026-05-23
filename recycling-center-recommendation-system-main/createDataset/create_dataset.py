from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from smartrecycleai.data_pipeline import run_full_pipeline
from smartrecycleai.model_training import train_supervised_models


def create_dataset():
    context = run_full_pipeline()
    model_context = train_supervised_models(force=True)
    print("Integrated SmartRecycleAI dataset created successfully.")
    print(f"Processed artifacts created: {context['metrics']['processed_artifacts']}")
    print(f"Model features prepared: {context['metrics']['model_features']}")
    if model_context.get("available"):
        print(f"Supervised models trained: {len(model_context['models'])}")
        print(f"Selected model: {model_context['best_model']['display_name']}")
    return context


if __name__ == "__main__":
    create_dataset()

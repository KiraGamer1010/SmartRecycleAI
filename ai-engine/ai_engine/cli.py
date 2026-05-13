import argparse
from pathlib import Path

from ai_engine.pipelines.classification_pipeline import ClassificationPipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run SmartRecycleAI image detection.")
    parser.add_argument("image", type=Path, help="Path to an image file.")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    result = ClassificationPipeline().classify_image(args.image)
    print(result.model_dump_json(indent=2))

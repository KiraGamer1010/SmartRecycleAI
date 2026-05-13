from pathlib import Path


SUPPORTED_IMAGE_SUFFIXES = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def validate_image_path(image_path: Path) -> None:
    if not image_path.exists():
        raise ValueError(f"Image path does not exist: {image_path}")

    if image_path.suffix.lower() not in SUPPORTED_IMAGE_SUFFIXES:
        raise ValueError(
            f"Unsupported image type '{image_path.suffix}'. "
            f"Expected one of: {', '.join(sorted(SUPPORTED_IMAGE_SUFFIXES))}"
        )


def read_image_shape(image_path: Path) -> tuple[int, int, int]:
    import cv2

    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"OpenCV could not read image: {image_path}")
    height, width, channels = image.shape
    return height, width, channels

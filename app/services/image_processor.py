from pathlib import Path

import cv2


def preprocess_image(input_path: Path, output_path: Path) -> None:
    image = cv2.imread(str(input_path))

    if image is None:
        raise ValueError(f"Cannot read image: {input_path}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    denoised = cv2.GaussianBlur(gray, (3, 3), 0)

    processed = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        10,
    )

    success = cv2.imwrite(str(output_path), processed)

    if not success:
        raise ValueError(f"Cannot save processed image: {output_path}")

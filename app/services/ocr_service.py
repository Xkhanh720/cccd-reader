import easyocr

reader = easyocr.Reader(["vi", "en"], gpu=False)

def read_text(image_path: str):
    results = reader.readtext(image_path)

    converted_results = []

    for box, text, confidence in results:
        converted_results.append(
            {
                "box": [
                [int(point[0]), int(point[1])]
                for point in box
            ],
            "text": text,
            "confidence": float(confidence),
        }
    )

    return converted_results

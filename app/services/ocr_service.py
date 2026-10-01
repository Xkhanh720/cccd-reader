import easyocr

reader = easyocr.Reader(["vi", "en"], gpu=False)


def read_text(image_path: str):
    results = reader.readtext(image_path)

    return results

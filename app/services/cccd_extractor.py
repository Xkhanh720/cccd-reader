import re


def extract_cccd_fields(ocr_results: list[dict]) -> dict:
    result = {
        "id_number": None,
        "full_name": None,
        "date_of_birth": None,
        "gender": None,
        "nationality": None,
        "place_of_origin": None,
        "residence": None,
    }

    texts = [item["text"].strip() for item in ocr_results]
    full_text = "\n".join(texts)

    # -------------------------
    # 1. Số CCCD
    # -------------------------
    id_candidates = re.findall(r"\b\d{12}\b", full_text)

    if id_candidates:
        result["id_number"] = id_candidates[0]

    # -------------------------
    # 2. Ngày sinh
    # -------------------------
    date_candidates = re.findall(
        r"\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b",
        full_text,
    )

    if date_candidates:
        result["date_of_birth"] = date_candidates[0]

    # -------------------------
    # 3. Họ tên
    # -------------------------
    for i, text in enumerate(texts):
        normalized = text.lower()

        if "h?" in normalized and "ten" in normalized:
            if i + 1 < len(texts):
                result["full_name"] = texts[i + 1]
                break

        if "ho va ten" in normalized:
            if i + 1 < len(texts):
                result["full_name"] = texts[i + 1]
                break

    # -------------------------
    # 4. Quốc tịch
    # -------------------------
    for text in texts:
        if "việt nam" in text.lower():
            result["nationality"] = "Việt Nam"
            break

    # -------------------------
    # 5. Giới tính
    # -------------------------
    for text in texts:
        lower_text = text.lower()

        if re.search(r"\bnam\b", lower_text):
            result["gender"] = "Nam"
            break

        if re.search(r"\bnữ\b", lower_text):
            result["gender"] = "Nữ"
            break

    # -------------------------
    # 6. Quê quán
    # -------------------------
    for i, text in enumerate(texts):
        lower_text = text.lower()

        if "que quán" in lower_text or "place" in lower_text:
            if i + 1 < len(texts):
                result["place_of_origin"] = texts[i + 1]
                break

    return result

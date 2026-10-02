from app.services.ocr_service import read_text
from app.services.cccd_extractor import extract_cccd_fields


image_path = "app/uploads/a4b26606b5ee4ad695c135526aaeafb0_processed.png"

ocr_results = read_text(image_path)

fields = extract_cccd_fields(ocr_results)

print(fields)


from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile

from app.services.cccd_extractor import extract_cccd_fields


app = FastAPI(
    title="CCCD Reader API",
    description="Backend API for extracting information from Vietnamese CCCD images",
    version="0.1.0",
)

UPLOAD_DIR = Path("app/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
}


@app.get("/")
def root():
    return {
        "message": "CCCD Reader API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.post("/api/v1/upload")
@app.post("/api/v1/upload")
async def upload_image(file: UploadFile = File(...)):
    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, JPEG and PNG images are allowed",
        )

    file_id = uuid4().hex
    filename = f"{file_id}{extension}"
    file_path = UPLOAD_DIR / filename

    content = await file.read()

    with open(file_path, "wb") as buffer:
        buffer.write(content)

    try:
        cccd_data = extract_cccd_fields(
            str(file_path)
        )

    except ValueError as error:
        file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    return {
        "message": "CCCD extraction completed successfully",
        "filename": filename,
        "size": len(content),
        "data": cccd_data,
    }

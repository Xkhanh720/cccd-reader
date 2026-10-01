from pathlib import Path
from uuid import uuid4
from app.services.image_processor import preprocess_image
from fastapi import FastAPI, File, UploadFile, HTTPException


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

    return {
        "message": "Image uploaded successfully",
        "filename": filename,
        "path": str(file_path),
        "size": len(content),
    }
@app.post("/api/v1/upload")
async def upload_image(file: UploadFile = File(...)):
    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, JPEG and PNG images are allowed",
        )

    file_id = uuid4().hex

    original_filename = f"{file_id}{extension}"
    processed_filename = f"{file_id}_processed.png"

    original_path = UPLOAD_DIR / original_filename
    processed_path = UPLOAD_DIR / processed_filename

    content = await file.read()

    with open(original_path, "wb") as buffer:
        buffer.write(content)

    try:
        preprocess_image(
            original_path,
            processed_path,
        )
    except ValueError as error:
        original_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    return {
        "message": "Image uploaded and processed successfully",
        "original_file": original_filename,
        "processed_file": processed_filename,
        "size": len(content),
    }

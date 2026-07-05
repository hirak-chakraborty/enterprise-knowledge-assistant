from fastapi import APIRouter, File, UploadFile
import os
import shutil
from backend.app.utils.pdf_parser import extract_text_from_pdf

router = APIRouter()

UPLOAD_FOLDER = "backend/uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    text = extract_text_from_pdf(file_path)

    return {
        "filename": file.filename,
        "message": "File uploaded successfully",
        "characters_extracted": len(text),
        "preview": text[:500]
    }
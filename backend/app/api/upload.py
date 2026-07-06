from fastapi import APIRouter, File, UploadFile
import os
import shutil

from backend.app.services.document_service import DocumentService

router = APIRouter()

UPLOAD_FOLDER = "backend/uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
document_service = DocumentService()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    chunks = document_service.process_document(file_path)
    return {
    "filename": file.filename,
    "chunks_created": len(chunks),
    "first_chunk": chunks[0],
    "last_chunk": chunks[-1]
}
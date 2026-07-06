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

    result = document_service.process_document(file_path)
    chunks = result["chunks"]
    embeddings = result["embeddings"]
    return {
    "filename": file.filename,
    "chunks_created": len(chunks),
    "embedding_dimension": len(embeddings[0]) if embeddings is not None and len(embeddings) > 0 else 0,
    "first_chunk": chunks[0] if chunks else ""
}
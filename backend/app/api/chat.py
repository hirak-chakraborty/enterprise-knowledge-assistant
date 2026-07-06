from fastapi import APIRouter

from backend.app.services.retrieval_service import RetrievalService

router = APIRouter()

retrieval_service = RetrievalService()


@router.get("/search")
def search(question: str):

    return retrieval_service.search(question)
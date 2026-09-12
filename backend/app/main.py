from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.health import router as health_router
from backend.app.api.upload import router as upload_router
from backend.app.api.chat import router as chat_router


app = FastAPI(
    title="Enterprise Knowledge Assistant API",
    version="1.0.0",
    description="Backend API for the Enterprise Knowledge Assistant"
)

# Allow the local Vite development server to call the API from the browser.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(upload_router)
app.include_router(chat_router)


@app.get("/")
def root():
    return {
        "message": "Enterprise Knowledge Assistant API is running!"
    }

from fastapi import FastAPI

app = FastAPI(
    title="Enterprise Knowledge Assistant API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Enterprise Knowledge Assistant API is running!"
    }
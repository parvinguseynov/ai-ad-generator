from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from schemas import AdRequest, AdResponse
from generator import generate_all

app = FastAPI()


@app.get("/")
def read_root():
    return FileResponse("static/index.html")


@app.post("/generate", response_model=AdResponse)
def generate_ad(request: AdRequest):
    result = generate_all(request.business, request.product)
    if result is None:
        raise HTTPException(
            status_code=502,
            detail="Failed to generate valid ad content. Please try again.",
        )
    return result

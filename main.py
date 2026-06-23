from fastapi import FastAPI
from schemas import AdRequest

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Server is running"}


@app.post("/generate")
def generate_ad(request: AdRequest):
    return {
        "received_business": request.business,
        "received_product": request.product,
    }

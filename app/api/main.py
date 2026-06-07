from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routers import data, train, eval

app = FastAPI(
    title="LLMOps API",
    description="REST API for managing data validation, model fine-tuning, and evaluation pipelines.",
    version="1.0.0"
)

# Allow CORS for UI access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(data.router, prefix="/api/v1/data", tags=["Data"])
app.include_router(train.router, prefix="/api/v1/train", tags=["Training"])
app.include_router(eval.router, prefix="/api/v1/eval", tags=["Evaluation"])

@app.get("/health")
def health_check():
    return {"status": "healthy"}

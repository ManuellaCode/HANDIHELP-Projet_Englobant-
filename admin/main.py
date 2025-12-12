from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import admin_api_router

app = FastAPI(
    title="HandiHelper Admin API",
    description="API Backend pour le dashboard admin",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les routers admin
app.include_router(admin_api_router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "HandiHelper Admin API"}


@app.get("/health")
def health():
    return {"status": "healthy"}
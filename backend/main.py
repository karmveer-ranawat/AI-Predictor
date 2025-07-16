# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from route.auth_routes import router as auth_router
from route.scanner_routes import router as scanner_router
from route.ml_routes import router as ml_router


app = FastAPI()

# Allow frontend dev server access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load routes
app.include_router(auth_router, prefix="/auth")
app.include_router(scanner_router, prefix="/scanner")
app.include_router(ml_router, prefix="/ml")


@app.get("/")
def root():
    return {"message": "Backend is running"}

@app.get("/info")
def root():
    return {"message": "here is ur info"}
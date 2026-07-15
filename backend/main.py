from fastapi import FastAPI
from agents.router import router
from database import init_db

# Initialize the database when the server starts
init_db()

app = FastAPI(title="TechMart AI Support API")

app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "TechMart AI API is running!"}
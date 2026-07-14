from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agents.router import router as agent_router
from agents.faq import router as faq_router
from agents.technical import router as tech_router
from agents.billing import router as billing_router
from agents.product import router as product_router      # <-- ADDED
from agents.complaint import router as complaint_router  # <-- ADDED
from agents.billing import router as billing_router
from agents.technical import router as tech_router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agents.router import router as agent_router
from agents.faq import router as faq_router

# 1. Create the app FIRST
app = FastAPI(title="Multi-Agent Support API", version="1.0")

# 2. Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. NOW connect the routers (since 'app' exists now!)
app.include_router(agent_router, prefix="/api/v1")
app.include_router(faq_router, prefix="/api/v1/agents")
app.include_router(tech_router, prefix="/api/v1/agents")
app.include_router(billing_router, prefix="/api/v1/agents")
app.include_router(agent_router, prefix="/api/v1")
app.include_router(faq_router, prefix="/api/v1/agents")
app.include_router(tech_router, prefix="/api/v1/agents")
app.include_router(billing_router, prefix="/api/v1/agents")
app.include_router(product_router, prefix="/api/v1/agents")      # <-- ADDED
app.include_router(complaint_router, prefix="/api/v1/agents")    # <-- ADDED

# 4. Root endpoint
@app.get("/")
async def root():
    return {"message": "Multi-Agent Support API is running!"}
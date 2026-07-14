import os
import json
from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

# 1. Import all your specialized agent functions
from agents.faq import ask_faq, FAQQuery
from agents.technical import resolve_tech, TechQuery
from agents.billing import resolve_billing, BillingQuery
from agents.product import resolve_product, ProductQuery
from agents.complaint import resolve_complaint, ComplaintQuery

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

router = APIRouter()

class UserQuery(BaseModel):
    query: str

class ChatResponse(BaseModel):
    original_query: str
    handled_by: str
    ai_response: str

@router.post("/chat", response_model=ChatResponse)
async def master_chat(request: UserQuery):
    """
    The Master Orchestrator: Detects intent and automatically routes the query to the correct agent.
    """
    # Phase 1: Determine the Intent
    prompt = f"""
    You are an intelligent customer support router. 
    Analyze this customer query: "{request.query}"
    
    Which of the following SINGLE departments should handle this?
    Options: ["billing", "technical", "product", "complaint", "faq"]
    
    Respond ONLY with a valid JSON array containing exactly one string representing the chosen department. 
    Do not include markdown formatting or any other text.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-flash-lite-latest',
            contents=prompt
        )
        clean_text = response.text.strip().strip("`").strip("json").strip()
        agents_to_trigger = json.loads(clean_text)
        primary_agent = agents_to_trigger[0].lower() if agents_to_trigger else "faq"
    except Exception as e:
        print(f"Error routing: {e}")
        primary_agent = "faq"
        
    # Phase 2: Automatically forward the query to the chosen agent's logic
    if primary_agent == "technical":
        agent_result = await resolve_tech(TechQuery(query=request.query))
    elif primary_agent == "billing":
        agent_result = await resolve_billing(BillingQuery(query=request.query))
    elif primary_agent == "product":
        agent_result = await resolve_product(ProductQuery(query=request.query))
    elif primary_agent == "complaint":
        agent_result = await resolve_complaint(ComplaintQuery(query=request.query))
    else:
        agent_result = await ask_faq(FAQQuery(query=request.query))
        
    # Phase 3: Return the final answer directly to the user
    # Note: FAQ uses "ai_answer", others use "ai_response". We handle both here!
    final_answer = agent_result.get("ai_response", agent_result.get("ai_answer", "Error retrieving response."))
    department_name = agent_result.get("department", "FAQ Support")
    
    return ChatResponse(
        original_query=request.query,
        handled_by=department_name,
        ai_response=final_answer
    )
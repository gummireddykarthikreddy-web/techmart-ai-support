import os
from fastapi import APIRouter
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

router = APIRouter()

class ComplaintQuery(BaseModel):
    query: str
    frustration_level: str = "High"

@router.post("/resolve-complaint")
async def resolve_complaint(request: ComplaintQuery):
    """
    Acts as a specialized de-escalation agent for angry or dissatisfied customers.
    """
    prompt = f"""
    You are a deeply empathetic, patient, and accommodating Customer Success Manager for TechMart Electronics.
    Your job is to de-escalate angry customers and resolve their complaints.
    
    Customer Complaint: "{request.query}"
    Estimated Frustration Level: "{request.frustration_level}"
    
    Rules for your response:
    1. Start with a sincere, unreserved apology for their poor experience.
    2. Validate their feelings of frustration completely.
    3. Offer a concrete next step to make things right (e.g., escalating to a human manager, offering a courtesy credit).
    4. Keep the tone gentle and professional. Do not use markdown headers.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-flash-lite-latest',
            contents=prompt
        )
        answer = response.text.strip()
    except Exception as e:
        print(f"Error in Complaint Agent: {e}")
        answer = "System error: We apologize, but our support desk is experiencing an outage."
        
    return {
        "original_query": request.query,
        "department": "Customer Success (De-escalation)",
        "ai_response": answer
    }
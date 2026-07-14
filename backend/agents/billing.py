import os
from fastapi import APIRouter
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv

# Load API key and initialize the Gemini Client
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

router = APIRouter()

# Define the expected incoming data payload
class BillingQuery(BaseModel):
    query: str
    account_status: str = "Active" 

@router.post("/resolve-billing")
async def resolve_billing(request: BillingQuery):
    """
    Acts as a specialized billing support agent to handle refunds and invoices.
    """
    
    prompt = f"""
    You are a professional, reassuring Billing Support Agent for TechMart Electronics.
    Your job is to resolve financial, invoice, and refund issues.
    
    Customer Issue: "{request.query}"
    Account Status: "{request.account_status}"
    
    Rules for your response:
    1. Maintain a highly professional and secure tone.
    2. Acknowledge the specific financial concern.
    3. Clearly outline the next steps for resolution using simple bullet points (do not use headers like ##).
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-flash-lite-latest',
            contents=prompt
        )
        answer = response.text.strip()
    except Exception as e:
        print(f"Error in Billing Agent: {e}")
        answer = "System error: Our secure billing servers are temporarily down. Please try again."
        
    return {
        "original_query": request.query,
        "department": "Billing Support",
        "ai_response": answer
    }
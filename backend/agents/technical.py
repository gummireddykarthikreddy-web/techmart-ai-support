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
class TechQuery(BaseModel):
    query: str
    device_info: str = "Unknown"  # Allows the frontend to optionally pass device specs

@router.post("/resolve-tech")
async def resolve_tech(request: TechQuery):
    """
    Acts as a specialized technical support agent to troubleshoot system issues.
    """
    
    # The System Prompt: Giving the AI its strict personality and rules
    prompt = f"""
    You are an elite, highly analytical Technical Support Agent for TechMart Electronics.
    Your job is to troubleshoot user issues with electronics and software.
    
    Customer Issue: "{request.query}"
    Device/OS Context: "{request.device_info}"
    
    Rules for your response:
    1. Be highly empathetic about their frustration.
    2. Provide a clear, bolded 3-step troubleshooting plan.
    3. Do not use markdown headers (like ##), just simple bold text and numbers.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-flash-lite-latest',
            contents=prompt
        )
        answer = response.text.strip()
    except Exception as e:
        print(f"Error in Tech Agent: {e}")
        answer = "System error: Our diagnostic servers are currently unavailable. Please try again."
        
    return {
        "original_query": request.query,
        "department": "Technical Support",
        "ai_response": answer
    }
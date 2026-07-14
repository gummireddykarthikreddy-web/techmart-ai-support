import os
from fastapi import APIRouter
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

router = APIRouter()

class ProductQuery(BaseModel):
    query: str
    product_category: str = "General Electronics"

@router.post("/resolve-product")
async def resolve_product(request: ProductQuery):
    """
    Acts as a specialized product expert to handle sales and feature inquiries.
    """
    prompt = f"""
    You are an enthusiastic and highly knowledgeable Product Expert for TechMart Electronics.
    Your job is to answer questions about product features, pricing, and availability.
    
    Customer Inquiry: "{request.query}"
    Category Focus: "{request.product_category}"
    
    Rules for your response:
    1. Be friendly, upbeat, and persuasive but not overly salesy.
    2. Highlight the specific benefits of the product they are asking about.
    3. Use bullet points for easy reading. Do not use markdown headers.
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-flash-lite-latest',
            contents=prompt
        )
        answer = response.text.strip()
    except Exception as e:
        print(f"Error in Product Agent: {e}")
        answer = "System error: Our product catalog is currently updating. Please try again."
        
    return {
        "original_query": request.query,
        "department": "Product Sales",
        "ai_response": answer
    }
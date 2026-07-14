import os
from fastapi import APIRouter
from pydantic import BaseModel
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from google import genai
from dotenv import load_dotenv

# Load API key and initialize the NEW Gemini Client
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

router = APIRouter()

class FAQQuery(BaseModel):
    query: str

# Load the FAISS vector database into memory
db_path = os.path.join(os.path.dirname(__file__), "../vectorstore/faiss_index")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_db = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)

@router.post("/ask-faq")
async def ask_faq(request: FAQQuery):
    """
    Retrieves context from the vector database and uses Gemini to answer the query.
    """
    # Semantic Search
    relevant_docs = vector_db.similarity_search(request.query, k=2)
    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    
    prompt = f"""
    You are a polite and helpful customer support agent for TechMart Electronics.
    Answer the customer's question using ONLY the provided context below. 
    If the answer is not contained in the context, politely say that you do not have that information and offer to connect them with a human agent.
    
    Context:
    {context}
    
    Customer Question: "{request.query}"
    """
    
    try:
        # Generate the final answer using the new SDK format
        response = client.models.generate_content(
         model='gemini-flash-lite-latest',
         contents=prompt
     )
        answer = response.text.strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        answer = "I am currently experiencing technical difficulties. Please try again later."
        
    return {
        "original_query": request.query,
        "retrieved_context": context,
        "ai_answer": answer
    }
import os
from google import genai
from dotenv import load_dotenv

# Load your secret key
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("Here are the models your API key has access to:")
print("-" * 50)

# Ask Google for the list and print them out
try:
    for model in client.models.list():
        # We only want to see models that can generate text
        if "generateContent" in model.supported_actions:
            print(model.name)
except Exception as e:
    print(f"Error connecting to Google: {e}")
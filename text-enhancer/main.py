import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from fastapi.middleware.cors import CORSMiddleware


# import os
# import google.generativeai as genai

# Set API Key
# API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyALZKlYvpfm9tCzpcvOf11pLhW6kpPc1wY")
# if API_KEY == "AIzaSyALZKlYvpfm9tCzpcvOf11pLhW6kpPc1wY":
#     raise ValueError("🚨 Missing or incorrect Google API key!")

# genai.configure(api_key=API_KEY)
# model = genai.GenerativeModel("gemini-pro")

genai.configure(api_key="AIzaSyALZKlYvpfm9tCzpcvOf11pLhW6kpPc1wY")

model = genai.GenerativeModel("gemini-pro")

# Set API Key
# os.environ["GOOGLE_API_KEY"] = "yAIzaSyCEHerWnJk_HT1xRkZZ07oIuqTW6IDxl5Y"

# Initialize Gemini model
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# model = genai.GenerativeModel("gemini-pro")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TextEnhancementRequest(BaseModel):
    text: str
    tone: str

@app.post("/enhance")
async def enhance_text(request: TextEnhancementRequest):
    try:
        prompt = f"Enhance this text: '{request.text}' in a '{request.tone}' tone while fixing grammar."
        response = model.generate_content(prompt)
        return {"enhanced_text": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

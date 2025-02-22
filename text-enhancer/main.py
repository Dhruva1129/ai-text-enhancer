import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from fastapi.middleware.cors import CORSMiddleware
from googletrans import Translator
from gtts import gTTS
from fastapi.responses import FileResponse

# Configure Google Gemini API Key
genai.configure(api_key="AIzaSyALZKlYvpfm9tCzpcvOf11pLhW6kpPc1wY")
model = genai.GenerativeModel("gemini-pro")

# Initialize FastAPI
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request models
class TextEnhancementRequest(BaseModel):
    text: str
    tone: str

class TranslationRequest(BaseModel):
    text: str
    language: str

class TextToSpeechRequest(BaseModel):
    text: str
    language: str

translator = Translator()

@app.post("/enhance")
async def enhance_text(request: TextEnhancementRequest):
    try:
        prompt = f"Enhance this text in a single line without using complex words in a '{request.tone}' tone while fixing grammar in a simple understandable language : '{request.text}'"
        response = model.generate_content(prompt)
        return {"enhanced_text": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/translate")
async def translate_text(request: TranslationRequest):
    try:
        translated = translator.translate(request.text, dest=request.language)
        return {"translated_text": translated.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/speak")
async def text_to_speech(request: TextToSpeechRequest):
    try:
        tts = gTTS(text=request.text, lang=request.language)
        file_path = "speech.mp3"
        tts.save(file_path)
        return FileResponse(file_path, media_type="audio/mpeg", filename="speech.mp3")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





# import google.generativeai as genai
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware
# from googletrans import Translator
# # from googletrans import Translator

# import os

# # Securely Load API Key
# # API_KEY = os.getenv("AIzaSyALZKlYvpfm9tCzpcvOf11pLhW6kpPc1wY")
# # if not API_KEY:
# #     raise ValueError("🚨 Missing or incorrect Google API key!")

# # API_KEY = os.getenv("GOOGLE_API_KEY")

# # if not API_KEY:
# #     raise ValueError("🚨 Missing or incorrect Google API key! Set GOOGLE_API_KEY in your environment variables.")

# genai.configure(api_key="AIzaSyALZKlYvpfm9tCzpcvOf11pLhW6kpPc1wY")
# model = genai.GenerativeModel("gemini-pro")

# # genai.configure(api_key=API_KEY)
# # model = genai.GenerativeModel("gemini-pro")

# # Initialize FastAPI
# app = FastAPI()

# # CORS Setup
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3001"],  # Adjust if frontend runs on a different URL
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Translator Instance
# translator = Translator()

# # Supported Tones
# SUPPORTED_TONES = [
#     "formal", "casual", "poetic", "sarcastic", "professional", "motivational"
# ]

# # Supported Languages
# SUPPORTED_LANGUAGES = {
#     "en": "English",
#     "hi": "Hindi",
#     "te": "Telugu",
#     "ta": "Tamil",
#     "kn": "Kannada",
#     "bn": "Bengali",
#     "mr": "Marathi",
#     "gu": "Gujarati",
#     "ml": "Malayalam",
#     "pa": "Punjabi",
# }

# # Request Model
# class TextEnhancementRequest(BaseModel):
#     text: str
#     tone: str
#     target_language: str = "en"  # Default to English

# @app.post("/enhance")
# async def enhance_text(request: TextEnhancementRequest):
#     try:
#         # Validate Tone
#         if request.tone not in SUPPORTED_TONES:
#             raise HTTPException(status_code=400, detail="Invalid tone selected")

#         # Validate Language
#         if request.target_language not in SUPPORTED_LANGUAGES:
#             raise HTTPException(status_code=400, detail="Invalid language selected")

#         # Generate Enhanced Text
#         prompt = f"Improve this text in a single line '{request.text}' in a {request.tone} tone while fixing grammar and making it more clear."
#         response = model.generate_content(prompt)
#         enhanced_text = response.text.strip()

#         # Translate if Necessary
#         translated_text = enhanced_text
#         if request.target_language != "en":
#             translated_text = translator.translate(enhanced_text, dest=request.target_language).text

#         return {
#             "enhanced_text": enhanced_text,
#             "translated_text": translated_text,
#             "language": SUPPORTED_LANGUAGES[request.target_language],
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))





# # import google.generativeai as genai
# # from fastapi import FastAPI, HTTPException
# # from pydantic import BaseModel
# # import os
# # from fastapi.middleware.cors import CORSMiddleware


# # # import os
# # # import google.generativeai as genai

# # # Set API Key
# # # API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyALZKlYvpfm9tCzpcvOf11pLhW6kpPc1wY")
# # # if API_KEY == "AIzaSyALZKlYvpfm9tCzpcvOf11pLhW6kpPc1wY":
# # #     raise ValueError("🚨 Missing or incorrect Google API key!")

# # # genai.configure(api_key=API_KEY)
# # # model = genai.GenerativeModel("gemini-pro")

# # genai.configure(api_key="AIzaSyALZKlYvpfm9tCzpcvOf11pLhW6kpPc1wY")

# # model = genai.GenerativeModel("gemini-pro")

# # # Set API Key
# # # os.environ["GOOGLE_API_KEY"] = "yAIzaSyCEHerWnJk_HT1xRkZZ07oIuqTW6IDxl5Y"

# # # Initialize Gemini model
# # # genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# # # model = genai.GenerativeModel("gemini-pro")

# # app = FastAPI()

# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=["http://localhost:3000"],  # React frontend
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # class TextEnhancementRequest(BaseModel):
# #     text: str
# #     tone: str

# # @app.post("/enhance")
# # async def enhance_text(request: TextEnhancementRequest):
# #     try:
# #         prompt = f"Enhance this text in simple understandable language: '{request.text}' in a '{request.tone}' tone in a sentance while fixing grammar."
# #         response = model.generate_content(prompt)
# #         return {"enhanced_text": response.text}
# #     except Exception as e: 
# #         raise HTTPException(status_code=500, detail=str(e))

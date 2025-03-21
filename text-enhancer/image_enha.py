import os
import requests
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from google.generativeai import GenerativeModel
import google.generativeai as genai

router = APIRouter()

# OCR.Space API Key
OCR_SPACE_API_KEY = "helloworld"

# Gemini setup
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))  # Set this in your .env
model = GenerativeModel("gemini-1.5-pro-latest")

@router.post("/image-to-enhanced-text/")
async def image_to_enhanced_text(
    file: UploadFile = File(...),
    tone: str = Form("formal")  # Default tone is 'formal' if not provided
):
    try:
        print(f"✅ File received: {file.filename}")
        print(f"🎨 Tone selected: {tone}")
        image_bytes = await file.read()

        # OCR.Space text extraction
        response = requests.post(
            "https://api.ocr.space/parse/image",
            files={"file": (file.filename, image_bytes, file.content_type)},
            data={
                "apikey": OCR_SPACE_API_KEY,
                "language": "eng",
                "isOverlayRequired": False,
            },
        )

        result = response.json()
        if result.get("IsErroredOnProcessing"):
            error_msg = result.get("ErrorMessage", ["OCR failed"])[0]
            raise HTTPException(status_code=400, detail=f"OCR.Space Error: {error_msg}")

        extracted_text = result["ParsedResults"][0]["ParsedText"]
        print("📝 Extracted Text:", extracted_text)

        # Enhanced prompt with tone and formatting instructions
        prompt = (
            "Improve the grammar and clarity of the following text while preserving the exact structure, formatting, and line breaks. "
            "Do not change the layout, indentation, bullet points, or paragraph spacing. Only correct grammatical errors and enhance readability.\n\n"
            f"Extracted Text:\n{extracted_text}"
        )

        gemini_response = model.generate_content(prompt)
        print("✨ Enhanced Text:", gemini_response.text)

        return {
            "enhanced_text": gemini_response.text,
            "raw_text": extracted_text
        }

    except Exception as e:
        print("❌ Server Error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))






# # image_enha.py

# import os
# from fastapi import APIRouter, UploadFile, File, HTTPException
# from google.cloud import vision
# import google.generativeai as genai

# # Set up Google credentials
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google-vision-key.json"

# # FastAPI router instead of app
# router = APIRouter()

# # Gemini + Vision setup
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
# model = genai.GenerativeModel("gemini-1.5-pro-latest")
# vision_client = vision.ImageAnnotatorClient()

# @router.post("/image-to-enhanced-text/")
# async def image_to_enhanced_text(file: UploadFile = File(...)):
#     try:
#         print("✅ File received:", file.filename)
#         image_bytes = await file.read()

#         # Vision OCR
#         image = vision.Image(content=image_bytes)
#         response = vision_client.text_detection(image=image)

#         annotations = response.text_annotations
#         if not annotations:
#             raise HTTPException(status_code=400, detail="No text detected.")

#         raw_text = annotations[0].description
#         print("📝 Extracted Text:", raw_text)

#         prompt = f"Enhance this handwritten extracted text: {raw_text}"
#         gemini_response = model.generate_content(prompt)

#         print("✨ Enhanced Text:", gemini_response.text)

#         return {
#             "enhanced_text": gemini_response.text,
#             "raw_text": raw_text
#         }

#     except Exception as e:
#         print("❌ Server Error:", str(e))  # Add this line
#         raise HTTPException(status_code=500, detail=str(e))

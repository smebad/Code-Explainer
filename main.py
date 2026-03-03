from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# FastAPI app
app = FastAPI()

# Connect to Groq AI
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Data we expect from the frontend
class CodeRequest(BaseModel):
    code: str
    action: str  # "explain", "debug", or "improve"

# Main AI endpoint
@app.post("/analyze")
async def analyze_code(request: CodeRequest):
    
    # Building the prompt based on what user wants
    prompts = {
        "explain": f"Explain this code clearly step by step:\n\n{request.code}",
        "debug": f"Find bugs and errors in this code and explain how to fix them:\n\n{request.code}",
        "improve": f"Suggest improvements for this code with examples:\n\n{request.code}"
    }

    prompt = prompts[request.action]

    # Send to Groq AI
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": "You are an expert programmer and code reviewer. Be clear, helpful and beginner friendly."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # AI response text
    result = response.choices[0].message.content

    return JSONResponse(content={"result": result})

# HTML frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")
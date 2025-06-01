import os
import json
import logging
from datetime import datetime
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
from pydantic import BaseModel
from typing import Optional

# Setup logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename=f"logs/app_{datetime.now().strftime('%Y%m%d')}.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Local LLM configuration
LOCAL_LLM_URL = "http://127.0.0.1:1234/v1/chat/completions"
DEFAULT_MODEL = "tinyllama"

# Writing styles
WRITING_STYLES = {
    "blog_intro": "Write a concise and engaging blog introduction about {topic}",
    "tweet": "Create a tweet (under 280 characters) about {topic}",
    "story": "Write a short story (2-3 paragraphs) about {topic}",
    "professional": "Write a professional email about {topic}",
    "casual": "Write a casual message about {topic}",
}

class GenerationRequest(BaseModel):
    topic: str
    style: str = "blog_intro"
    temperature: float = 0.7

class Message(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[Message]
    temperature: float = 0.7
    max_tokens: int = 500

def log_generation(topic: str, style: str, output: str, model: str):
    """Log the generation to a file"""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "topic": topic,
        "style": style,
        "model": model,
        "output": output
    }
    with open("logs/generations.log", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def generate_text(prompt: str, temperature: float = 0.7, model: str = DEFAULT_MODEL) -> str:
    """Generate text using the local LLM"""
    try:
        headers = {"Content-Type": "application/json"}
        
        # Prepare messages in chat format
        messages = [{"role": "user", "content": prompt}]
        
        data = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": 500
        }
        
        logging.info(f"Sending request to LLM: {json.dumps(data, indent=2)}")
        
        response = requests.post(LOCAL_LLM_URL, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        logging.info(f"Received response from LLM: {json.dumps(result, indent=2)}")
        
        # Extract the generated text from the response
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        else:
            error_msg = f"Unexpected response format: {result}"
            logging.error(error_msg)
            return error_msg
            
    except requests.exceptions.RequestException as e:
        error_msg = f"Error connecting to LLM server: {str(e)}"
        logging.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Error generating text: {str(e)}"
        logging.error(error_msg)
        return error_msg

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "styles": list(WRITING_STYLES.keys()),
        "default_model": DEFAULT_MODEL
    })

@app.post("/generate")
async def generate(
    topic: str = Form(...),
    style: str = Form("blog_intro"),
    temperature: float = Form(0.7),
    model: str = Form(DEFAULT_MODEL)
):
    if not topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty")
    
    # Get the prompt template based on style
    prompt_template = WRITING_STYLES.get(style, WRITING_STYLES["blog_intro"])
    prompt = prompt_template.format(topic=topic)
    
    # Generate the text
    output = generate_text(prompt, temperature, model)
    
    # Log the generation
    log_generation(topic, style, output, model)
    
    return {
        "output": output,
        "prompt": prompt,
        "model": model,
        "style": style
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

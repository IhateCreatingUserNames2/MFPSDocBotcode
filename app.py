from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import httpx
import os
import json


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
CODEBASE_FILE = "codebase.txt" 
MODEL = "google/gemini-2.0-flash-exp:free"  


with open(CODEBASE_FILE, 'r', encoding='utf-8') as f:
    CODEBASE_CONTENT = f.read()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message")
    
    prompt = f"""You are an expert technical assistant for MFPS 2.0 (Multiplayer First Person Shooter framework). Your purpose is to provide accurate, detailed answers about the codebase architecture, implementation patterns, and best practices.

## Developer Query

{user_message}

## Your Capabilities

You have comprehensive knowledge of:
- **Networking Architecture**: Client-server synchronization, packet optimization, interpolation/extrapolation, lag compensation, and networked entity management
- **Core Systems**: Player controllers, weapon systems, game modes, spawn management, UI frameworks, and loadout systems
- **Rendering Pipeline**: Multi-platform compatibility layers, performance optimization, and render-to-texture implementations
- **Integration Points**: Photon networking integration, database connectors, input systems, and third-party API interfaces
- **Development History**: 7+ years of framework evolution, architectural decisions, deprecated patterns, and migration strategies

## Response Guidelines

When answering the query above:

1. **Be Precise**: Reference specific classes, methods, and file locations when applicable
2. **Provide Context**: Explain not just "what" but "why" - include architectural reasoning and design trade-offs
3. **Code Examples**: Include relevant code snippets with explanations when helpful
4. **Best Practices**: Highlight recommended patterns and warn against common pitfalls
5. **Version Awareness**: Note if features or approaches differ across versions
6. **Performance Implications**: Mention networking, memory, or CPU considerations when relevant
7. **Cross-References**: Point to related systems or dependencies that may be affected

## MFPS 2.0 Codebase Reference

The complete codebase documentation is provided below. Search through this for relevant information to answer the developer's query:

{CODEBASE_CONTENT}

---

Please provide a comprehensive technical response to the developer's query above."""
    
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "http_referer": "https://mfpsdocs.onrender.com",
        "http_user_agent": "MFPS-2.0/1.0.0",
    }
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://mfpsdocs.onrender.com",
        "X-Title": "MFPS 2.0 Architecture Assistant",
        "OR-PROMPT-TRAINING": "allow"
    }
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                data=json.dumps(payload),
                headers=headers
            )
        
        output = response.json()
        print("🔍 OpenRouter raw response:", output)
        
        if 'choices' in output and output['choices']:
            return JSONResponse({"response": output['choices'][0]['message']['content']})
        else:
            return JSONResponse({"error": "Erro na resposta do modelo", "details": output}, status_code=500)
    except Exception as e:
        print(f"Error connecting to OpenRouter: {str(e)}")
        return JSONResponse({"error": "Erro ao conectar com OpenRouter", "details": str(e)}, status_code=500)

# MFPS DocBot 🤖

An documentation assistant for MFPS 2.0 (Multiplayer First Person Shooter framework). This chatbot provides technical answers about the codebase architecture, implementation patterns, and best practices by analyzing the complete Unity C# codebase.

** Use this at your Own Risk. It is running on OpenRouter Gemini Free Keys. This was made by a User of MFPS, not a developer from MFPS. It has nothing to do with Lovatto Studios.  ** 

** This project folder DOES NOT HAVE THE MFPS CODEBASE , you have to extract it by yourself. Use the Python Code CodeUNity.py to extract it from your MFPS Files. ** 


## Features

- 🔍 **Deep Codebase Analysis**: Loads 600k+ tokens of MFPS 2.0 source code
- 💬 **Interactive Chat Interface**: Web-based UI for easy interaction
- 🚀 **Powered by Gemini 2.0 Flash**: Fast, accurate responses via OpenRouter API
- 📚 **Context-Aware Responses**: References specific classes, methods, and file locations
- 🎯 **Technical Focus**: Answers about networking, rendering, game systems, and more

## Prerequisites

- Python 3.8+
- OpenRouter API key ([Get one here](https://openrouter.ai/))
- MFPS 2.0 Unity project

## Installation

### 1. Clone or Download the Repository

```bash
git clone <your-repo-url>
cd mfps-docbot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Generate the Codebase File

First, update the path in `codeUNITY.py` to point to your MFPS installation:

```python
source_directory = "E:\\UnityPROJECTSA\\Sloop\\Assets\\MFPS\\Scripts"
```

Then run the script to extract all C# files into a single text file:

```bash
python codeUNITY.py
```

This will create `UnityScriptsMFPS.txt` containing all MFPS scripts.

### 4. Rename Codebase File

Rename the generated file to match what the app expects:

```bash
# Windows
ren UnityScriptsMFPS.txt codebase.txt

# Linux/Mac
mv UnityScriptsMFPS.txt codebase.txt
```

### 5. Set Up Environment Variables

Create a `.env` file or set the environment variable:

**Option A: Using .env file**
```bash
echo OPENROUTER_API_KEY=your_api_key_here > .env
```

**Option B: Direct export (Linux/Mac)**
```bash
export OPENROUTER_API_KEY=your_api_key_here
```

**Option C: Direct set (Windows)**
```cmd
set OPENROUTER_API_KEY=your_api_key_here
```

## Running the Application

### Development Mode

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

The application will be available at:
- Local: `http://localhost:8000`
- Network: `http://your-ip:8000`

## Usage

1. Open your browser and navigate to `http://localhost:8000`
2. Type your technical question about MFPS 2.0 in the chat interface
3. Wait for the AI assistant to analyze the codebase and respond

### Example Questions

- "How does weapon synchronization work across the network?"
- "Show me the player spawn system implementation"
- "What's the best way to add a new game mode?"
- "Explain the damage calculation system"
- "How is lag compensation handled?"

## Project Structure

```
mfps-docbot/
├── app.py                      # FastAPI backend
├── codeUNITY.py               # Script to extract Unity C# files
├── requirements.txt           # Python dependencies
├── codebase.txt              # Generated MFPS codebase (you create this)
├── static/
│   └── index.html            # Chat interface UI
└── README.md                 # This file
```

## Configuration

### Changing the AI Model

Edit `app.py` and modify the `MODEL` variable:

```python
MODEL = "google/gemini-2.0-flash-exp:free"  # Current model
# Other options:
# MODEL = "anthropic/claude-3.5-sonnet"
# MODEL = "openai/gpt-4-turbo"
```

Check [OpenRouter Models](https://openrouter.ai/models) for available options.

### Adjusting Timeout

For large codebases, you may need to increase the timeout:

```python
async with httpx.AsyncClient(timeout=120.0) as client:  # Increase from 60s
```

### Customizing the Prompt

The system prompt is in `app.py` around line 30. Modify it to:
- Change response style
- Add specific guidelines
- Focus on particular aspects of MFPS

## Deployment

### Render.com

1. Create a new Web Service on Render
2. Connect your repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
5. Add environment variable: `OPENROUTER_API_KEY`
6. Upload `codebase.txt` as a static file

### Docker (Optional)

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t mfps-docbot .
docker run -p 8000:8000 -e OPENROUTER_API_KEY=your_key mfps-docbot
```

## Troubleshooting

### "File not found: codebase.txt"

Make sure you:
1. Ran `codeUNITY.py` successfully
2. Renamed `UnityScriptsMFPS.txt` to `codebase.txt`
3. The file is in the same directory as `app.py`

### "Error connecting to OpenRouter"

- Verify your API key is correct
- Check your internet connection
- Ensure you have credits on your OpenRouter account

### "Response timeout"

- Increase timeout in `app.py` (line with `httpx.AsyncClient`)
- Try a faster model (e.g., Gemini Flash instead of GPT-4)
- Consider reducing codebase size

### UI not loading

- Ensure `static/index.html` exists
- Check browser console for errors
- Verify port 8000 is not blocked by firewall

## Performance Tips

- **Large Codebase**: The 600k token codebase may take 5-15 seconds per query
- **Model Selection**: Gemini 2.0 Flash offers the best speed/quality balance
- **Caching**: Consider implementing response caching for common queries
- **RAG Optimization**: For production, implement semantic search to send only relevant code sections

## API Costs

Using Gemini 2.0 Flash (free tier):
- ~$0 per query (free tier available)
- Rate limits: Check OpenRouter documentation


# Local GitHub Repository Code Explainer

A local GenAI application that accepts **any public HTTPS GitHub repository URL**, analyzes the repository, sends the most relevant evidence to a locally running **Ollama / Qwen 2.5 3B** model, and displays a detailed beginner-friendly explanation in Streamlit.

## Assignment pipeline

**GitHub Repository → GitPython → Repository Analyzer → Smart LLM Context → Local Ollama/Qwen → FastAPI → Streamlit → Explanation**

The Streamlit entrypoint is intentionally at the project root:

```powershell
streamlit run app.py
```

This also makes deployment on Streamlit Community Cloud straightforward: select `app.py` as the main file.

## What the app supports

- Any public HTTPS GitHub repository
- Python, Java, JavaScript, TypeScript, C/C++, C#, Go, Rust, PHP, Ruby, Kotlin, Swift, Dart, R, MATLAB and other readable source files
- Jupyter notebooks (`.ipynb`) without executing them
- README and documentation-only repositories
- Configuration and dependency files
- Data/schema files
- Tests, deployment and CI/CD files
- HTML/CSS/markup
- Unknown but readable text files
- Binary/assets (classified and reported without sending binary content to the text model)
- Sensitive files are withheld from LLM context

## Local AI

Ollama is used for local inference with:

```text
qwen2.5:3b
```

The generated explanation is produced by the local model and is not hard-coded.

## Latency design

The complete repository is inventoried, but the model receives only the most relevant evidence. Large files are excerpted, duplicate context is avoided, binary content is skipped, and analysis runs as a background job with polling.

## Local setup

Create and activate a virtual environment, then install dependencies:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Make sure Ollama is installed and the model exists:

```powershell
ollama pull qwen2.5:3b
```

Start Ollama if needed:

```powershell
ollama serve
```

Start the FastAPI backend:

```powershell
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

In another terminal, run the Streamlit frontend:

```powershell
streamlit run app.py
```

## Streamlit Community Cloud

Use `app.py` as the Main file path.

Set the Streamlit secret:

```toml
BACKEND_URL = "https://YOUR-NGROK-URL"
```

The secret points Streamlit to the FastAPI backend. The local backend still needs to reach Ollama/Qwen on the backend machine.

For a demo tunnel:

```powershell
ngrok http 8000
```

Keep FastAPI, Ollama and ngrok running while the deployed frontend is being used.

## API

- `GET /`
- `GET /api/health`
- `POST /api/analyze`
- `GET /api/jobs/{job_id}`

## Tests

Run:

```powershell
pytest -q
```

Deployment notes are in `STREAMLIT_DEPLOYMENT.md` and `DEPLOYMENT_CHECKLIST.md`.

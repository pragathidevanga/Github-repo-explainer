# Streamlit Deployment

## Local run

From the project root:

```powershell
streamlit run app.py
```

The canonical Streamlit entrypoint is **`app.py`** at the project root.

## Streamlit Community Cloud

Use:

- Repository: `pragathidevanga/github-code-explainer` (or your own repository containing these files)
- Branch: `main`
- Main file path: `app.py`
- Python: 3.12

Set this Streamlit secret:

```toml
BACKEND_URL = "https://YOUR-NGROK-URL"
```

The deployed Streamlit frontend calls the configured FastAPI backend. For the local-LLM assignment, FastAPI and Ollama/Qwen remain on the machine running the local backend. The backend machine must stay online while the deployed frontend is being used.

## Local backend

```powershell
.\.venv\Scripts\Activate.ps1
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

Then expose port 8000 with ngrok:

```powershell
ngrok http 8000
```

Put the resulting public HTTPS URL into Streamlit Cloud's `BACKEND_URL` secret.

## Security

Do not commit `.streamlit/secrets.toml`, `.env`, API tokens, ngrok credentials, or model files.

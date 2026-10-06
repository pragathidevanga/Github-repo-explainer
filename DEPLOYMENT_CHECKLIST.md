# Deployment Checklist

## Local machine

- [ ] Python virtual environment created
- [ ] `pip install -r requirements.txt` completed
- [ ] Ollama installed
- [ ] `qwen2.5:3b` pulled
- [ ] Ollama reachable at `http://127.0.0.1:11434`
- [ ] FastAPI running at `http://127.0.0.1:8000`
- [ ] `GET /` returns HTTP 200
- [ ] `GET /api/health` reports Ollama available
- [ ] Streamlit starts
- [ ] A public GitHub source repo works
- [ ] A different person's public repo works
- [ ] A docs-only repo works

## Streamlit Cloud + ngrok demo

- [ ] FastAPI is running with `--host 0.0.0.0 --port 8000`
- [ ] ngrok is forwarding port 8000
- [ ] Public `/` endpoint returns HTTP 200
- [ ] Streamlit Cloud secret contains the current `BACKEND_URL`
- [ ] Streamlit app can start a job and poll its status
- [ ] Ollama and FastAPI remain running on the laptop during the demo
- [ ] Stop the tunnel after the demo

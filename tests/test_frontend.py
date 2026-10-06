from pathlib import Path


def test_frontend_contains_required_pipeline() -> None:
    text = Path("frontend/app.py").read_text(encoding="utf-8")
    for marker in ["BACKEND_URL", "/api/analyze", "/api/jobs/", "Ollama", "Qwen 2.5 3B", "Streamlit"]:
        assert marker in text

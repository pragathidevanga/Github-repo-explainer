from pathlib import Path


def test_root_streamlit_entrypoint_exists() -> None:
    text = Path("app.py").read_text(encoding="utf-8")
    assert "from frontend.app import main" in text
    assert 'if __name__ == "__main__":' in text
    assert "main()" in text


def test_run_script_uses_root_app() -> None:
    text = Path("run_app.bat").read_text(encoding="utf-8")
    assert "streamlit run app.py" in text

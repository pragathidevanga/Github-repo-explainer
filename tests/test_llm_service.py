from backend.llm_service import build_prompt


def test_prompt_is_evidence_based() -> None:
    report = {
        "counts": {"total_files": 2},
        "languages": {"Python": 1},
        "technologies": ["Python"],
        "folder_tree": ["README.md", "main.py"],
        "file_summaries": [
            {"path": "README.md", "category": "documentation", "language": None, "summary": "A demo"},
            {"path": "main.py", "category": "source", "language": "Python", "summary": "print(1)"},
        ],
    }
    prompt = build_prompt(owner="a", repo_name="b", url="https://github.com/a/b", report=report, context_blocks=["### FILE: main.py\nprint(1)"])
    assert "Do not invent technologies" in prompt
    assert "## Project Overview" in prompt
    assert "main.py" in prompt

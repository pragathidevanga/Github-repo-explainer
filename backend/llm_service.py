from __future__ import annotations

import os
from typing import Iterable

import requests


class OllamaService:
    def __init__(self) -> None:
        self.base_url = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
        self.model = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")
        self.timeout = int(os.getenv("OLLAMA_TIMEOUT_SECONDS", "240"))

    def health(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            response.raise_for_status()
            return True
        except requests.RequestException:
            return False

    def generate(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "num_ctx": 16384,
            },
        }
        response = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()
        text = data.get("response", "").strip()
        if not text:
            raise RuntimeError("Ollama returned an empty explanation.")
        return text


def build_prompt(*, owner: str, repo_name: str, url: str, report: dict, context_blocks: Iterable[str]) -> str:
    file_lines = "\n".join(
        f"- {item['path']} | {item['category']} | {item.get('language') or 'unknown'} | {item['summary']}"
        for item in report["file_summaries"][:120]
    )
    tree = "\n".join(report["folder_tree"][:180])
    context = "\n\n".join(context_blocks)
    return f"""You are a repository code explainer for a beginner. Analyze ONLY the supplied evidence.
Do not invent technologies, files, databases, APIs, framework behavior, or commands. If evidence is insufficient, say so.
The repository is public and may contain any programming language or file type. Binary files are metadata only.

Repository: {owner}/{repo_name}
URL: {url}
Counts: {report['counts']}
Languages: {report['languages']}
Detected technologies (evidence-based): {report['technologies']}

FOLDER TREE:
{tree}

FILE INVENTORY:
{file_lines}

SELECTED FILE CONTENT:
{context}

Write a simple-language but technically useful explanation with exactly these headings:
## Project Overview
## Main Features / Purpose
## Main Technologies
## Repository Structure
## How It Works
## Important Files and Components
## Data Flow
## Configuration and Dependencies
## How to Run (only when supported by evidence)
## Limitations / Notes

Do not claim that a feature exists unless the supplied evidence supports it. Mention when a file was truncated or when the repository is primarily documentation/configuration/data rather than conventional source code."""

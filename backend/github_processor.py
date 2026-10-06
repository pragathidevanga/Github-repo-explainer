from __future__ import annotations

import os
import shutil
from pathlib import Path
from urllib.parse import urlparse

try:
    from git import Repo
except ImportError:  # pragma: no cover - dependency is installed from requirements.txt in deployment
    Repo = None

from .utils import safe_job_id


class GitHubProcessor:
    def __init__(self, root: Path):
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def validate_url(url: str) -> tuple[str, str, str]:
        parsed = urlparse(url.strip())
        if parsed.scheme != "https" or parsed.netloc.lower() != "github.com":
            raise ValueError("Please provide a public HTTPS GitHub repository URL.")
        parts = [p for p in parsed.path.strip("/").split("/") if p]
        if len(parts) < 2:
            raise ValueError("GitHub URL must look like https://github.com/owner/repository")
        owner, repo = parts[0], parts[1]
        repo = repo.removesuffix(".git")
        if not owner or not repo:
            raise ValueError("Invalid GitHub repository URL.")
        clean_url = f"https://github.com/{owner}/{repo}.git"
        return owner, repo, clean_url

    def clone(self, url: str) -> tuple[Path, str, str, str]:
        owner, repo_name, clone_url = self.validate_url(url)
        destination = self.root / safe_job_id()
        os.environ.setdefault("GIT_TERMINAL_PROMPT", "0")
        if Repo is None:
            raise RuntimeError("GitPython is not installed. Run: python -m pip install -r requirements.txt")
        try:
            repo = Repo.clone_from(
                clone_url,
                destination,
                depth=1,
                single_branch=True,
                no_checkout=False,
            )
            branch = repo.active_branch.name if not repo.head.is_detached else None
            return destination, owner, repo_name, branch or "unknown"
        except Exception:
            shutil.rmtree(destination, ignore_errors=True)
            raise

    @staticmethod
    def cleanup(path: Path) -> None:
        shutil.rmtree(path, ignore_errors=True)

"""
Upload DragonGuide to a Hugging Face Space (Streamlit).

Set environment variable HF_TOKEN (write token from https://huggingface.co/settings/tokens)
Optional: HF_SPACE_REPO = "your-username/dragonguide"

Usage:
    set HF_TOKEN=hf_...
    set HF_SPACE_REPO=YourUsername/dragonguide
    python deploy_hf.py
"""

import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent
EXCLUDE = {".env", "venv", ".venv", "__pycache__", ".git", "deploy_hf.py", "deploy.zip"}

README_SPACE = """---
title: DragonGuide
emoji: 🐉
colorFrom: '#07294D'
colorTo: '#FFC600'
sdk: streamlit
sdk_version: 1.45.1
app_file: main.py
pinned: true
license: mit
---

# DragonGuide

AI academic navigator for Drexel University — RAG over official policy documents.

**Set Space secret:** `OPENAI_API_KEY`
"""


def main():
    token = os.getenv("HF_TOKEN")
    repo_id = os.getenv("HF_SPACE_REPO", "").strip()
    if not token:
        print("HF_TOKEN not set. Get a token at https://huggingface.co/settings/tokens")
        sys.exit(1)
    if not repo_id or "/" not in repo_id:
        print("Set HF_SPACE_REPO=YourUsername/dragonguide")
        sys.exit(1)

    try:
        from huggingface_hub import HfApi, upload_folder
    except ImportError:
        print("Install: pip install huggingface_hub")
        sys.exit(1)

    api = HfApi(token=token)
    print(f"Creating Space {repo_id} …")
    try:
        api.create_repo(
            repo_id=repo_id.split("/", 1)[1],
            repo_type="space",
            space_sdk="streamlit",
            private=False,
            exist_ok=True,
        )
    except Exception as exc:
        print(f"  (repo note: {exc})")

    readme_path = ROOT / "README.md"
    backup = None
    if readme_path.exists():
        backup = readme_path.read_text(encoding="utf-8")
    readme_path.write_text(README_SPACE, encoding="utf-8")

    print("Uploading files …")
    upload_folder(
        folder_path=str(ROOT),
        repo_id=repo_id,
        repo_type="space",
        token=token,
        ignore_patterns=list(EXCLUDE) + ["*.pyc", "agent-tools/*"],
    )

    if backup is not None:
        readme_path.write_text(backup, encoding="utf-8")

    slug = repo_id.replace("/", "-")
    url = f"https://huggingface.co/spaces/{repo_id}"
    app_url = f"https://{slug}.hf.space"
    print(f"\nSpace: {url}")
    print(f"App (after build): {app_url}")
    print("\nIn Space Settings → Repository secrets, add OPENAI_API_KEY")


if __name__ == "__main__":
    main()

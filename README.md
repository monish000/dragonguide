# 🐉 DragonGuide

**AI-Powered Semantic Navigator for Drexel University Registration & Academic Policies**  
CS-591 Capstone · Spring 2026

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://dragonguide.streamlit.app)
[![Open in Spaces](https://huggingface.co/datasets/huggingface/badges/raw/main/open-in-hf-spaces-sm.svg)](https://huggingface.co/spaces/monish000/dragonguide)

## Live demo

| Platform | URL |
|----------|-----|
| **Streamlit Cloud** | **https://dragonguide.streamlit.app** |
| Hugging Face Space | https://huggingface.co/spaces/monish000/dragonguide |

> After first deploy, add `OPENAI_API_KEY` in the host’s **Secrets** settings (see below).

---

## Deploy in 2 minutes (Streamlit Cloud)

1. Open **[share.streamlit.io](https://share.streamlit.io)** → Sign in with GitHub.
2. **Create app** → Repository: `monish000/dragonguide` · Branch: `main` · Main file: `main.py`
3. **App URL:** `dragonguide` → Deploy.
4. **Secrets** (⚙️):
   ```toml
   OPENAI_API_KEY = "sk-..."
   ```
5. Open **https://dragonguide.streamlit.app**

---

## Local run

```powershell
cd DragonGuide
setup.bat
launch.bat
```

---

## Stack

GPT-4o · FAISS · LangChain · Streamlit · 14 official Drexel documents

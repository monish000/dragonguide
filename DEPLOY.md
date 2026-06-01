# Deploy DragonGuide (public URL)

## Target URLs

| Platform | URL you want |
|----------|----------------|
| **Streamlit Cloud** (recommended) | `https://dragonguide.streamlit.app` |
| **Hugging Face Space** | `https://YOUR_USERNAME-dragonguide.hf.space` |

A custom domain like `dragonguide.com` requires buying a domain and DNS setup (not included here).

---

## Option A — Streamlit Cloud → `dragonguide.streamlit.app`

1. **Install Git** from https://git-scm.com/download/win and restart your terminal.

2. **Create a GitHub repo** named `DragonGuide` (public).

3. Push this folder:
   ```powershell
   cd "C:\Users\Monish Barot\Documents\Drexel\SpringQuater2026\CS591\DragonGuide"
   git init
   git add main.py brain.py config.py ui_theme.py ingest.py download_docs.py requirements.txt packages.txt .streamlit data vectorstore .gitignore README.md DEPLOY.md
   git commit -m "DragonGuide MVP for Streamlit Cloud"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/DragonGuide.git
   git push -u origin main
   ```

4. Go to **https://share.streamlit.io** → Sign in with GitHub → **Create app**.

5. Settings:
   - Repository: `YOUR_USERNAME/DragonGuide`
   - Branch: `main`
   - Main file: `main.py`
   - **App URL (subdomain):** `dragonguide`

6. **Secrets** (⚙️ → Secrets):
   ```toml
   OPENAI_API_KEY = "sk-your-key-here"
   ```

7. Click **Deploy**. Live app: **https://dragonguide.streamlit.app**

---

## Option B — Hugging Face Space

1. Create token: https://huggingface.co/settings/tokens (Write access).

2. ```powershell
   cd "C:\Users\Monish Barot\Documents\Drexel\SpringQuater2026\CS591\DragonGuide"
   venv\Scripts\activate
   pip install huggingface_hub
   set HF_TOKEN=hf_your_token
   set HF_SPACE_REPO=YourUsername/dragonguide
   python deploy_hf.py
   ```

3. Space → **Settings → Repository secrets** → `OPENAI_API_KEY`

4. Open: `https://YourUsername-dragonguide.hf.space`

---

## What is deployed

- Pre-built `vectorstore/` (no ingest needed on first boot)
- 14 Drexel policy documents in `data/`
- GPT-4o + FAISS RAG pipeline

**Never commit `.env`** — use platform secrets only.

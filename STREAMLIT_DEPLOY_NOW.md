# Deploy DragonGuide now (2 minutes)

Your code is live on GitHub: **https://github.com/monish000/dragonguide**

## Get https://dragonguide.streamlit.app

1. Open **https://share.streamlit.io** and sign in with **GitHub** (account `monish000`).

2. Click **Create app**.

3. Fill in:
   - **Repository:** `monish000/dragonguide`
   - **Branch:** `main`
   - **Main file path:** `main.py`
   - **App URL (subdomain):** `dragonguide`

4. Click **Advanced settings** → **Secrets** and paste:

   ```toml
   OPENAI_API_KEY = "sk-your-openai-key-here"
   ```

5. Click **Deploy**.

6. Wait ~2–3 minutes. Your app will be at:

   ## **https://dragonguide.streamlit.app**

---

## Optional: Hugging Face (auto-deploy from GitHub)

1. Create a token: https://huggingface.co/settings/tokens (Write)
2. Add GitHub secret: https://github.com/monish000/dragonguide/settings/secrets/actions  
   Name: `HF_TOKEN` · Value: your HF token
3. Run workflow: https://github.com/monish000/dragonguide/actions → **Deploy to Hugging Face Space** → **Run workflow**
4. Add Space secret: https://huggingface.co/spaces/monish000/dragonguide/settings → `OPENAI_API_KEY`
5. App URL: **https://monish000-dragonguide.hf.space**

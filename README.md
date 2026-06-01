# 🐉 DragonGuide
### AI-Powered Semantic Navigator for Drexel University Registration & Academic Policies
**CS-591 Capstone | Spring Quarter 2026 | Q1 MVP**

---

## Overview

DragonGuide is a **Retrieval-Augmented Generation (RAG)** AI assistant grounded exclusively in official Drexel University documents. It uses OpenAI embeddings + FAISS vector search + GPT-4o to answer student questions with zero hallucination.

---

## Project Structure

```
DragonGuide/
├── data/                          ← Knowledge base documents (pre-loaded)
│   ├── Drexel_Academic_Calendar_2025-2026.txt
│   ├── Drexel_Registration_Guide.txt
│   ├── Drexel_Registration_Holds_and_Restrictions.txt
│   ├── Drexel_Course_Withdrawal_Policy.txt
│   ├── Drexel_Enrollment_Policies.txt
│   ├── Drexel_Graduation_and_Degree_Application.txt
│   ├── Drexel_Satisfactory_Academic_Progress.txt
│   ├── Drexel_Grading_Scale_and_Academic_Standing.txt
│   └── Drexel_Academic_Policies_Index.txt
├── vectorstore/                   ← Auto-generated FAISS index (after ingest)
├── .env                           ← Your OpenAI API key (edit this!)
├── requirements.txt               ← Python dependencies
├── ingest.py                      ← Document → embeddings → FAISS pipeline
├── brain.py                       ← DragonBrain RAG class (GPT-4o + retriever)
├── main.py                        ← Streamlit chat UI
├── setup.bat                      ← One-click setup (Windows)
└── launch.bat                     ← One-click launch (Windows)
```

---

## Quick Start (3 Steps)

### Step 1 — Add Your OpenAI API Key
Edit `.env`:
```
OPENAI_API_KEY=sk-...your-key-here...
```
Get your key at: https://platform.openai.com/api-keys

### Step 2 — Run Setup (first time only)
```bat
setup.bat
```
This will:
- Create a Python virtual environment
- Install all dependencies
- Run the ingestion pipeline

### Step 3 — Launch the App
```bat
launch.bat
```
Or manually:
```bash
venv\Scripts\activate
streamlit run main.py
```

---

## Manual Setup (PowerShell)

```powershell
# Navigate to project folder
cd "C:\Users\Monish Barot\Documents\Drexel\SpringQuater2026\CS591\DragonGuide"

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Edit .env with your OpenAI API key
# (Open .env in any text editor)

# Build the vector index from documents in data/
python ingest.py

# Launch the app
streamlit run main.py
```

App opens automatically at: **http://localhost:8501**

---

## Knowledge Base — Pre-Loaded Documents

| Document | Coverage |
|---|---|
| `Drexel_Academic_Calendar_2025-2026.txt` | All quarter dates: add/drop, withdraw, finals, holidays (Fall/Winter/Spring/Summer 2025–26) |
| `Drexel_Registration_Guide.txt` | Registration process, time tickets, instructional methods, Schedule Ahead |
| `Drexel_Registration_Holds_and_Restrictions.txt` | All registration error types and how to resolve them |
| `Drexel_Course_Withdrawal_Policy.txt` | Withdrawal windows, implications, electronic process, exceptions |
| `Drexel_Enrollment_Policies.txt` | Enrollment status, credit loads, leave of absence, university withdrawal |
| `Drexel_Graduation_and_Degree_Application.txt` | Degree application deadlines, steps, diploma details, commencement |
| `Drexel_Satisfactory_Academic_Progress.txt` | SAP policy, GPA/completion requirements, appeal process |
| `Drexel_Grading_Scale_and_Academic_Standing.txt` | Grading scale, GPA calculation, INC grades, academic standing |
| `Drexel_Academic_Policies_Index.txt` | Comprehensive index of all Provost policies with descriptions |

---

## Adding More Documents

To expand the knowledge base:
1. Drop additional PDF or TXT files into the `data/` folder
2. Re-run: `python ingest.py`
3. Restart the app

---

## Architecture

```
User Question
     │
     ▼
Streamlit UI (main.py)
     │
     ▼
DragonBrain.ask() (brain.py)
     │
     ├── FAISS Vector Search (vectorstore/)
     │        └── Top-6 most relevant document chunks (MMR)
     │
     └── GPT-4o (gpt-4o, temp=0)
              └── Synthesizes answer from chunks only
                       │
                       ▼
              Answer + Source Citations
```

---

## Technology Stack

| Component | Technology |
|---|---|
| Language Model | OpenAI GPT-4o |
| Embeddings | OpenAI text-embedding-3-small |
| Vector Store | FAISS (CPU) |
| RAG Framework | LangChain |
| UI | Streamlit |
| Document Loading | LangChain PyPDFLoader + TextLoader |

---

## Sources

All documents sourced from official Drexel University websites:
- Office of the Provost: drexel.edu/provost
- Drexel Central: drexel.edu/drexelcentral
- University Registrar: drexel.edu/registrar

---

*DragonGuide v1.0 — CS-591 Capstone, Drexel University, Spring 2026*

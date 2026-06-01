"""
main.py — DragonGuide Streamlit Application
"""

from pathlib import Path

import streamlit as st

from brain import DragonBrain
from ui_theme import inject_css

st.set_page_config(
    page_title="DragonGuide — Drexel AI Advisor",
    page_icon="🐉",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

DATA_DIR = Path(__file__).parent / "data"

SAMPLE_QUESTIONS = [
    "What is the add/drop deadline for Spring 2026?",
    "How do I clear a registration hold?",
    "What is the last day to withdraw from a course in Spring 2026?",
    "What is Satisfactory Academic Progress (SAP)?",
    "How do I apply for graduation?",
    "What are the MS graduate credit requirements?",
]


@st.cache_resource(show_spinner="Loading DragonGuide knowledge base…")
def get_brain() -> DragonBrain:
    brain = DragonBrain()
    brain.load()
    return brain


def count_docs() -> int:
    if not DATA_DIR.exists():
        return 0
    return len(list(DATA_DIR.glob("*.pdf"))) + len(list(DATA_DIR.glob("*.txt")))


def render_sources(sources: list) -> None:
    if not sources:
        return
    with st.expander(f"📚 Sources ({len(sources)})", expanded=False):
        for s in sources:
            st.markdown(
                f'<div class="dg-src"><strong>📄 {s["source"]}</strong> · Page {s["page"]}'
                f'<em>"{s["snippet"]}…"</em></div>',
                unsafe_allow_html=True,
            )


if "messages" not in st.session_state:
    st.session_state.messages = []

from config import get_openai_api_key

if not get_openai_api_key():
    st.error(
        "OpenAI API key missing. Add `OPENAI_API_KEY` to `.env` locally or to "
        "Streamlit / Hugging Face secrets when deployed."
    )
    st.stop()

brain = get_brain()
doc_count = count_docs()
index_ready = brain.is_loaded

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div class="dg-logo-wrap">
          <div class="dg-logo-ring">🐉</div>
          <div class="dg-logo-name">DragonGuide</div>
          <div class="dg-logo-sub">Drexel University · Academic AI</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    pill = "dg-pill-ok" if index_ready else "dg-pill-err"
    label = "Knowledge Base Online" if index_ready else "Knowledge Base Offline"
    st.markdown(f'<span class="dg-pill {pill}">● {label}</span>', unsafe_allow_html=True)

    if not index_ready:
        st.caption("Run: python ingest.py")

    st.markdown(
        f"""
        <div class="dg-stat-grid">
          <div class="dg-stat"><div class="dg-stat-num">{doc_count}</div><div class="dg-stat-lbl">Documents</div></div>
          <div class="dg-stat"><div class="dg-stat-num">172</div><div class="dg-stat-lbl">Index Chunks</div></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("🗑️ Clear Chat", type="primary", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pop("pending_question", None)
        st.rerun()

    st.markdown("**Quick questions**")
    for i, q in enumerate(SAMPLE_QUESTIONS):
        if st.button(q, key=f"qq_{i}", use_container_width=True):
            st.session_state.pending_question = q
            st.rerun()

    st.caption("CS-591 Capstone · Official Drexel sources only")

# ── Main ──────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div class="dg-hero">
      <h1>DragonGuide</h1>
      <p>AI academic navigator for Drexel registration, deadlines, holds, and policy — grounded in official university documents.</p>
      <div class="dg-badges">
        <span class="dg-badge">RAG · Source-Grounded</span>
        <span class="dg-badge">GPT-4o</span>
        <span class="dg-badge">FAISS Search</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

if not st.session_state.messages:
    with st.chat_message("assistant", avatar="🐉"):
        st.markdown(
            """
**Welcome!** Ask about registration windows, add/drop dates, withdrawals, holds,
SAP, graduation, or catalog policies.

Use a **quick question** in the sidebar or type below. Every answer includes **source citations**.
            """
        )

for msg in st.session_state.messages:
    avatar = "🐉" if msg["role"] == "assistant" else "🧑‍🎓"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            render_sources(msg.get("sources", []))


def handle_question(prompt: str) -> None:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🐉"):
        if not brain.is_loaded:
            answer = "Knowledge base offline. Run `python ingest.py` and refresh."
            sources = []
            st.error(answer)
        else:
            with st.spinner("Searching official Drexel documents…"):
                result = brain.ask(prompt)
            answer = result["answer"]
            sources = result["sources"]
            st.markdown(answer)
            render_sources(sources)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "sources": sources}
    )


pending = st.session_state.pop("pending_question", None)
if pending:
    handle_question(pending)
elif prompt := st.chat_input("Ask about registration, deadlines, holds, or academic policy…"):
    handle_question(prompt)

st.markdown(
    '<p class="dg-footer">DragonGuide uses indexed Drexel documents only. '
    "Verify critical decisions with Drexel Central or your academic advisor.</p>",
    unsafe_allow_html=True,
)

"""Inject DragonGuide global CSS safely (Streamlit-compatible)."""

import streamlit as st

NAVY = "#07294D"
NAVY_SOFT = "#1a3d5c"
GOLD = "#FFC600"
GOLD_SOFT = "#e6b800"
BG_MAIN = "#f7f9fc"
BG_CARD = "#ffffff"
TEXT_MUTED = "#5c6b7a"
BORDER_SOFT = "#dde4ec"


def inject_css() -> None:
    """Apply styles via markdown (compatible with all Streamlit 1.x versions)."""
    css = f"""
    #MainMenu, footer, header[data-testid="stHeader"] {{
        visibility: hidden !important;
        height: 0 !important;
    }}

    .stApp {{
        background-color: {BG_MAIN};
        font-family: 'Segoe UI', system-ui, sans-serif;
        color: {NAVY};
    }}

    .main .block-container {{
        padding-top: 1.25rem;
        max-width: 860px;
    }}

    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {NAVY} 0%, {NAVY_SOFT} 100%) !important;
        border-right: 2px solid {GOLD_SOFT};
    }}

    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown strong,
    [data-testid="stSidebar"] label {{
        color: rgba(255, 255, 255, 0.9) !important;
    }}

    [data-testid="stSidebar"] .stCaption {{
        color: rgba(255, 255, 255, 0.55) !important;
    }}

    [data-testid="stSidebar"] div[data-testid="stButton"] > button {{
        background-color: rgba(255, 198, 0, 0.92) !important;
        color: {NAVY} !important;
        border: 1px solid {GOLD_SOFT} !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.8rem !important;
        text-align: left !important;
        padding: 0.5rem 0.7rem !important;
        line-height: 1.35 !important;
    }}

    [data-testid="stSidebar"] div[data-testid="stButton"] > button:hover {{
        background-color: #ffe082 !important;
        color: {NAVY} !important;
    }}

    [data-testid="stSidebar"] div[data-testid="stButton"]:has(button[kind="primary"]) > button {{
        background-color: rgba(255,255,255,0.1) !important;
        color: #fff !important;
        border: 1px solid rgba(255,255,255,0.35) !important;
        text-align: center !important;
    }}

    [data-testid="stSidebar"] div[data-testid="stButton"]:has(button[kind="primary"]) > button:hover {{
        background-color: rgba(255,255,255,0.2) !important;
    }}

    .dg-logo-wrap {{
        text-align: center;
        padding: 1rem 0 0.85rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.15);
        margin-bottom: 0.65rem;
    }}
    .dg-logo-ring {{
        width: 56px; height: 56px; margin: 0 auto 0.45rem;
        border-radius: 50%; border: 2px solid {GOLD};
        display: flex; align-items: center; justify-content: center;
        font-size: 1.75rem; background: rgba(255, 198, 0, 0.08);
    }}
    .dg-logo-name {{
        font-size: 1.45rem; font-weight: 700; color: {GOLD} !important;
    }}
    .dg-logo-sub {{
        font-size: 0.65rem; color: rgba(255,255,255,0.6) !important;
        letter-spacing: 0.06em; margin-top: 0.2rem;
    }}

    .dg-pill {{
        display: block; text-align: center; padding: 0.35rem 0.65rem;
        border-radius: 8px; font-size: 0.76rem; font-weight: 600;
        margin-bottom: 0.65rem;
    }}
    .dg-pill-ok {{
        background: rgba(255,255,255,0.12); color: #b8e6c8 !important;
        border: 1px solid rgba(255,255,255,0.2);
    }}
    .dg-pill-err {{
        background: rgba(255,255,255,0.08); color: #f0c4c4 !important;
        border: 1px solid rgba(255,255,255,0.15);
    }}

    .dg-stat-grid {{
        display: grid; grid-template-columns: 1fr 1fr; gap: 0.45rem;
        margin: 0.45rem 0 0.85rem;
    }}
    .dg-stat {{
        background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.12);
        border-radius: 8px; padding: 0.45rem; text-align: center;
    }}
    .dg-stat-num {{ font-size: 1.1rem; font-weight: 700; color: {GOLD} !important; }}
    .dg-stat-lbl {{
        font-size: 0.6rem; color: rgba(255,255,255,0.55) !important;
        text-transform: uppercase;
    }}

    .dg-hero {{
        background: {NAVY};
        border-radius: 12px; padding: 1.35rem 1.5rem; margin-bottom: 1rem;
        border-left: 4px solid {GOLD};
    }}
    .dg-hero h1 {{
        color: {GOLD} !important; font-size: 1.65rem; font-weight: 700; margin: 0;
    }}
    .dg-hero p {{
        color: rgba(255,255,255,0.85) !important; margin: 0.4rem 0 0;
        font-size: 0.9rem; line-height: 1.5;
    }}
    .dg-badges {{ margin-top: 0.65rem; display: flex; flex-wrap: wrap; gap: 0.35rem; }}
    .dg-badge {{
        background: rgba(255,255,255,0.1); color: rgba(255,255,255,0.85) !important;
        font-size: 0.65rem; padding: 0.15rem 0.5rem; border-radius: 6px;
    }}

    [data-testid="stChatMessage"] {{
        background: {BG_CARD} !important;
        border-radius: 10px !important;
        border: 1px solid {BORDER_SOFT} !important;
        box-shadow: none !important;
        margin-bottom: 0.5rem !important;
    }}

    [data-testid="stChatInput"] > div {{
        border: 1px solid {BORDER_SOFT} !important;
        border-radius: 10px !important;
        background: {BG_CARD} !important;
    }}

    [data-testid="stChatInput"]:focus-within > div {{
        border-color: {GOLD_SOFT} !important;
        box-shadow: none !important;
    }}

    .dg-src {{
        background: {BG_MAIN}; border-left: 3px solid {GOLD_SOFT};
        border-radius: 6px; padding: 0.55rem 0.75rem; margin-bottom: 0.4rem;
        font-size: 0.83rem; color: {TEXT_MUTED};
    }}
    .dg-src strong {{ color: {NAVY}; }}
    .dg-src em {{
        color: {TEXT_MUTED}; display: block; margin-top: 0.2rem;
        font-size: 0.78rem; font-style: normal;
    }}

    .dg-footer {{
        text-align: center; color: {TEXT_MUTED}; font-size: 0.7rem;
        margin: 1.25rem 0 0.5rem;
    }}

    [data-testid="stExpander"] {{
        background: {BG_CARD};
        border: 1px solid {BORDER_SOFT};
        border-radius: 8px;
    }}
    """

    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

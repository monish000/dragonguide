"""Shared config — API keys from Streamlit secrets or environment."""

import os

from dotenv import load_dotenv

load_dotenv()


def get_openai_api_key() -> str | None:
    key = os.getenv("OPENAI_API_KEY")
    if key and not key.startswith("your_"):
        return key
    try:
        import streamlit as st

        if "OPENAI_API_KEY" in st.secrets:
            return st.secrets["OPENAI_API_KEY"]
    except Exception:
        pass
    return None

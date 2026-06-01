"""
ingest.py — DragonGuide Data Ingestion Pipeline

Loads Drexel documents (PDF and TXT) from data/, splits into overlapping
chunks, embeds via OpenAI text-embedding-3-small, and persists a FAISS
vector index to vectorstore/.

Usage:
    python ingest.py
"""

import os
import glob
import sys
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from config import get_openai_api_key

BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
DATA_DIR        = os.path.join(BASE_DIR, "data")
VECTORSTORE_DIR = os.path.join(BASE_DIR, "vectorstore")
CHUNK_SIZE      = 1000
CHUNK_OVERLAP   = 200


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def load_documents(data_dir: str) -> list:
    """Recursively load all PDF and TXT files from data_dir."""
    pdf_paths = sorted(glob.glob(os.path.join(data_dir, "**", "*.pdf"), recursive=True))
    txt_paths = sorted(glob.glob(os.path.join(data_dir, "**", "*.txt"), recursive=True))
    all_paths = pdf_paths + txt_paths

    if not all_paths:
        print(f"\n[ERROR] No PDF or TXT files found in '{data_dir}'.")
        print("  → Add Drexel catalog / policy documents to the data/ folder.")
        sys.exit(1)

    documents = []
    for path in all_paths:
        filename = os.path.basename(path)
        ext      = os.path.splitext(path)[1].lower()
        try:
            if ext == ".pdf":
                loader = PyPDFLoader(path)
            else:
                loader = TextLoader(path, encoding="utf-8")
            pages = loader.load()
            documents.extend(pages)
            print(f"  ✔  {filename:60s}  ({len(pages)} chunk(s))")
        except Exception as exc:
            print(f"  ✘  {filename} — skipped ({exc})")

    print(f"\n  Loaded {len(documents)} section(s) from {len(all_paths)} file(s).")
    return documents


def split_documents(documents: list) -> list:
    """Split documents into overlapping chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(documents)
    print(f"  Created {len(chunks):,} chunk(s)  "
          f"(size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP})")
    return chunks


def build_vectorstore(chunks: list) -> None:
    """Embed chunks and save FAISS index."""
    print("\n  Generating embeddings via OpenAI (text-embedding-3-small) …")
    api_key = get_openai_api_key()
    if not api_key:
        print("\n[ERROR] OPENAI_API_KEY not set. Add it to .env or Streamlit secrets.")
        sys.exit(1)
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=api_key)
    vectorstore = FAISS.from_documents(chunks, embeddings)

    os.makedirs(VECTORSTORE_DIR, exist_ok=True)
    vectorstore.save_local(VECTORSTORE_DIR)
    print(f"  FAISS index saved → {VECTORSTORE_DIR}")


# ─────────────────────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────────────────────

def main():
    sep = "═" * 60
    print(f"\n{sep}")
    print("  DragonGuide  |  Ingestion Pipeline")
    print(f"{sep}\n")

    print(f"[1/3] Scanning '{DATA_DIR}' for PDF and TXT files …")
    documents = load_documents(DATA_DIR)

    print("\n[2/3] Splitting documents into chunks …")
    chunks = split_documents(documents)

    print("\n[3/3] Building vector index …")
    build_vectorstore(chunks)

    print(f"\n{sep}")
    print("  Ingestion complete!  Run:  streamlit run main.py")
    print(f"{sep}\n")


if __name__ == "__main__":
    main()

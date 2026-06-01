"""
brain.py — DragonGuide AI Core

DragonBrain wraps a FAISS retriever + GPT-4o into a RetrievalQA chain
with a strict Drexel-branded system prompt. Designed for zero hallucination:
the LLM is instructed to answer ONLY from the retrieved context.
"""

import os

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

from config import get_openai_api_key

BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
VECTORSTORE_DIR = os.path.join(BASE_DIR, "vectorstore")

# ─────────────────────────────────────────────────────────────
# System Prompt
# ─────────────────────────────────────────────────────────────
_PROMPT_TEMPLATE = """\
You are DragonGuide, an elite Drexel University Academic Assistant. \
Your mission is to help students navigate course registration, academic \
deadlines, prerequisite requirements, and university policies with precision.

STRICT RULES:
1. ONLY use the provided context excerpts to answer. Do NOT use any outside \
knowledge or make assumptions.
2. If the answer is not explicitly found in the context, respond with:
   "I'm sorry, I don't have that specific information in my current database. \
Please contact Drexel Central at drexel.edu/drexelcentral or your academic \
advisor for assistance."
3. Always cite the exact document name (e.g., "According to the \
Drexel_Undergraduate_Catalog_2025-26.pdf…") and, when available, the page number.
4. Be concise, professional, and student-friendly.
5. Use bullet points or numbered lists when listing multiple items.

--- CONTEXT ---
{context}
--- END CONTEXT ---

Student Question: {question}

DragonGuide Answer:"""


class DragonBrain:
    """RAG pipeline for DragonGuide — load once, query many times."""

    def __init__(self):
        self._chain = None

    # ── Initialisation ────────────────────────────────────────

    def load(self) -> bool:
        """
        Load the FAISS index and wire up the RetrievalQA chain.
        Returns True on success, False if vectorstore/ is missing.
        """
        index_file = os.path.join(VECTORSTORE_DIR, "index.faiss")
        if not os.path.exists(index_file):
            return False

        api_key = get_openai_api_key()
        if not api_key:
            return False

        embeddings = OpenAIEmbeddings(model="text-embedding-3-small", api_key=api_key)
        vectorstore = FAISS.load_local(
            VECTORSTORE_DIR,
            embeddings,
            allow_dangerous_deserialization=True,
        )

        retriever = vectorstore.as_retriever(
            search_type="mmr",           # Maximal Marginal Relevance — more diverse chunks
            search_kwargs={"k": 6, "fetch_k": 20},
        )

        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=0,
            max_tokens=1024,
            api_key=api_key,
        )

        prompt = PromptTemplate(
            template=_PROMPT_TEMPLATE,
            input_variables=["context", "question"],
        )

        self._chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt},
        )
        return True

    @property
    def is_loaded(self) -> bool:
        return self._chain is not None

    # ── Query interface ───────────────────────────────────────

    def ask(self, question: str) -> dict:
        """
        Ask a question. Returns:
            {
              "answer":  str,
              "sources": [{"source": str, "page": int, "snippet": str}, …]
            }
        """
        if not self.is_loaded:
            raise RuntimeError("DragonBrain not loaded. Call load() first.")

        result           = self._chain.invoke({"query": question})
        answer           = result.get("result", "").strip()
        source_documents = result.get("source_documents", [])

        sources = []
        seen    = set()
        for doc in source_documents:
            meta        = doc.metadata or {}
            source_path = meta.get("source", "Unknown document")
            source_name = os.path.basename(source_path)
            page        = meta.get("page", 0) + 1          # 0-indexed → human page
            snippet     = doc.page_content[:350].strip()
            key         = (source_name, page)
            if key not in seen:
                seen.add(key)
                sources.append({"source": source_name, "page": page, "snippet": snippet})

        return {"answer": answer, "sources": sources}

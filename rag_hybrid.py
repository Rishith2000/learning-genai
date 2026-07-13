"""
rag_hybrid.py — Hybrid RAG: dense (semantic) + BM25 (keyword) fused with RRF.
Beats dense-only retrieval by catching both meaning AND exact terms.
"""
from dotenv import load_dotenv
from anthropic import Anthropic
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
import numpy as np

load_dotenv(override=True)
client = Anthropic()
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# ── Knowledge base ────────────────────────────────────────────────────
docs = [
    "The capital of France is Paris.",
    "Python is a popular programming language for data science.",
    "The Eiffel Tower is located in Paris, France.",
    "Photosynthesis is how plants convert sunlight into energy.",
    "Machine learning models learn patterns from data.",
]

# ── Build both indexes ONCE ───────────────────────────────────────────
doc_embeddings = model.encode(docs, normalize_embeddings=True)   # dense
bm25 = BM25Okapi([d.lower().split() for d in docs])              # sparse

# ── The two retrievers (each returns INDEXES, ranked best-first) ──────
def dense_search(query, k=5):
    q = model.encode(query, normalize_embeddings=True)
    scores = doc_embeddings @ q
    return list(np.argsort(scores)[::-1][:k])

def bm25_search(query, k=5):
    scores = bm25.get_scores(query.lower().split())
    return list(np.argsort(scores)[::-1][:k])

# ── Fusion ────────────────────────────────────────────────────────────
def rrf(ranked_lists, k=60):
    """Reciprocal Rank Fusion: merge ranked lists using position, not score."""
    scores = {}
    for ranked in ranked_lists:
        for rank, idx in enumerate(ranked):
            scores[idx] = scores.get(idx, 0) + 1 / (k + rank)
    return sorted(scores, key=scores.get, reverse=True)

def hybrid_retrieve(query, k=2):
    fused = rrf([dense_search(query), bm25_search(query)])
    return [docs[i] for i in fused[:k]]

# ── Generation (grounded answer) ──────────────────────────────────────
def rag_answer(query, k=2):
    chunks = hybrid_retrieve(query, k)
    context = "\n".join(f"- {c}" for c in chunks)

    resp = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=256,
        system="Answer the question using ONLY the context provided. "
               "If the answer isn't in the context, say you don't know.",
        messages=[{"role": "user",
                   "content": f"Context:\n{context}\n\nQuestion: {query}"}],
    )
    answer = "".join(b.text for b in resp.content if b.type == "text")
    return answer, chunks

# ── Try it ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    for q in ["Where is the Eiffel Tower?",
              "What language is used for data science?",
              "Who won the World Cup in 2022?"]:        # ← not in docs!
        answer, chunks = rag_answer(q)
        print(f"\nQ: {q}")
        print(f"A: {answer}")
        print(f"   sources: {chunks}")
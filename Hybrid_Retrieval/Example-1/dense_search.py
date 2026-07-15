import json
from pathlib import Path
import numpy as np
from sentence_transformers import SentenceTransformer

INDEX_DIR = Path("index")

# --- load the index we built in Step 2 ---
chunks = json.loads((INDEX_DIR / "chunks.json").read_text())
embeddings = np.load(INDEX_DIR / "embeddings.npy")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

print(f"loaded {len(chunks)} chunks, embeddings {embeddings.shape}")


def dense_search(query, k=3):
    # 1. embed the QUERY (the only embedding done at query time)
    q = model.encode(query, normalize_embeddings=True)     # (384,)

    # 2. cosine similarity against all 45 chunks at once
    scores = embeddings @ q                                # (45,)

    # 3. rank: best first, take top k
    top = np.argsort(scores)[::-1][:k]

    return [(scores[i], chunks[i]) for i in top]


def show(query):
    print("\n" + "=" * 70)
    print("QUERY:", query)
    print("=" * 70)
    for score, c in dense_search(query):
        print(f"  {score:.3f}  [{c['source']} — {c['section']}]")
        print(f"         {c['text'][:100]}...")


# --- test 1: a MEANING question (dense should shine) ---
show("customer wants to return a sofa, is there a fee?")

# --- test 2: an EXACT CODE (watch this struggle) ---
show("E-102")
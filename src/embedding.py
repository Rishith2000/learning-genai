from sentence_transformers import SentenceTransformer
import numpy as np

# first run downloads the model (~90MB)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

sentences = [
    "The cat sat on the mat.",
    "A kitten rested on the rug.",     # same meaning, different words
    "Interest rates rose sharply.",     # totally unrelated
]

# normalize so dot product == cosine similarity (range -1 to 1)
emb = model.encode(sentences, normalize_embeddings=True)

print("shape:", emb.shape)          # (3, 384) → 3 sentences, 384 numbers each
for i in range(len(sentences)):
    print("one vector:", emb[i][:8])    # peek at first 8 numbers of sentence 0

def sim(a, b):
    return float(np.dot(a, b))      # cosine similarity

print("\ncat vs kitten (similar): ", round(sim(emb[0], emb[1]), 3))
print("cat vs interest rates:    ", round(sim(emb[0], emb[2]), 3))
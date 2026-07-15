import json
from pathlib import Path
import sys

import numpy as np

# Importing SentenceTransformer may download a model the first time it's used
# and requires the package to be installed. We import it lazily later so that
# the script can still run the chunking step even if the package is missing.

from chunking import chunk_markdown  # reuse Step 1 from chunking.py

# Model name used by sentence-transformers (Hugging Face). Change if needed.
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Use an index directory next to this script so paths are predictable.
BASE = Path(__file__).parent
INDEX_DIR = BASE / "index"


def main() -> int:
    """Main ingestion flow:
    1. Chunk markdown files under `corpus/`.
    2. (Optionally) embed chunks using a SentenceTransformer model.
    3. Save embeddings and chunk metadata to `index/`.

    The function is defensive: it handles a missing corpus, missing model
    package, and empty chunk sets gracefully to make debugging easier.
    """

    corpus_dir = BASE / "corpus"
    if not corpus_dir.exists():
        print(f"Corpus directory not found: {corpus_dir}")
        return 1

    # 1) Chunk the corpus. We read files with explicit utf-8 encoding and
    # call `chunk_markdown` from the `chunking` module to split documents.
    chunks = []
    for f in sorted(corpus_dir.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        chunks += chunk_markdown(text, f.name)
    print(f"{len(chunks)} chunks")

    if not chunks:
        print("No chunks created; aborting embedding and index save.")
        return 0

    # 2) Embed them. Import the SentenceTransformer package here so the script
    # can still produce chunks even if the package isn't installed.
    try:
        from sentence_transformers import SentenceTransformer
    except Exception as exc:  # pragma: no cover - environment dependent
        print("sentence-transformers not available:", exc)
        print("Skipping embedding step. Install 'sentence-transformers' to run embeddings.")
        return 0

    model = SentenceTransformer(EMBED_MODEL)
    embeddings = model.encode(
        [c["text"] for c in chunks],  # only the chunk text is embedded
        normalize_embeddings=True,      # length-1 vectors: cosine == dot
        show_progress_bar=True,
    ).astype(np.float32)

    print("embeddings shape:", embeddings.shape)

    # 3) Save to disk. Use a directory next to the script for the index files.
    INDEX_DIR.mkdir(exist_ok=True)
    np.save(INDEX_DIR / "embeddings.npy", embeddings)
    (INDEX_DIR / "chunks.json").write_text(json.dumps(chunks, indent=2))
    print(f"Saved index to {INDEX_DIR}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
from pathlib import Path

CHUNK_SIZE, OVERLAP = 700, 120


def split_long(text, size, overlap):
    """Fallback — only runs if a section is bigger than CHUNK_SIZE."""
    if len(text) <= size:
        return [text]
    out, start = [], 0
    while start < len(text):
        out.append(text[start:start + size])
        start += size - overlap          # move 580, so consecutive chunks overlap by 120
    return [t for t in out if t.strip()]


def chunk_markdown(text, source):
    """Cut at '## ' headings — each section is one complete policy."""
    chunks = []
    for part in text.split("\n## "):                  # ← the key line
        part = part.strip()
        if not part or part.startswith("# "):
            continue                                  # skip the doc title
        heading = part.split("\n", 1)[0].strip()      # section name
        for piece in split_long(part, CHUNK_SIZE, OVERLAP):
            chunks.append({
                "source": source,
                "section": heading,
                "text": " ".join(piece.split()),      # collapse whitespace
            })
    return chunks


base = Path(__file__).parent
corpus_dir = base / "corpus"
if not corpus_dir.exists():
    print(f"Corpus directory not found: {corpus_dir}")
    files = []
else:
    files = sorted(corpus_dir.glob("*.md"))

all_chunks = []

if not files:
    print("No markdown files found in corpus.")
else:
    for f in files:
        text = f.read_text(encoding="utf-8")
        cs = chunk_markdown(text, f.name)
        all_chunks += cs
        print(f"{f.name:32} {len(cs):2d} chunks")

print(f"\nTOTAL: {len(all_chunks)} chunks")

print("\n--- example chunk ---")
if len(all_chunks) > 3:
    c = all_chunks[3]
    print("source :", c["source"])
    print("section:", c["section"])
    print("text   :", c["text"])
else:
    print("Not enough chunks to show example (need at least 4).")

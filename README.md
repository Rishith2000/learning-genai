# learning-genai

Personal sandbox for learning and experimenting with Generative AI: LLM APIs
(Anthropic Claude, Google Gemini), embeddings, and retrieval-augmented
generation (RAG).

## Structure

```
src/
  main.py          entry point — sanity-checks the Anthropic API key
  embedding.py      sentence-transformers embeddings + cosine similarity demo
notebooks/
  rung1.ipynb              exploring the Anthropic SDK, response shapes, chat loop
  context-embedding.ipynb  embeddings + context experiments
  rag-basics.ipynb         RAG fundamentals
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then fill in your API key(s)
```

## Run

```bash
python src/main.py
python src/embedding.py
```

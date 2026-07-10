"""
learning-genai

Entry point / quick sanity check for the repo. Confirms the Anthropic API
key in .env is wired up correctly before diving into the notebooks.
"""

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

if not os.getenv("ANTHROPIC_API_KEY"):
    raise RuntimeError("ANTHROPIC_API_KEY is not set in your .env file")

client = Anthropic()

response = client.messages.create(
    model="claude-haiku-4-5",
    max_tokens=256,
    messages=[{"role": "user", "content": "Explain what an API is in two sentences."}],
)

print(response.content[0].text)

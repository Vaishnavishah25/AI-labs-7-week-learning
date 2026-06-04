# AI Documentation Assistant

> **A beginner-friendly, production-style LangChain project**
> Powered by LangChain LCEL · Ollama (llama3) · Pydantic · Python

---

## What This Project Does

Enter any technical topic (e.g. *RAG*, *Kubernetes*, *LangChain*) and get back:

- **Technical explanation** — plain English, beginner-friendly
- **Architecture summary** — how the technology works internally
- **Key components** — the building blocks you need to know
- **Best practices** — actionable tips for real-world use
- **Structured JSON output** — validated by Pydantic, saved to file

---

## Project Structure

```
ai_documentation_assistant/
├── app.py              ← Entry point: user input, display, save to file
├── chains.py           ← LCEL pipelines (prompt | llm | parser)
├── prompts.py          ← All ChatPromptTemplate definitions
├── schemas.py          ← Pydantic models for structured output
├── bonus_features.py   ← Memory, RAG, FastAPI, streaming, markdown export
├── requirements.txt    ← Python dependencies
├── .env                ← Configuration (model name, Ollama URL)
└── output/
    └── generated_docs.json   ← Saved documentation history
```

---

## Quick Start

### Step 1 — Install Ollama

```bash
# macOS / Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows — download from https://ollama.com/download
```

### Step 2 — Pull the model

```bash
ollama pull llama3
```

### Step 3 — Verify Ollama is running

```bash
ollama serve          # starts the server (runs on http://localhost:11434)
ollama list           # should show llama3 in the list
```

### Step 4 — Clone / create the project in VS Code

```bash
# Open VS Code terminal (Ctrl+` or Cmd+`)
cd ~/Documents
mkdir ai_documentation_assistant
cd ai_documentation_assistant
code .                # open folder in VS Code
```

### Step 5 — Create and activate a virtual environment

```bash
# Create the venv
python -m venv venv

# Activate it
# macOS / Linux:
source venv/bin/activate
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# Windows (CMD):
venv\Scripts\activate.bat
```

You should see `(venv)` at the start of your terminal prompt.

### Step 6 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 7 — Run the project

```bash
python app.py
```

---

## Sample Terminal Output

```
════════════════════════════════════════════════════════════
   🤖  AI Documentation Assistant
   Powered by LangChain + Ollama (llama3)
════════════════════════════════════════════════════════════

Enter a technical topic (e.g. RAG, LangChain, Kubernetes): RAG

Choose output mode:
  1 → Full structured JSON documentation  (saves to file)
  2 → Streamed plain-text explanation
  3 → Both

Enter 1, 2, or 3 [default: 1]: 1

⏳  Generating structured documentation for: 'RAG' ...

────────────────────────────────────────────────────────────
  📚  TOPIC
────────────────────────────────────────────────────────────
RAG

────────────────────────────────────────────────────────────
  🧠  TECHNICAL EXPLANATION
────────────────────────────────────────────────────────────
RAG stands for Retrieval-Augmented Generation. It is a technique that
improves AI answers by first searching a knowledge base, then handing
the relevant information to the language model ...

────────────────────────────────────────────────────────────
  🏗️   ARCHITECTURE SUMMARY
────────────────────────────────────────────────────────────
A RAG system has two stages: indexing and retrieval-generation ...

────────────────────────────────────────────────────────────
  🔩  KEY COMPONENTS
────────────────────────────────────────────────────────────
  • Document Loader
  • Text Splitter
  • Embedding Model
  • Vector Store
  • Retriever
  • LLM

────────────────────────────────────────────────────────────
  ✅  BEST PRACTICES
────────────────────────────────────────────────────────────
  • Choose chunk size carefully: 512–1024 tokens
  • Add overlap between chunks to avoid context cutoffs
  ...

✅  Saved to /your/path/output/generated_docs.json

🎉  Done! Thank you for using AI Documentation Assistant.
```

---

## How LCEL Works (the Core Concept)

```
prompt | llm | parser
  ↑        ↑       ↑
  │        │       └─ Converts AIMessage → Python object / string
  │        └───────── Sends messages to Ollama, returns AIMessage
  └────────────────── Fills {topic} placeholder, returns ChatMessages
```

Each step is a **Runnable**. The `|` operator chains them so the output of
one becomes the input of the next — exactly like Unix pipes.

---

## Common Errors and Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| `Connection refused` | Ollama not running | Run `ollama serve` |
| `model not found` | llama3 not pulled | Run `ollama pull llama3` |
| `ModuleNotFoundError` | venv not activated | Run `source venv/bin/activate` |
| `JSONDecodeError` | Model returned bad JSON | Lower temperature in `.env` or retry |
| `venv not recognised` | Python not in PATH | Install Python 3.10+ and restart terminal |

---

## Bonus Features

| Feature | File | How to use |
|---------|------|-----------|
| Conversation memory | `bonus_features.py` | Call `demo_memory()` |
| RAG over documents | `bonus_features.py` | Call `build_rag_chain(text, question)` |
| FastAPI REST API | `bonus_features.py` | `uvicorn bonus_features:fastapi_app --reload` |
| Streaming | `bonus_features.py` | Call `demo_streaming("Docker")` |
| Markdown export | `bonus_features.py` | Call `export_to_markdown(data)` |

---

## Learning Path

After this project, explore:

1. **LangChain Agents** — let the model decide which tool to use
2. **LangSmith** — observability and tracing for your chains
3. **Multi-modal** — pass images to vision models via Ollama
4. **Production RAG** — Chroma, Qdrant, or Weaviate as your vector store

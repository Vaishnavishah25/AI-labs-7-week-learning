# bonus_features.py
# ─────────────────────────────────────────────────────────────────────────────
# BONUS FEATURES — read through these after the main project works.
# Each section is self-contained. Copy the parts you want into your project.
# ─────────────────────────────────────────────────────────────────────────────


# ══════════════════════════════════════════════════════════════════════════════
# BONUS 1 — CONVERSATION MEMORY
# ══════════════════════════════════════════════════════════════════════════════
#
# By default, each chain.invoke() call is stateless — the model forgets the
# previous turn.  ConversationBufferMemory keeps the full chat history in
# memory and automatically appends it to every new prompt.
#
# HOW IT WORKS:
#   RunnableWithMessageHistory wraps any LCEL chain.
#   It intercepts each call, loads the history for the given session_id,
#   prepends it to the messages, and saves the new turns after the call.
#
# ─────────────────────────────────────────────────────────────────────────────

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Simple in-process store: session_id → ChatMessageHistory object
_session_store: dict[str, ChatMessageHistory] = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    """Return (or create) the message history for a given session."""
    if session_id not in _session_store:
        _session_store[session_id] = ChatMessageHistory()
    return _session_store[session_id]


def build_memory_chain():
    """
    Returns a stateful chain that remembers conversation history.

    The {history} placeholder is filled automatically by
    RunnableWithMessageHistory — you do NOT pass it manually.
    """
    from langchain_ollama import ChatOllama
    from langchain_core.output_parsers import StrOutputParser

    llm = ChatOllama(model="llama3", temperature=0.3)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful technical assistant. Answer questions clearly."),
        MessagesPlaceholder(variable_name="history"),  # ← injected automatically
        ("human", "{input}"),
    ])

    chain = prompt | llm | StrOutputParser()

    # Wrap the chain with history management
    chain_with_memory = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )
    return chain_with_memory


def demo_memory():
    chain = build_memory_chain()
    config = {"configurable": {"session_id": "user-001"}}

    r1 = chain.invoke({"input": "What is LangChain?"}, config=config)
    print("Turn 1:", r1)

    # The model now remembers what was said about LangChain
    r2 = chain.invoke({"input": "Can you give me an example of what you just explained?"}, config=config)
    print("Turn 2:", r2)


# ══════════════════════════════════════════════════════════════════════════════
# BONUS 2 — SIMPLE RAG (Retrieval-Augmented Generation)
# ══════════════════════════════════════════════════════════════════════════════
#
# RAG lets the model answer questions about YOUR documents — not just its
# training data.  Steps:
#   1. Load documents
#   2. Split into chunks
#   3. Embed chunks → store in vector DB
#   4. At query time: retrieve relevant chunks → feed to LLM
#
# Install extras first:
#   pip install faiss-cpu langchain-community
# ─────────────────────────────────────────────────────────────────────────────

def build_rag_chain(documents_text: str, question: str) -> str:
    """
    Minimal RAG demo — splits text, embeds with Ollama, retrieves, answers.

    Args:
        documents_text: raw text you want the model to reason over
        question:       the user's question

    Returns:
        The model's answer grounded in the provided documents
    """
    from langchain_community.vectorstores import FAISS
    from langchain_ollama import OllamaEmbeddings, ChatOllama
    from langchain_core.documents import Document
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough

    # 1. Wrap raw text in a Document object
    doc = Document(page_content=documents_text)

    # 2. Split into 500-token chunks with 50-token overlap
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks   = splitter.split_documents([doc])

    # 3. Embed and store in FAISS (runs locally via Ollama's nomic-embed-text)
    embeddings   = OllamaEmbeddings(model="nomic-embed-text")
    vector_store = FAISS.from_documents(chunks, embeddings)

    # 4. Create a retriever that fetches top 3 relevant chunks
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    # 5. Build the RAG prompt
    rag_prompt = ChatPromptTemplate.from_messages([
        ("system",
         "Answer the question using ONLY the context below. "
         "If the answer is not in the context, say 'I don't know'.\n\n"
         "Context:\n{context}"),
        ("human", "{question}"),
    ])

    # 6. LCEL pipeline with retrieval
    def format_docs(docs):
        return "\n\n".join(d.page_content for d in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | rag_prompt
        | ChatOllama(model="llama3")
        | StrOutputParser()
    )

    return chain.invoke(question)


# ══════════════════════════════════════════════════════════════════════════════
# BONUS 3 — FASTAPI REST API
# ══════════════════════════════════════════════════════════════════════════════
#
# Wrap the documentation chain in a FastAPI endpoint so any client
# (Postman, frontend, mobile app) can call it over HTTP.
#
# Install:  pip install fastapi uvicorn
# Run:      uvicorn bonus_features:fastapi_app --reload --port 8000
# Test:     curl -X POST http://localhost:8000/generate \
#             -H "Content-Type: application/json" \
#             -d '{"topic": "Kubernetes"}'
# ─────────────────────────────────────────────────────────────────────────────

try:
    from fastapi import FastAPI
    from fastapi.responses import StreamingResponse
    from pydantic import BaseModel as PydanticBaseModel

    fastapi_app = FastAPI(title="AI Documentation Assistant API")

    class TopicRequest(PydanticBaseModel):
        topic: str

    @fastapi_app.post("/generate")
    async def generate_docs(request: TopicRequest):
        """Returns structured JSON documentation for a technical topic."""
        from chains import build_documentation_chain
        chain  = build_documentation_chain()
        result = chain.invoke({"topic": request.topic})
        return result

    @fastapi_app.post("/stream")
    async def stream_docs(request: TopicRequest):
        """Streams the plain-text explanation token by token (SSE)."""
        from chains import stream_explanation

        def token_generator():
            for chunk in stream_explanation(request.topic):
                yield chunk

        return StreamingResponse(token_generator(), media_type="text/plain")

except ImportError:
    # FastAPI not installed — that is fine for the core project
    fastapi_app = None


# ══════════════════════════════════════════════════════════════════════════════
# BONUS 4 — EXPORT TO MARKDOWN
# ══════════════════════════════════════════════════════════════════════════════

def export_to_markdown(data: dict, output_path: str = "output/documentation.md"):
    """
    Converts the structured documentation dict into a pretty Markdown file.

    Args:
        data:        dict returned by build_documentation_chain()
        output_path: where to save the .md file
    """
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    lines = [
        f"# {data.get('topic', 'Unknown Topic')}",
        "",
        "## Technical Explanation",
        "",
        data.get("technical_explanation", ""),
        "",
        "## Architecture Summary",
        "",
        data.get("architecture_summary", ""),
        "",
        "## Key Components",
        "",
    ]

    for component in data.get("key_components", []):
        lines.append(f"- {component}")

    lines += [
        "",
        "## Best Practices",
        "",
    ]

    for practice in data.get("best_practices", []):
        lines.append(f"- {practice}")

    lines += [
        "",
        f"---",
        f"*Generated by AI Documentation Assistant on {data.get('generated_at', '')}*",
    ]

    with open(output_path, "w") as f:
        f.write("\n".join(lines))

    print(f"✅  Markdown saved to {output_path}")


# ══════════════════════════════════════════════════════════════════════════════
# BONUS 5 — STREAMING DEMO (standalone)
# ══════════════════════════════════════════════════════════════════════════════

def demo_streaming(topic: str = "Docker"):
    """
    Run this directly to see token-by-token streaming in the terminal.
    """
    from chains import stream_explanation

    print(f"\nStreaming explanation of '{topic}' ...\n")
    print("─" * 50)

    for chunk in stream_explanation(topic):
        print(chunk, end="", flush=True)

    print("\n" + "─" * 50)


# ── Run demos when executed directly ─────────────────────────────────────────
if __name__ == "__main__":
    print("Running Streaming Demo...")
    demo_streaming("LangChain")

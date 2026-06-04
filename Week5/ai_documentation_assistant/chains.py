# chains.py
# ─────────────────────────────────────────────────────────────────────────────
# WHY THIS FILE EXISTS:
#   This is the "engine room" of the project.  It wires together the three
#   major LangChain building blocks — prompt, LLM, and parser — using LCEL.
#
# WHAT IS LCEL?
#   LCEL (LangChain Expression Language) is a way to compose AI pipelines
#   using the pipe operator  |  just like Unix shell pipes.
#
#   Unix shell:   cat file.txt | grep "error" | sort
#   LCEL:         prompt | llm | parser
#
#   Each step receives the output of the previous step as its input.
#   LangChain calls these composable pieces "Runnables".
#
# HOW THE PIPELINE FLOWS:
#
#   1. prompt.invoke({"topic": "RAG"})
#      → Fills {topic} → returns a list of ChatMessage objects
#
#   2. llm.invoke(messages)
#      → Sends messages to Ollama → returns an AIMessage with .content (string)
#
#   3. parser.invoke(ai_message)
#      → Extracts / validates the string → returns a Python object or plain str
#
#   The pipe operator | chains these three Runnables so you can call the whole
#   thing with one line:  chain.invoke({"topic": "RAG"})
# ─────────────────────────────────────────────────────────────────────────────

import os
from dotenv import load_dotenv

# LangChain Ollama integration — lets LangChain talk to your local Ollama server
from langchain_ollama import ChatOllama

# Output parsers — transform the LLM's raw reply into usable Python objects
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

# Our prompt templates (defined in prompts.py)
from prompts import DOCUMENTATION_PROMPT, EXPLANATION_PROMPT, ARCHITECTURE_PROMPT

# Our Pydantic schema (defined in schemas.py)
from schemas import DocumentationOutput

# Load environment variables from .env (e.g., OLLAMA_MODEL)
load_dotenv()


# ── LLM SETUP ─────────────────────────────────────────────────────────────────
#
# ChatOllama connects LangChain to your locally running Ollama server.
#
# model       → which model Ollama should use (pulled via `ollama pull llama3`)
# temperature → creativity level:
#               0.0 = deterministic/factual (good for structured output)
#               1.0 = creative/varied
# base_url    → where Ollama is listening (default: localhost:11434)
#
def get_llm(temperature: float = 0.1) -> ChatOllama:
    """
    Factory function that creates and returns a ChatOllama instance.
    Using a factory instead of a module-level variable means we can
    easily swap models or settings from app.py if needed.
    """
    model_name = os.getenv("OLLAMA_MODEL", "llama3")   # fallback to llama3
    base_url   = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

    return ChatOllama(
        model=model_name,
        temperature=temperature,
        base_url=base_url,
        # format="json" tells Ollama to enable its built-in JSON mode.
        # This makes the model more likely to return valid JSON every time.
        format="json",
    )


# ── CHAIN 1: STRUCTURED DOCUMENTATION CHAIN ───────────────────────────────────
#
# Pipeline:  DOCUMENTATION_PROMPT | llm | JsonOutputParser()
#
# JsonOutputParser does two things:
#   a) Strips any markdown fences (``` json ... ```) the model may add
#   b) Calls json.loads() on the remaining string
#   c) Optionally validates against a Pydantic model (passed via pydantic_object)
#
# The result is a plain Python dict that matches DocumentationOutput's fields.
#
def build_documentation_chain():
    """
    Returns a Runnable that:
      Input  → {"topic": "<string>"}
      Output → dict matching DocumentationOutput schema
    """
    llm    = get_llm(temperature=0.1)        # low temp → consistent structure
    parser = JsonOutputParser(pydantic_object=DocumentationOutput)

    # THE LCEL PIPELINE — read left to right:
    #   1. prompt formats the messages
    #   2. llm generates a JSON string
    #   3. parser converts the JSON string → Python dict
    chain = DOCUMENTATION_PROMPT | llm | parser

    return chain


# ── CHAIN 2: PLAIN-TEXT EXPLANATION CHAIN ─────────────────────────────────────
#
# Pipeline:  EXPLANATION_PROMPT | llm | StrOutputParser()
#
# StrOutputParser simply extracts the .content string from the AIMessage.
# Use this when you want a readable paragraph, not structured data.
#
def build_explanation_chain():
    """
    Returns a Runnable that:
      Input  → {"topic": "<string>"}
      Output → plain string (paragraphs of explanation)
    """
    llm    = get_llm(temperature=0.3)        # slightly higher temp for readability
    parser = StrOutputParser()

    chain = EXPLANATION_PROMPT | llm | parser
    return chain


# ── CHAIN 3: ARCHITECTURE CHAIN ───────────────────────────────────────────────
#
# Same pattern — demonstrates that once you learn the pattern,
# you can spin up specialised chains quickly.
#
def build_architecture_chain():
    """
    Returns a Runnable that:
      Input  → {"topic": "<string>"}
      Output → plain string (architecture description)
    """
    llm    = get_llm(temperature=0.1)
    parser = StrOutputParser()

    chain = ARCHITECTURE_PROMPT | llm | parser
    return chain


# ── BONUS: STREAMING CHAIN ────────────────────────────────────────────────────
#
# Any LCEL chain supports .stream() out of the box.
# This generator yields tokens as they arrive — no waiting for the full reply.
#
def stream_explanation(topic: str):
    """
    Streams the explanation token-by-token.
    Usage:
        for chunk in stream_explanation("Kubernetes"):
            print(chunk, end="", flush=True)
    """
    chain = build_explanation_chain()
    for chunk in chain.stream({"topic": topic}):
        yield chunk

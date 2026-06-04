# prompts.py
# ─────────────────────────────────────────────────────────────────────────────
# WHY THIS FILE EXISTS:
#   A "prompt template" is a reusable message blueprint with placeholders.
#   Instead of hard-coding your instruction string inside chains.py or app.py,
#   you define it once here, keep it clean, and inject runtime values later.
#
# HOW PROMPT TEMPLATES WORK:
#   ChatPromptTemplate.from_messages([...]) accepts a list of (role, content)
#   tuples.  Roles can be:
#     "system"  → background instructions the model always sees first
#     "human"   → the user's turn (contains your {placeholders})
#     "ai"      → a pre-filled assistant turn (rarely needed here)
#
#   When you call  prompt.invoke({"topic": "RAG"})  LangChain replaces every
#   {topic} placeholder with the real value and returns a list of
#   ChatMessage objects ready for the LLM.
# ─────────────────────────────────────────────────────────────────────────────

from langchain_core.prompts import ChatPromptTemplate


# ── 1. DOCUMENTATION PROMPT ──────────────────────────────────────────────────
#
# This prompt drives the main feature: structured documentation generation.
# Notice the system message sets the persona and constraints once,
# while the human message carries the only dynamic part: {topic}.
#
DOCUMENTATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert technical writer and software architect.
Your job is to generate clear, accurate, beginner-friendly documentation.

Rules you must follow:
- Use plain English; avoid unexplained acronyms.
- Explanations should be understandable by a junior developer.
- Be concise but complete — do not pad with filler sentences.
- Always respond with valid, well-formed JSON that matches the schema exactly.
- Do not add any text before or after the JSON block.""",
        ),
        (
            "human",
            """Generate comprehensive technical documentation for the following topic:

Topic: {topic}

Return your response as a JSON object with these exact keys:
- topic
- technical_explanation
- architecture_summary
- key_components   (array of strings)
- best_practices   (array of strings)""",
        ),
    ]
)


# ── 2. EXPLANATION-ONLY PROMPT ────────────────────────────────────────────────
#
# A lighter prompt used when we only need a plain-text explanation
# (no structured output).  Demonstrates how the same {topic} variable
# can feed different pipelines.
#
EXPLANATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a patient senior engineer mentoring a junior developer. "
            "Explain technical concepts in a friendly, approachable tone.",
        ),
        (
            "human",
            "Please explain '{topic}' in 3–4 short paragraphs. "
            "Start from the basics before moving to advanced ideas.",
        ),
    ]
)


# ── 3. ARCHITECTURE PROMPT ────────────────────────────────────────────────────
#
# Focused solely on architectural overview.
# Shows how you can compose specialised prompts for specific sub-tasks.
#
ARCHITECTURE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a solutions architect. Describe system designs clearly and concisely.",
        ),
        (
            "human",
            "Describe the internal architecture of '{topic}'. "
            "Cover the main layers, components, and how data flows between them. "
            "Use bullet points where helpful.",
        ),
    ]
)

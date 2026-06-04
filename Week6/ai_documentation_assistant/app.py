# app.py
# ─────────────────────────────────────────────────────────────────────────────
# WHY THIS FILE EXISTS:
#   This is the entry point — the file you run with `python app.py`.
#   It handles:
#     • Greeting the user
#     • Collecting input
#     • Calling the right chain from chains.py
#     • Displaying results in the terminal
#     • Saving the structured output to output/generated_docs.json
#
# KEEP THIS FILE THIN:
#   app.py should only coordinate — not contain business logic.
#   Logic lives in chains.py, schemas.py, and prompts.py.
# ─────────────────────────────────────────────────────────────────────────────

import json
import os
import sys
from pathlib import Path
from datetime import datetime

# Our chain builders (defined in chains.py)
from chains import (
    build_documentation_chain,
    build_explanation_chain,
    stream_explanation,
)


# ── HELPERS ───────────────────────────────────────────────────────────────────

def print_banner():
    """Print a friendly welcome banner."""
    print("\n" + "═" * 60)
    print("   🤖  AI Documentation Assistant")
    print("   Powered by LangChain + Ollama (llama3)")
    print("═" * 60 + "\n")


def print_section(title: str, content: str):
    """Pretty-print a labelled section."""
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print(f"{'─' * 60}")
    print(content)


def save_output(data: dict, topic: str):
    """
    Save the structured output dict to a JSON file.

    Path: output/generated_docs.json
    Each run APPENDS to a list inside the file so you build a history
    of all topics you have documented.
    """
    output_dir  = Path("output")
    output_dir.mkdir(exist_ok=True)          # create folder if it doesn't exist
    output_file = output_dir / "generated_docs.json"

    # Load existing records (if the file already exists)
    records = []
    if output_file.exists():
        try:
            with open(output_file, "r") as f:
                records = json.load(f)
        except json.JSONDecodeError:
            records = []                     # file was empty or corrupt — start fresh

    # Add metadata to this run
    data["generated_at"] = datetime.now().isoformat()

    records.append(data)

    with open(output_file, "w") as f:
        json.dump(records, f, indent=2)

    print(f"\n✅  Saved to {output_file.resolve()}")


# ── MAIN FLOW ─────────────────────────────────────────────────────────────────

def run_documentation_mode(topic: str):
    """
    Full structured documentation pipeline.
    Calls the DOCUMENTATION_PROMPT | llm | JsonOutputParser chain.
    """
    print(f"\n⏳  Generating structured documentation for: '{topic}' ...")
    print("    (This may take 15–30 seconds on first run while Ollama loads)\n")

    chain = build_documentation_chain()

    try:
        # .invoke() runs the full LCEL pipeline synchronously and returns
        # a dict (because we used JsonOutputParser in chains.py)
        result: dict = chain.invoke({"topic": topic})
    except Exception as e:
        print(f"\n❌  Error calling Ollama: {e}")
        print("\nTroubleshooting checklist:")
        print("  1. Is Ollama running?  →  ollama serve")
        print("  2. Is llama3 pulled?   →  ollama pull llama3")
        print("  3. Check OLLAMA_BASE_URL in your .env file")
        sys.exit(1)

    # ── Display results ───────────────────────────────────────────────────────

    print_section("📚  TOPIC", result.get("topic", topic))

    print_section("🧠  TECHNICAL EXPLANATION", result.get("technical_explanation", ""))

    print_section("🏗️   ARCHITECTURE SUMMARY", result.get("architecture_summary", ""))

    components = result.get("key_components", [])
    if components:
        print_section("🔩  KEY COMPONENTS", "\n".join(f"  • {c}" for c in components))

    practices = result.get("best_practices", [])
    if practices:
        print_section("✅  BEST PRACTICES", "\n".join(f"  • {p}" for p in practices))

    # ── Save to file ──────────────────────────────────────────────────────────
    save_output(result, topic)

    return result


def run_explanation_mode(topic: str):
    """
    Streaming plain-text explanation pipeline.
    Demonstrates .stream() — tokens appear as they are generated.
    """
    print(f"\n⏳  Streaming explanation for: '{topic}' ...\n")
    print("─" * 60)

    # stream_explanation() is a generator — we iterate token by token
    for chunk in stream_explanation(topic):
        print(chunk, end="", flush=True)   # flush=True makes each token appear immediately

    print("\n" + "─" * 60)


# ── ENTRY POINT ───────────────────────────────────────────────────────────────

def main():
    print_banner()

    # ── Get topic from user ───────────────────────────────────────────────────
    topic = input("Enter a technical topic (e.g. RAG, LangChain, Kubernetes): ").strip()

    if not topic:
        print("❌  No topic entered. Exiting.")
        sys.exit(1)

    # ── Choose mode ───────────────────────────────────────────────────────────
    print("\nChoose output mode:")
    print("  1 → Full structured JSON documentation  (saves to file)")
    print("  2 → Streamed plain-text explanation")
    print("  3 → Both")

    mode = input("\nEnter 1, 2, or 3 [default: 1]: ").strip() or "1"

    if mode == "1":
        run_documentation_mode(topic)

    elif mode == "2":
        run_explanation_mode(topic)

    elif mode == "3":
        run_documentation_mode(topic)
        print("\n\n" + "═" * 60)
        print("  Now streaming a plain-text explanation …")
        print("═" * 60)
        run_explanation_mode(topic)

    else:
        print(f"❌  Unknown mode '{mode}'. Running mode 1 by default.")
        run_documentation_mode(topic)

    print("\n\n🎉  Done! Thank you for using AI Documentation Assistant.\n")


if __name__ == "__main__":
    main()

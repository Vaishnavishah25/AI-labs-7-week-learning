# schemas.py
# ─────────────────────────────────────────────────────────────────────────────
# WHY THIS FILE EXISTS:
#   LangChain can force the LLM to return data that matches a strict shape.
#   We define that shape here using Pydantic — Python's most popular data
#   validation library.  When the LLM output is parsed, Pydantic checks every
#   field automatically and raises a clear error if something is missing or
#   has the wrong type.
#
# HOW STRUCTURED OUTPUT WORKS (big picture):
#   1.  You define a Python class that inherits from BaseModel.
#   2.  Each class attribute becomes a required (or optional) field.
#   3.  LangChain serialises the schema to JSON Schema and injects it into
#       the prompt so the model knows exactly what to produce.
#   4.  The parser deserialises the model's JSON reply back into your class.
#   Result → you get a real Python object, not a raw string.
# ─────────────────────────────────────────────────────────────────────────────

from pydantic import BaseModel, Field
from typing import List


class DocumentationOutput(BaseModel):
    """
    This is the shape of every response the AI will produce.

    Pydantic's BaseModel gives us:
      • automatic type checking
      • helpful error messages when data is wrong
      • easy JSON serialisation (.model_dump_json())

    The Field(...) calls let us attach a description to each field.
    LangChain forwards those descriptions to the LLM so it understands
    exactly what to write in each slot.
    """

    topic: str = Field(
        ...,                          # '...' means this field is required
        description="The exact technical topic that was requested by the user."
    )

    technical_explanation: str = Field(
        ...,
        description=(
            "A beginner-friendly explanation of the topic. "
            "Use plain language and short sentences. "
            "Avoid unexplained jargon."
        )
    )

    architecture_summary: str = Field(
        ...,
        description=(
            "A concise overview of how the technology is structured internally. "
            "Mention the main layers, components, or stages."
        )
    )

    key_components: List[str] = Field(
        ...,
        description=(
            "A list of 4–6 individual components, concepts, or building blocks "
            "that are central to understanding this topic."
        )
    )

    best_practices: List[str] = Field(
        ...,
        description=(
            "A list of 4–6 practical best-practice tips a developer should follow "
            "when working with this technology."
        )
    )

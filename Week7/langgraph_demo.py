from dotenv import load_dotenv
from langchain_core.runnables import RunnableLambda
import os

# Load environment variables
load_dotenv()

# LangChain ollama model
from langchain_ollama import ChatOllama

# LangGraph imports
from langgraph.graph import StateGraph, END
from typing_extensions import TypedDict

# ----------------------------------------
# DEFINE STATE
# ----------------------------------------

class GraphState(TypedDict):
    topic: str
    research: str
    summary: str


# ----------------------------------------
# LOAD GEMINI MODEL
# ----------------------------------------

llm = ChatOllama(
    model="llama3",
    temperature=0.5
)

# ----------------------------------------
# NODE 1 → RESEARCH AGENT
# ----------------------------------------

def research_agent(state: GraphState):
    print("\n🔍 Research Agent Running...\n")
    topic = state["topic"]

    response = llm.invoke(
        f"Give detailed information about {topic}"
    )

    return {
        "research": response.content
    }

# ----------------------------------------
# NODE 2 → SUMMARY AGENT
# ----------------------------------------

def summary_agent(state: GraphState):

    print("\n📝 Summary Agent Running...\n")
    research_text = state.get("research", "")
    if not research_text:
        return{**state, "summary": "No research data available to summarize."}
    response = llm.invoke(
        f"Summarize this in 5 lines:\n\n{research_text}"
    )

    return {**state,
        "summary": response.content
    }

# ----------------------------------------
# CREATE GRAPH
# ----------------------------------------

graph = StateGraph(dict)

# Add nodes
graph.add_node("research",RunnableLambda(research_agent))
graph.add_node("summary",RunnableLambda(summary_agent))

# Set entry point
graph.set_entry_point("research")

# Connect nodes using edges
graph.add_edge("research", "summary")

# End graph
graph.add_edge("summary", END)

# ----------------------------------------
# COMPILE GRAPH
# ----------------------------------------

app = graph.compile()

# ----------------------------------------
# SHOW GRAPH STRUCTURE
# ----------------------------------------

print(app.get_graph().draw_ascii())

# ----------------------------------------
# RUN GRAPH
# ----------------------------------------

result = app.invoke({
    "topic": "LangGraph"
})

# ----------------------------------------
# PRINT FINAL OUTPUT
# ----------------------------------------

print("\n" + "="*50)
print("FINAL OUTPUT")
print("="*50)

print("\n📚 Research:\n")
print(result["research"])

print("\n📝 Summary:\n")
print(result["summary"]) 

app.get_graph().draw_mermaid_png()
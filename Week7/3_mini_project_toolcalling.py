from typing import TypedDict
from langgraph.graph import StateGraph,START,END
from datetime import datetime

class ToolCallingStateDict(TypedDict):
    query: str
    tool: str
    result: str

## tools
def Calculator_tool(expression:str):
    try:
        return str(eval(expression))
    except:
        return "Invalid expression"

def Date_tool():
    return datetime.now().strftime("%d-%m-%Y")

def Knowledge_tool(query:str):
    knowledge_base = {
        "What is AI?": "AI stands for Artificial Intelligence.",
        "What is LLM?": "LLM stands for Large Language Model.",
        
    }
    return knowledge_base.get(query, "I don't know the answer to that question.")


## Agent Node
def agent(state):
    query = state["query"].lower()

    if "date" in query:
        state["tool"]  = "date"

    elif any(op in query for op in ["+", "-", "*", "/"]):
        state["tool"] = "calculator"

    else:
        state["tool"] = "knowledge"

    return state

## Router Node
def route_tool(state):
    return state["tool"]

def calculator_node(state):
    result = Calculator_tool(state["query"])
    state["result"] = result
    return state

def date_node(state):
    state["result"] = Date_tool()
    return state

def knowledge_node(state):
    query = state["query"]
    state["result"] = Knowledge_tool(query)
    return state

def response_node(state):
    print("Result:",state["result"])
    return state

graph = StateGraph(ToolCallingStateDict)
graph.add_node("Agent", agent)
graph.add_node("Calculator", calculator_node)
graph.add_node("Date", date_node)
graph.add_node("Knowledge", knowledge_node)

graph.add_node("Response", response_node)
graph.add_edge(START, "Agent")
graph.add_conditional_edges(
    "Agent",
    route_tool,
    {
        "calculator": "Calculator",
        "date": "Date",
        "knowledge": "Knowledge"
    }
)
graph.add_edge("Calculator", "Response")
graph.add_edge("Date", "Response")
graph.add_edge("Knowledge", "Response")

graph.add_edge("Response", END)
app = graph.compile()
app.invoke({
    "query": "What is AI?",
    "tool": "",
    "result": ""
})

'''app.invoke({
    "query": "date",
    "tool": "",
    "result": ""
})'''
'''app.invoke({
    "query": "15*12",
    "tool": "",
    "result": ""
})'''

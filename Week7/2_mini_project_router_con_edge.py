from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class RouterStateDict(TypedDict):
    query: str
    intent: str


def Router(state):
    query = state["query"].lower()

    if query in ["hello", "hi", "hey"]:
        state["intent"] = "Greeter"

    elif query == "1+1":
        state["intent"] = "Math"

    else:
        state["intent"] = "General"

    return state


def route_decision(state):
    return state["intent"]


def Greeter(state):
    print("Hello! How can I assist you today?")
    return state


def Math(state):
    print("The answer is 2.")
    return state


def General(state):
    print("I'm sorry, I don't understand.")
    return state


graph = StateGraph(RouterStateDict)

graph.add_node("Router", Router)
graph.add_node("Greeter", Greeter)
graph.add_node("Math", Math)
graph.add_node("General", General)

graph.add_edge(START, "Router")

graph.add_conditional_edges(
    "Router",
    route_decision,
    {
        "Greeter": "Greeter",
        "Math": "Math",
        "General": "General"
    }
)

graph.add_edge("Greeter", END)
graph.add_edge("Math", END)
graph.add_edge("General", END)

app = graph.compile()

app.invoke({
    "query": "1+1",
    "intent": ""
})

#app.invoke({
 #   "query": "1+1",
#   "intent": ""
#})
from typing import TypedDict

from langgraph.graph import StateGraph,START,END

class GreeterStateDict(TypedDict):
    name: str

def Cleaner(state):
    input_name = input("Please enter your name: ")
    state["name"] = input_name.title()
    return state

def Greeter(state):
    print(f"Hello, {state['name']},Welocome to AI Lab!")
    return state

builder = StateGraph(GreeterStateDict)
builder.add_node("Cleaner", Cleaner)
builder.add_edge(START, "Cleaner")
builder.add_node("Greeter",Greeter)
builder.add_edge("Cleaner", "Greeter")
builder.add_edge("Greeter", END)
graph = builder.compile()
graph.invoke({"name": ""})


print(graph.get_graph().draw_ascii())

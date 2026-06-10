from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class MemoryChatbotState(TypedDict):
    message: str
    history: list
    response: str


def generate_response(state):

    if "what is my name" in state["message"].lower():

        for msg in state["history"]:

            if "my name is" in msg.lower():

                name = msg.lower().split("my name is")[-1].strip()
                state["response"] = f"Your name is {name}"
                return state

        state["response"] = "I don't know your name yet."

    else:
        state["response"] = "Message stored successfully."

    return state


def store_message(state):

    history = state["history"]

    history.append(state["message"])

    if len(history) > 3:
        history = history[-3:]

    state["history"] = history

    return state


def print_response(state):

    print(state["response"])

    return state


graph = StateGraph(MemoryChatbotState)

graph.add_node("GenerateResponse", generate_response)
graph.add_node("StoreMessage", store_message)
graph.add_node("PrintResponse", print_response)

graph.add_edge(START, "GenerateResponse")
graph.add_edge("GenerateResponse", "StoreMessage")
graph.add_edge("StoreMessage", "PrintResponse")
graph.add_edge("PrintResponse", END)

app = graph.compile()


history = []

result = app.invoke({
    "message": "My name is Vaishnavi.",
    "history": history,
    "response": ""
})

history = result["history"]

result = app.invoke({
    "message": "What is my name?",
    "history": history,
    "response": ""
})
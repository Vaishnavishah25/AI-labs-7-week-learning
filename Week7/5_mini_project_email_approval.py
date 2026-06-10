from typing import TypedDict
from langgraph.graph import StateGraph,START,END

class ApprovalStateDict(TypedDict):
    topic : str
    email : str
    approved : bool

def generate_email(state):
    state["email"] = (
        f"Subject: Request\n\n"
        f"This email is regarding {state['topic']}."
    )
    return state

def approval_node(state):
    print("\nGenerated Email:\n")
    print(state["email"])

    choice = input("\n Approve? (y/n): ")
    state["approved"] = (
        choice.lower() == 'y'
    
    )
    return state


def route_approval(state):
    if state["approved"]:
        return "send"
    
    return "reject"

def send_email(state):
    print("\n Email Sent Successfully!")
    return state

def reject_email(state):
    print("\n Email Rejected.")
    return state

graph = StateGraph(ApprovalStateDict)
graph.add_node("GenerateEmail", generate_email)
graph.add_node("Approval", approval_node)
graph.add_node("SendEmail", send_email)
graph.add_node("RejectEmail", reject_email)
graph.add_edge(START, "GenerateEmail")
graph.add_edge("GenerateEmail", "Approval")
graph.add_conditional_edges(
    "Approval",
    route_approval,
    {
        "send":"SendEmail",
        "reject":"RejectEmail"
    }
)
graph.add_edge("SendEmail", END)
graph.add_edge("RejectEmail", END)

app = graph.compile()
app.invoke({"topic":"Leave Request",
    "email":"",
    "approved":False})
    


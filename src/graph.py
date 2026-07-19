#src/graph.py
from langgraph.graph import START, END, StateGraph

from .state import AgentState
from .nodes import (
    conversation_node,
    search_node,
    response_node,
    validation_node,
)
def validation_route(state: AgentState) -> str:
    if state["is_valid_input"]:
        return "conversation"

    return END

def route(state: AgentState) -> str:
    if state["need_web_search"]:
        return "search"

    return "response"


def build_graph() -> StateGraph:

    builder = StateGraph(AgentState)
    builder.add_node("validation", validation_node)
    builder.add_node("conversation", conversation_node)
    builder.add_node("search", search_node)
    builder.add_node("response", response_node)

    builder.add_edge(START, "validation")
    builder.add_conditional_edges(
    "validation",
    validation_route,
    {
        "conversation": "conversation",
        END: END,
    },
)
    builder.add_conditional_edges(
        "conversation",
        route,
        {
            "search": "search",
            "response": "response",
        },
    )

    builder.add_edge("search", "response")
    builder.add_edge("response", END)

    return builder
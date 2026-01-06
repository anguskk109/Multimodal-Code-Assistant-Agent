# backend/graph/builder.py
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from backend.graph.state import AgentState
from backend.nodes.vision_node import vision_node
from backend.nodes.router_node import router_node
from backend.nodes.python_agent import python_agent_node


def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("router", router_node)
    builder.add_node("vision", vision_node)
    builder.add_node("python", python_agent_node)


    builder.set_entry_point("vision")
    builder.add_edge("vision", "router")
    builder.add_edge("router", "python")
    builder.add_edge("python", END)

    return builder.compile(checkpointer=InMemorySaver())

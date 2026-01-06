# backend\graph\state.py
from typing import TypedDict, Optional, Literal

class AgentState(TypedDict, total=False):
    # Input at start
    query: str
    image_path: Optional[str]
    trace_id: str

    # After vision_node
    problem_text: str

    # After router_node
    intent: Literal["debug", "optimize", "generate"]

    # After python_agent_node
    final_code: str
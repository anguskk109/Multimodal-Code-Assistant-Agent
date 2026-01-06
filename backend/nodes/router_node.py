# backend/nodes/router_node.py
from typing import Dict, Any
import re

from backend.graph.state import AgentState
from backend.tools.logger import agent_logger


# Heuristic keywords per intent
DEBUG_KEYWORDS = [
    "error", "traceback", "crash", "fail", "not defined", "attributeerror",
    "typeerror", "valueerror", "keyerror", "indexerror", "exception",
    "why does this fail", "fix this", "broken", "doesn't work", "debug"
]

OPTIMIZE_KEYWORDS = [
    "optimize", "improve", "faster", "efficient", "refactor", "clean up",
    "best practice", "reduce memory", "speed up", "make it better",
    "performance", "simplify", "elegant"
]

DEBUG_PATTERN = re.compile("|".join(DEBUG_KEYWORDS), re.IGNORECASE)
OPTIMIZE_PATTERN = re.compile("|".join(OPTIMIZE_KEYWORDS), re.IGNORECASE)


@agent_logger("router_node")
def router_node(state: AgentState) -> Dict[str, Any]:
    """
    Deterministic intent classification using keyword heuristics.
    """
    problem_text = state.get("problem_text", "").strip()
    text_lower = problem_text.lower()

    # If error-like keywords → debug
    if DEBUG_PATTERN.search(text_lower):
        intent = "debug"
    # Else if optimization keywords → optimize
    elif OPTIMIZE_PATTERN.search(text_lower):
        intent = "optimize"
    # Default → generate
    else:
        intent = "generate"

    return {"intent": intent}
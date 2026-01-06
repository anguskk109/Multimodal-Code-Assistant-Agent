# backend/tools/logger.py
import logging
import uuid
from typing import Any, Dict

# ------------------------------------------------------
# Basic logger
# ------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(message)s",
)
logger = logging.getLogger("MAA")

def new_trace_id() -> str:
    return str(uuid.uuid4())

# ------------------------------------------------------
# State diff utility (clean and focused)
# --------------------------------------------------

def _summarize_state_changes(old: Dict, new: Dict) -> str:
    """Return concise summary of state updates."""
    updates = {}
    for k, v in new.items():
        if k not in old or old[k] != v:
            # Truncate long strings
            disp = repr(v)
            if len(disp) > 60:
                disp = disp[:57] + "..."
            updates[k] = disp
    if not updates:
        return "no updates"
    return ", ".join(f"{k}={val}" for k, val in updates.items())

# ------------------------------------------------------
# LangGraph Node Decorator
# --------------------------------------------------

def agent_logger(agent_name: str):
    """
    Logs:
      - Input state (relevant keys only)
      - Output state changes
      - (Optional) next node if routing
    """
    def wrapper(func):
        def inner(state: Dict[str, Any]) -> Dict[str, Any]:
            trace_id = state.get("trace_id", "NO-TRACE")
            
            # Log input (only keys that matter)
            input_keys = ["query", "image_b64", "problem_text", "intent", "final_code"]
            input_summary = {
                k: (state[k][:80] + "..." if isinstance(state.get(k), str) and len(state[k]) > 80 else state.get(k))
                for k in input_keys if k in state
            }
            logger.info(f"[{agent_name}] 📥 trace={trace_id} | INPUT: {input_summary}")

            try:
                output = func(state)
            except Exception as e:
                logger.error(f"[{agent_name}] ❌ trace={trace_id} | ERROR: {e}")
                raise

            # Merge output into full new state
            new_state = {**state, **output}

            # Log what changed
            changes = _summarize_state_changes(state, new_state)
            logger.info(f"[{agent_name}] 📤 trace={trace_id} | UPDATED: {changes}")

            # Optional: log routing decision (if this node decides next)
            if "next" in output:
                logger.info(f"[{agent_name}] 🔀 trace={trace_id} | ROUTE TO: {output['next']}")

            # Propagate trace_id
            if "trace_id" not in new_state and "trace_id" in state:
                new_state["trace_id"] = state["trace_id"]

            return new_state
        return inner
    return wrapper
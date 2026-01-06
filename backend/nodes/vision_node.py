# backend/nodes/vision_node.py
from typing import Dict, Any
from pathlib import Path
import base64

from langchain_core.messages import HumanMessage

from backend.graph.state import AgentState
from backend.tools.logger import agent_logger
from backend.models.chatollama import get_vision_model


def _load_image_base64(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Image not found: {path}")
    return base64.b64encode(p.read_bytes()).decode("utf-8")


@agent_logger("vision_node")
def vision_node(state: AgentState) -> Dict[str, Any]:
    query = state.get("query", "").strip()
    image_path = state.get("image_path")

    # Case 1: No image → just return query
    if not image_path:
        return {"problem_text": query}

    # Case 2: Image provided → run VL inference
    try:
        image_b64 = _load_image_base64(image_path)
    except Exception as e:
        return {
            "problem_text": f"{query}\n\n[VISION ERROR]: Failed to load image: {e}"
        }

    vl_model = get_vision_model()
    
    prompt = (
        "You are a helpful coding assistant. "
        "Describe the content of this image clearly and concisely. "
        "If it shows code, extract it exactly. "
        "If it shows a data structure (e.g., tree, graph), describe its structure and values. "
        "If it shows an error, quote the traceback. "
        "Do not add explanations or markdown."
    )

    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}}
        ]
    )

    try:
        response = vl_model.invoke([message])
        visual_description = response.content.strip()
    except Exception as e:
        visual_description = f"[VL_INFERENCE_ERROR: {str(e)}]"

    problem_text = f"{query}\n\n[VISION ANALYSIS]:\n{visual_description}".strip()
    return {"problem_text": problem_text}
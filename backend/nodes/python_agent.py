# backend/nodes/python_agent_node.py
from typing import Dict, Any
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage

from backend.graph.state import AgentState
from backend.models.chatollama import get_brain_model, get_code_model
from backend.tools.logger import agent_logger
from backend.tools.python_tools import (
    DEBUG_TOOLS,
    OPTIMIZE_TOOLS,
    GENERATE_TOOLS,
)

TOOLS_BY_INTENT = {
    "debug": DEBUG_TOOLS,
    "optimize": OPTIMIZE_TOOLS,
    "generate": GENERATE_TOOLS,
}


@agent_logger("python_agent_node")
def python_agent_node(state: AgentState) -> Dict[str, Any]:
    intent = state["intent"]
    problem_text = state["problem_text"]

    tools = TOOLS_BY_INTENT[intent]

    if intent == "generate":
            llm = get_code_model()
            prompt = f"Write Python code that solves this problem:\n\n{problem_text}\n\nRespond with ONLY the code. No explanations."
            response = llm.invoke([HumanMessage(content=prompt)])
            output = response.content.strip()
            return {"final_code": output}

    llm = get_brain_model()

    agent = create_agent(
        model=llm,
        tools=tools,
    )

    task_hint = {
        "debug": "Debug the following Python code.",
        "optimize": "Analyze and optimize the following Python code.",
    }[intent]

    user_prompt = f"""
    {task_hint}
    {problem_text}
    """

    try:
        result = agent.invoke(
            {"messages": [HumanMessage(content=user_prompt)]}
        )
        final_message = result["messages"][-1]
        output = final_message.content.strip()

    except Exception as e:
        output = f"# AGENT ERROR: {str(e)}"

    return {
        "final_code": output
    }

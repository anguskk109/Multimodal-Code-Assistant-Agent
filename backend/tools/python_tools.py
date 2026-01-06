# backend/tools/python_tools.py
from backend.models.chatollama import get_code_model
from langchain.tools import tool
from langchain_core.messages import HumanMessage


# ============================================================
# DEBUG TOOLS
# ============================================================

@tool
def validate_python_syntax(code: str) -> str:
    """
    Check whether the given Python code is syntactically valid.
    Return errors only, no fixes.
    """
    try:
        compile(code, "<string>", "exec")
        return "Syntax OK"
    except SyntaxError as e:
        return f"SyntaxError: {e}"


@tool
def detect_python_errors(code: str) -> str:
    """
    Identify likely logical or runtime bugs in the code.
    Do NOT fix them. List causes and locations.
    """
    llm = get_code_model()
    prompt = f"""
Analyze the following Python code and list:
- logical bugs
- runtime error risks
- incorrect assumptions

Do NOT rewrite the code.
Do NOT suggest fixes.

Code:
{code}
"""
    return llm.invoke(prompt).content


@tool
def explain_failure_trace(trace: str) -> str:
    """
    Explain a Python error trace in plain language.
    Focus on root cause.
    """
    llm = get_code_model()
    prompt = f"""
Explain the following Python error traceback.
Focus on:
- what failed
- why it failed
- where it failed

Traceback:
{trace}
"""
    return llm.invoke(prompt).content


# ============================================================
# OPTIMIZE TOOLS
# ============================================================

@tool
def analyze_time_space_complexity(code: str) -> str:
    """
    Analyze time and space complexity of the code.
    Use Big-O notation.
    """
    llm = get_code_model()
    prompt = f"""
Analyze the time and space complexity of the following Python code.
Use Big-O notation.
Explain briefly.

Code:
{code}
"""
    return llm.invoke(prompt).content


@tool
def suggest_refactorings(code: str) -> str:
    """
    Suggest refactoring ideas without changing behavior.
    No full rewrites.
    """
    llm = get_code_model()
    prompt = f"""
Suggest refactoring improvements for the following Python code.
Rules:
- Preserve behavior
- No full rewrites
- Focus on readability, maintainability, performance

Code:
{code}
"""
    return llm.invoke(prompt).content


# ============================================================
# GENERATE TOOLS
# ============================================================

@tool
def generate_python_code(problem_text: str) -> str:
    """
    generate python code with given problem text
    """

    llm = get_code_model()
    prompt = f"""
Write a complete Python solution for the following problem.

Requirements:
- Output ONLY valid Python code
- Do NOT explain
- Do NOT return JSON
- Use standard LeetCode-style ListNode definition if needed

Problem:
{problem_text}
"""
    return llm.invoke(prompt).content


# ============================================================
# TOOL GROUPS BY INTENT
# ============================================================

DEBUG_TOOLS = [
    validate_python_syntax,
    detect_python_errors,
    explain_failure_trace,
]

OPTIMIZE_TOOLS = [
    analyze_time_space_complexity,
    suggest_refactorings,
    validate_python_syntax,
]

GENERATE_TOOLS = [generate_python_code]

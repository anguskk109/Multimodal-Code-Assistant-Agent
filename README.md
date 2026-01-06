# 🧠 Multimodal Code Assistant Agent

A learning-focused coding assistant that explores how **LangGraph workflows** and **LangChain ReAct agents** can be composed into a **controlled, inspectable** system.

This project represents my **first structured attempt** at combining deterministic graph-based orchestration with scoped agent reasoning for coding tasks.

---

## 🎯 Project Goals

- Practice building **LangGraph-based workflows** with explicit state transitions
- Explore **ReAct-style tool reasoning** in a constrained, realistic setting
- Understand **where agent reasoning helps**
- Understand **where deterministic logic is preferable**

---

## 🧩 High-Level Architecture

The system is organized as a **fixed LangGraph pipeline**, where each node has a single responsibility:


<p align="center">Vision → Intent Routing → Python Agent → Final Output</p>

Key idea:  
**LangGraph controls the flow**, not the LM.

---

## 🧠 Design Philosophy

### Deterministic Control Flow (LangGraph)

The vision → router → Python execution flow is **inherently deterministic** in this system:
there is exactly one correct way to connect these components.

Instead of relying on a ReAct agent to infer or plan this structure, LangGraph is used to encode it explicitly, making the workflow:

- Fixed by construction

- Easy to reason about

- Free from unnecessary agent planning overhead

This choice intentionally reduces the burden on ReAct, reserving agent reasoning for parts of the system that are not deterministic.

### Why ReAct Lives Inside the Python Node

Unlike workflow orchestration, debugging and optimizing Python code are not deterministic:

- The failure mode is ambiguous

- Multiple hypotheses may need to be tested

- Tool usage depends on intermediate observations

For this reason, the Python node itself is implemented as a ReAct-style agent, where iterative reasoning and tool-calling are useful.

In short:

> **LangGraph encodes what is known and fixed.
ReAct handles what is uncertain and exploratory.**

---

## 🗂️ State Design

The workflow operates on a typed, phase-aware state:

- **Input phase**: user query, optional image
- **Vision phase**: normalized problem description
- **Routing phase**: deterministic intent classification
- **Execution phase**: code generation or analysis output


---

## 🤖 Model Roles

Different models are assigned explicit responsibilities in the workflow, instead of overloading one single “smart” model.

- **Reasoning / ReAct (llama3.1)**
Used inside the Python node for ReAct-style reasoning and tool callings.

- **Code (qwen2.5-coder:1.5b)**
Used for Python code related tasks. Lightweight and specialized for code.

- **Vision (qwen3-vl:2b)**
Used in the vision node to extract structured textual descriptions from images 
(code snippets, error messages, data structures).

- **General Purpose (qwen3:1.7b)**
Reserved for fall backs.

---

## 🛠️ Tooling Strategy

Tools are grouped by intent and exposed only when relevant:

- **Debug tools**
  - Syntax validation
  - Error detection
  - Traceback explanation

- **Optimization tools**
  - Time & space complexity analysis
  - Refactoring suggestions

- **Generation**
  - Direct code generation (no agent loop)
---

## 🌐 Interface

- **Backend**: FastAPI + LangGraph
- **Frontend**: Minimal UI for text + optional image input
- Designed for experimentation, tracing, and iteration

---

## 🚂 Try It Out

From the project root, run:
```bash
uvicorn backend.app:app --port 8000
```

You should see output similar to:
```bash
INFO:     Started server process [PID]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

This indicates the FastAPI server and LangGraph workflow are running successfully.
Once the server is running, open your browser and visit:
```bash
http://127.0.0.1:8000
```

### ⚠️ Local Execution Note
This system runs entirely locally using **ChatOllama** (langchain_ollama) and required models (e.g. LLaMA, Qwen) must be downloaded in advance via Ollama before starting the server.

---

## 📌 Lesson Learnt

- How far **structured workflows** can go before agent reasoning is needed
- How ReAct behaves when **intentionally constrained**
- Trade-offs between **determinism vs. flexibility** in agent systems

Sidenotes:

>This repository captures an **early, exploratory stage** of building agentic systems with LangGraph and LangChain, serving as a foundation for future iterations and alternative agent contexts.



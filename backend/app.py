# backend/app.py
import uuid
import shutil
import os
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.graph.builder import build_graph

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = build_graph()


@app.post("/chat")
async def chat(
    text: str = Form(""),
    image: UploadFile | None = None,
):
    image_path = None

    # --- Save image (single image only) ---
    if image:
        image_path = f"/tmp/{uuid.uuid4()}.png"
        with open(image_path, "wb") as f:
            shutil.copyfileobj(image.file, f)

    # --- Initial AgentState ---
    state = {
        "query": text,
        "image_path": image_path,
        "trace_id": str(uuid.uuid4()),
    }

    # --- Run LangGraph ---
    result = graph.invoke(
        state,
        {"configurable": {"thread_id": "ui"}}
    )

    # --- Extract final output ---
    final_code = result.get("final_code", "")

    # --- Cleanup ---
    if image_path:
        try:
            os.remove(image_path)
        except:
            pass

    return {
        "reply": final_code,
        "intent": result.get("intent"),
    }


app.mount(
    "/",
    StaticFiles(directory="frontend", html=True),
    name="frontend",
)

#backend\models\chatollama.py
from langchain_ollama import ChatOllama

def get_brain_model():
    return ChatOllama(model="llama3.1", temperature=0.2)

def get_code_model():
    return ChatOllama(model="qwen2.5-coder:1.5b", temperature=0.1)

def get_vision_model():
    return ChatOllama(model="qwen3-vl:2b", temperature=0.1)

def get_general_model():
    return ChatOllama(model="qwen3:1.7b", temperature=0.1)
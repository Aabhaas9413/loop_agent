import os
from typing import Literal, TypedDict
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field

MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
MAX_REVISIONS = int(os.getenv("MAX_REVISIONS", 2))

model = OpenAI(model_name=MODEL, temperature=0.7, max_tokens=2000, api_key=os.getenv("OPENAI_KEY"))

class State(TypedDict):
    topic: str
    draft: str
    feedback: str
    decision: str
    revision_count: int
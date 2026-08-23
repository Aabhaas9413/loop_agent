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


def writer(state: State) -> State:
    """Agent 1: creates the first answer draft based on the topic."""
    response = model.invoke(
        [
            {
                "role": "system",
                "content": "You are a helpful beginner friendly teacher, explain the topic in 150 to 160 words. Use simple language"
            },
            {
                "role": "user",
                "content": f"Write a draft for the following topic: {state['topic']}",
            },
        ]
    )
    return {
        "draft": response.choices[0].message.content,
        "feedback": "",
        "decision": "",
        "revision_count": 0,
    }
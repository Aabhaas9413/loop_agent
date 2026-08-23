import os
from typing import Literal, TypedDict
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field

MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
MAX_REVISIONS = int(os.getenv("MAX_REVISIONS", 2))

model = OpenAI(model_name=MODEL, temperature=0.7, max_tokens=2000, api_key=os.getenv("OPENAI_KEY"))

class Review(BaseModel):
    decision: Literal["Pass", "Revise"] = Field(
         description="PASS only of the answer satisfy the review rule; othervise REVISE."
         )
    feedback: str = Field(
         description="Short, specific feedback. Empty string when decision is PASS."
         )

reviewer_model = model.with_structured_output(Review)    

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

def reviewer(state: State):
    """Agent 2: reviews the draft and provides feedback."""
    review = reviewer_model.invoke(
        [
            {
                "role": "system",
                "content": "You are a helpful beginner friendly teacher, explain the topic in 150 to 160 words. Use simple language"
            },
            {
                "role": "user",
                "content": f"Review the following topic: {state['topic']} and provide feedback for both the question and the answer: {state['draft']}",
            },
        ]
    )
    return {
        "decision": review.desicion,
        "feedback": review.feedback
    }    
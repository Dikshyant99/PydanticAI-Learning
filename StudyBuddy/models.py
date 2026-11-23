"""Data models: what the data looks like.

Later, FastAPI request/response models go here too
(e.g. ChatRequest, ChatResponse, AssignmentCreate).
"""
from datetime import date

from pydantic import BaseModel


#What one assignment looks like
class Assignment(BaseModel):
    title: str
    subject: str
    due_date: date
    done: bool = False  # Every new assignment starts as not done

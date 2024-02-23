# -*- coding: utf-8 -*-

"""
File: models.py
Author: Dartrisen
Description: models for the Groq API.
"""
from typing import Optional

from pydantic import BaseModel


class Stats(BaseModel):
    time_generated: float
    tokens_generated: int
    time_processed: float
    tokens_processed: int


class Chat(BaseModel):
    content: str
    request_id: Optional[str]
    stats: Stats

from pydantic import BaseModel
from typing import Optional


class Stats(BaseModel):
    time_generated: float
    tokens_generated: int
    time_processed: float
    tokens_processed: int


class Chat(BaseModel):
    content: str
    request_id: Optional[str]
    stats: Stats

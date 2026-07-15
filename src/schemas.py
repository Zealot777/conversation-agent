#src/schemas.py
from pydantic import BaseModel, Field
from typing import Literal

class ConversationOutput(BaseModel):
    
    feedback: str | None = Field(
        default=None,
        description=(
        "Feedback written ONLY in Korean. "
        "Never English. Never Japanese except short examples."
        )
        
    )
    response_mode: Literal["normal", "unusual"]
    
    need_web_search: bool = Field(
        description="Whether external information is required."
    )

    search_query: str | None = Field(
        default=None,
        description="Search query when web search is required."
    )
    feedback_types: list[str] = Field(
        description="Type of feedback, if there's no feedback then return []."
    )
    
class ResponseOutput(BaseModel):
    reply: str = Field(
        description="Natural Japanese reply."
    )

#src/schemas.py
from pydantic import BaseModel, Field


class ConversationOutput(BaseModel):
    
    feedback: str | None = Field(
        default=None,
        description=(
        "Feedback written ONLY in Korean. "
        "Never English. Never Japanese except short examples."
        )
        
    )

    need_web_search: bool = Field(
        description="Whether external information is required."
    )

    search_query: str | None = Field(
        default=None,
        description="Search query when web search is required."
    )
    
class ResponseOutput(BaseModel):
    reply: str = Field(
        description="Natural Japanese reply."
    )
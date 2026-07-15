#src/state.py
from typing import Optional, TypedDict, Literal


class AgentState(TypedDict):
    user_input: str
    reply: Optional[str]
    feedback: Optional[str]
    feedback_types:list[str]
    response_mode : Literal["normal", "unusual"]
    need_web_search: bool
    search_query: Optional[str]
    search_result: Optional[str]

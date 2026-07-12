#src/state.py
from typing import Optional, TypedDict


class AgentState(TypedDict):
    user_input: str

    reply: Optional[str]
    feedback: Optional[str]

    need_web_search: bool
    search_query: Optional[str]
    search_result: Optional[str]

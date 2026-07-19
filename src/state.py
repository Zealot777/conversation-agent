#src/state.py
from typing import Optional, TypedDict, Literal, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    user_input: str
    reply: Optional[str]
    feedback: Optional[str]
    feedback_types:list[str]
    response_mode : Literal["normal", "unusual"]
    need_web_search: bool
    search_query: Optional[str]
    search_result: Optional[str]
    messages: Annotated[list[BaseMessage], add_messages]
    is_valid_input: bool
    error_message : Optional[str]

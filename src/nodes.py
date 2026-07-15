#nodes.py
from langchain_openai import ChatOpenAI
from .tools import search_tool
from .prompts import CONVERSATION_PROMPT, NORMAL_RESPONSE_PROMPT, UNUSUAL_RESPONSE_PROMPT
from .schemas import ConversationOutput, ResponseOutput
from .state import AgentState


llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

conversation_llm = llm.with_structured_output(ConversationOutput)
response_llm = llm.with_structured_output(ResponseOutput)


def conversation_node(state: AgentState) -> dict:
    """
    Analyze user input.

    - Grammar check
    - Feedback generation
    - Decide whether web search is needed
    """

    raw = conversation_llm.invoke(
        [
            ("system", CONVERSATION_PROMPT),
            ("human", state["user_input"]),
        ]
    )
    result = ConversationOutput.model_validate(raw)
    return {
        "feedback": result.feedback,
        "need_web_search": result.need_web_search,
        "search_query": result.search_query,
        "feedback_types": result.feedback_types,
        "response_mode": result.response_mode,
    }


def search_node(state: AgentState) -> dict:
    """
    Execute web search.
    """

    if not state["search_query"]:
        return {
            "search_result": None,
        }

    result = search_tool.invoke(state["search_query"])

    return {
        "search_result": result,
    }


def response_node(state: AgentState) -> dict:
    """
    Generate the final reply.
    """

    human_message = f"""
    User Input:
    {state["user_input"]}
    """
    if state.get("search_result"):
        human_message += f"""
    Search Result:
    {state.get("search_result")}
    """
    if state["response_mode"] == "normal":
        prompt = NORMAL_RESPONSE_PROMPT
    else:
        prompt = UNUSUAL_RESPONSE_PROMPT
    raw = response_llm.invoke(
        [
            ("system", prompt),
            ("human", human_message),
        ]
    )
    result = ResponseOutput.model_validate(raw)

    return {
        "reply": result.reply,
    }
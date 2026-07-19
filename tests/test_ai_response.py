#tests/test_ai_response.py
import pytest
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from src.graph import build_graph
RESPONSE_JUDGE_PROMPT = """
You are an impartial evaluator.

Evaluate ONLY the assistant's Japanese reply.

Assume that grammar feedback is handled by another agent.

The assistant's job is conversation only.

Evaluate the following categories.

1. Naturalness

- Does the reply sound like something a native Japanese speaker would say?
- Is it grammatically natural?
- Is it fluent?
- The reply should be written in Japanese unless explicitly requested otherwise.

Score from 1 to 5.

Provide a short reason.


2. Conversation Continuity

Evaluate whether the reply naturally continues the user's conversation.

The assistant should:

- respond to the user's intention
- maintain the conversation
- avoid changing the topic unnecessarily

Score from 1 to 5.

Provide a short reason.


3. Response Mode

Evaluate whether the reply matches the requested response_mode.

NORMAL mode:

- Ignore minor grammar mistakes.
- Continue the conversation naturally.
- Focus on the intended meaning.

UNUSUAL mode:

- react to impossible or strange statements
- express surprise or confusion naturally
- ask for clarification when appropriate
- do NOT normalize impossible statements

Score from 1 to 5.

Provide a short reason.

4. Avoiding Implicit Correction

Evaluate whether the assistant avoided silently correcting the user's Japanese.

Score 5

- No grammar rewriting
- No vocabulary rewriting
- No kanji rewriting
- No register rewriting

Score 1

- The assistant rewrote or normalized the user's Japanese without telling them.

Ignore wording differences.

Focus on conversational quality.

Return ONLY JSON.

"""
class ResponseJudgeOutput(BaseModel):

    naturalness_score: int = Field(ge=1, le=5)
    naturalness_reason: str

    continuity_score: int = Field(ge=1, le=5)
    continuity_reason: str

    response_mode_score: int = Field(ge=1, le=5)
    response_mode_reason: str

    implicit_correction_score: int = Field(ge=1, le=5)
    implicit_correction_reason: str
app = build_graph().compile()

judge_llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
).with_structured_output(ResponseJudgeOutput)

@pytest.mark.parametrize(
    "user_input",
    [
        
    "こんにちは！",
    "昨日映画を見ます。",          # grammar
    "今日は寿司に食べます。",      # grammar
    "今日はHappyです。",          # vocabulary
    "今日は免強します。",          # kanji
    "昨日寿司に食べられた。",      # semantic
    "太陽が寿司を食べられた。",    # semantic
    "キーボードが大学を卒業しました。", # semantic
    "東京の今日の天気は？",        # web
    "東京の今日のニュースは？",    # web
    "今日は寿司が食べたい。",      # perfect

    ]
)


def test_ai_response(user_input):

    result = app.invoke(
        {
            "user_input": user_input
        }
    )

    judge_input = f"""
            User input:
            {user_input}

            feedback:
            {result["feedback"]}
            
            feedback_types:
            {result["feedback_types"]}
            
            Assistant reply:
            {result["reply"]}

            Response mode:
            {result["response_mode"]}
            """

    raw = judge_llm.invoke(
        [
            ("system", RESPONSE_JUDGE_PROMPT),
            ("human", judge_input),
        ]
    )
    judge = ResponseJudgeOutput.model_validate(raw)
    assert judge.naturalness_score >= 4, (judge.naturalness_reason
    )
    assert judge.continuity_score >= 4, (
        judge.continuity_reason
    )

    assert judge.response_mode_score >= 4, (
        judge.response_mode_reason
    )
    assert judge.implicit_correction_score >= 4, (
    judge.implicit_correction_reason
)
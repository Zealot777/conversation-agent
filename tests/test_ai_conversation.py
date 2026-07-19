#tests/test_ai_conversation.py
from dotenv import load_dotenv
load_dotenv()
import pytest
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from src.graph import build_graph
JUDGE_PROMPT = """
You are an impartial evaluator.

Evaluate ONLY the output of the Conversation Node.

If there is no 
- grammar issue,
- vocabulary issue,
- kanji issue,
- register issue,
- semantic issue,

feedback SHOULD be null.

Do NOT penalize missing feedback in this case.

Ignore web search decisions.
They are tested separately.

Evaluate the following three categories.

1. Feedback Quality

Evaluate whether:

- The feedback correctly identifies the user's mistake.
- The explanation is technically accurate.
- The feedback is concise.
- The feedback is written entirely in Korean.
- Japanese examples are included only when helpful.

Give a score from 1 to 5.

Also provide a short reason.


2. Feedback Classification

Evaluate whether:

- feedback_types correctly classify every detected issue.
- Multiple issues are all included when necessary.
- No unnecessary types are added.

Give a score from 1 to 5.

Also provide a short reason.


3. Response Mode

Evaluate whether:

- response_mode is appropriate.
Use NORMAL when:

- the intended meaning is understandable,
- even if grammar, vocabulary, kanji, or register problems exist.

Use UNUSUAL when:

- the sentence itself is semantically impossible,
- or the intended meaning cannot reasonably be inferred.

Give a score from 1 to 5.

Also provide a short reason.


Scoring Guide

5 = Excellent

4 = Good

3 = Acceptable but imperfect

2 = Incorrect

1 = Completely wrong


Ignore wording differences.

Focus on correctness rather than writing style.

Return ONLY JSON with the following fields:

feedback_score
feedback_reason

feedback_types_score
feedback_types_reason

response_mode_score
response_mode_reason
"""

class ConversationJudgeOutput(BaseModel):
    feedback_score: int = Field(ge=1, le=5)
    feedback_reason: str

    feedback_types_score: int
    feedback_types_reason: str

    response_mode_score: int
    response_mode_reason: str

    
app = build_graph().compile()

judge_llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
).with_structured_output(ConversationJudgeOutput)

@pytest.mark.parametrize(
    "user_input",
    [
        "こんにちは！",
        "今日は寿司に食べます。",
        "今日はHappyです。",
        "昨日寿司に食べられた。",
        "東京の今日の天気は？",
        "キーボードが大学を卒業しました。",

    ]
)


def test_ai_conversation(user_input):

    result = app.invoke(
        {
            "user_input": user_input
        }
    )

    judge_input = f"""
                feedback:
                {result["feedback"]}

                feedback_types:
                {result["feedback_types"]}

                response_mode:
                {result["response_mode"]}

                Expected responsibilities:
                - Detect grammar errors.
                - Detect unnatural vocabulary.
                - Detect incorrect or unnatural Kanji usage.
                - Detect register problems.
                - Detect semantic inconsistencies.
                - Assign one or more feedback_types.
                - Select the appropriate response_mode.
                """

    raw = judge_llm.invoke(
        [
            ("system", JUDGE_PROMPT),
            ("human", judge_input),
        ]
    )
    judge = ConversationJudgeOutput.model_validate(raw)
    assert judge.feedback_score >= 4, judge.feedback_reason

    assert judge.feedback_types_score >= 4, (
        judge.feedback_types_reason
    )

    assert judge.response_mode_score >= 4, (
        judge.response_mode_reason
    )
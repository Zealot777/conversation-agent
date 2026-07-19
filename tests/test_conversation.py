#tests/test_conversation.py
from src.graph import build_graph

import pytest

app = build_graph().compile()

@pytest.mark.parametrize(
    "user_input,has_feedback,expected_response_mode,need_web_search",[
        (
            "こんにちは！",
            False,
            "normal",
            False,
        ),

        (
            "私は学生です。",
            False,
            "normal",
            False,
        ),

        (
            "今日は寿司に食べます。",
            True,
            "normal",
            False,
        ),

        (
            "今日はHappyです。",
            True,
            "normal",
            False,
        ),

        (
            "昨日机に食べられた。",
            True,
            "unusual",
            False,
        ),

        (
            "太陽がコーヒーを飲んだ。",
            True,
            "unusual",
            False,
        ),

        (
            "キーボードが大学を卒業しました。",
            True,
            "unusual",
            False,
        ),


        (
            "今日の東京の天気は？",
            False,
            "normal",
            True,
        ),

        (
            "今日のドル円は？",
            False,
            "normal",
            True,
        ),

        (
            "今日のニュースを教えて。",
            False,
            "normal",
            True,
        ),

        (
            "昨日は寿司を食べました。とても美味しかったです。",
            False,
            "normal",
            False,
        ),

        (
            "今日はHappyに食べます。",
            True,
            "normal",
            False,
        ),


    ]
)

def test_conversation(user_input,
    has_feedback,
    expected_response_mode,
    need_web_search,):
    result = app.invoke(
        {
            "user_input" : user_input
        }
    )
    assert (result["feedback"] is not None) == has_feedback
    assert result["response_mode"] == expected_response_mode
    assert result["need_web_search"] == need_web_search
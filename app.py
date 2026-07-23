#app.py
import streamlit as st
from src.graph import build_graph
from langgraph.checkpoint.memory import MemorySaver

st.set_page_config(
    page_title="Japanese Conversation Agent",
    page_icon="🇯🇵",
    layout="centered",
)
st.markdown("""
<style>
/* 전체 배경 */
.st-emotion-cache-1r4qj8v{
    background:#FBEFEF; 
}
.st-emotion-cache-1up3yna{
    background:#FBEFEF;
}
.st-emotion-cache-16hesyz{
    background: #c5b3d3;
}
.st-emotion-cache-128upt6{
    background:#FBEFEF;
}
.stAppBottom {
    background: #F5CBCB;
}

/* 제목 */
.main-title{
    
    text-align:center;
    color:#8B0000;
    font-size:42px;
    font-weight:700;
    margin-bottom:8px;
}

/* 설명 박스 */
.intro-box{
    border-left:8px solid #c0392b;
    border-radius:12px;
    padding:18px;
    margin-bottom:20px;
    box-shadow:0 2px 8px rgba(0,0,0,0.08);
}

.intro-title{
    font-size:24px;
    font-weight:bold;
    color:#222;
    margin-bottom:12px;
}

.intro-text{
    font-size:18px;
    color:#222;
    line-height:1.8;
}
/* 채팅 박스*/
.st-emotion-cache-6mn6c9{
    background-color: #FFE2E2;
}
/* 사이드바 영역*/
.st-emotion-cache-1kss9tm{
        background-color: #FFE2E2;
}
.st-emotion-cache-su9zec{
    background-color:#f5cbcb;
}
.st-emotion-cache-1fee4w7{
    background-color: #f4e8ff;
}
/* 피드백 박스 */
div[data-testid="stInfo"]{
    font-size:17px;
}

/* 채팅 입력창 */
div[data-testid="stChatInput"]{
    
    border-top:2px solid #c0392b;
    padding-top:12px;
}

div[data-testid="stBottom"]{
    background:#FBEFEF !important;
}
@media @media (prefers-color-scheme: dark) {
  /* 다크 모드에 적용할 스타일 정의 */
    .main-title{
    
    text-align:center;
    color:#8B0000;
    font-size:42px;
    font-weight:700;
    margin-bottom:8px;
}

}
</style>
""", unsafe_allow_html=True)
memory = MemorySaver()

graph = build_graph().compile(
    checkpointer=memory
)

st.title("일본어로 말해봐요!")

st.markdown(
    """
일본어로 자유롭게 대화해 보세요!

- 여러분이 어떤 이상한 말을 하더라도 자연스럽게 대화를 이어갑니다.
- 문법 / 어휘 / 한자 / 경어(Register)를 한국어로 피드백합니다.
- 최신 정보가 필요한 질문은 자동으로 검색합니다.
"""
)

# ----------------------------
# Sidebar
# ----------------------------

with st.sidebar:

    st.header("📖 사용 방법")

    st.markdown("""
1. 일본어를 입력하세요.

2. AI와 자연스럽게 대화하세요.

3. 오류가 있으면 한국어 피드백을 제공합니다.

4. 최신 정보는 자동 검색합니다.
""")

    st.divider()

    st.markdown("### ⚠️ 입력 안내")

    st.info(
        "이 에이전트는 일본어 학습용입니다.\n\n"
        "일본어 문장을 입력해주세요."
    )

    st.divider()

    if st.button("🗑️ 대화 초기화"):
        st.session_state.messages = []
        st.rerun()

# ----------------------------
# Example
# ----------------------------

with st.expander("💡 예시 입력"):

    st.markdown(
"""
- こんにちは！
- 今日は寿司に食べます。
- 今日の東京の天気は？
- 太陽がコーヒーを飲んだ。
- 社長、腹減った。
"""
)

# ----------------------------
# Chat history
# ----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

thread_id = "conversation"

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])
        

# ----------------------------
# Chat
# ----------------------------

prompt = st.chat_input("일본어를 입력하세요. (예: こんにちは！)")

if prompt:
    
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.write(prompt)

    with st.spinner("답변을 생성하는 중입니다..."):

        try:

            result = graph.invoke(
                {
                    "user_input": prompt,
                },
                config={
                    "configurable": {
                        "thread_id": thread_id
                    }
                }
            )
        except Exception:

            st.error(
                "답변을 생성하는 중 오류가 발생했습니다.\n\n잠시 후 다시 시도해 주세요."
            )
            st.stop()
    if not result["is_valid_input"]:
        st.error(result["error_message"])
        st.stop()
    
    reply = result["reply"]

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reply,
        }
    )

    with st.chat_message("assistant"):

        st.write(reply)

        if result["feedback"]:

            with st.expander("📝 학습 피드백"):

                st.info(result["feedback"])

        else:

            st.success("이번 문장은 특별한 문제가 발견되지 않았습니다.")
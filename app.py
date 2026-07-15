import streamlit as st
from src.graph import build_graph
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()

graph = build_graph().compile(
    checkpointer=memory
)

st.title("Japanese Conversation Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

thread_id = "conversation"

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("메시지를 입력하세요."):

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.write(prompt)

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

        st.info(result["feedback"])
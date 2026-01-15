import streamlit as st

from langchain_openai import ChatOpenAI
# 오픈AI 모델을 사용하는 랭체인 챗봇 클래스
from langchain_core.chat_history import InMemoryChatMessageHistory
#메모리에 대화 기록을 저장하는 클래스
from langchain_core.runnables.history import RunnableWithMessageHistory
#메시지 기록을 활용해 실행가능한 wrapper 클래스
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))

st.title("Simple Chatbot")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        SystemMessage(content="너는 사용자를 도와주는 상담사야."),
    ]

#세션별 대화 기록을 저장할 딕셔너리 대신 session_state를 사용함
if "store" not in st.session_state:
    st.session_state["store"] = {}

def get_session_history(session_id: str):
    if session_id not in st.session_state["store"]:
        st.session_state["store"][session_id] = InMemoryChatMessageHistory()
    return st.session_state["store"][session_id]

llm = ChatOpenAI(model="gpt-4o-mini")
with_message_history = RunnableWithMessageHistory(llm, get_session_history)

config = {"configurable": {"session_id": "abc2"}}

#스트림릿 화면에 메시지 출력
for msg in st.session_state.messages:
    if msg:
        if isinstance(msg, SystemMessage):
            st.chat_message("system").write(msg.content)
        elif isinstance(msg, AIMessage):
            st.chat_message("assistant").write(msg.content)
        elif isinstance(msg, HumanMessage):
            st.chat_message("user").write(msg.content)

if prompt := st.chat_input():
    print('user:', prompt)
    st.session_state.messages.append(HumanMessage(prompt))
    st.chat_message("user").write(prompt)

    response = with_message_history.stream([HumanMessage(prompt)], config=config)

    ai_response_bucket = None
    with st.chat_message("assistant").empty():
        for r in response:
            if ai_response_bucket is None:
                ai_response_bucket = r
            else:
                ai_response_bucket += r
            print(r.content, end='')
            st.markdown(ai_response_bucket.content)
    
    msg = ai_response_bucket.content
    st.session_state.messages.append(ai_response_bucket)
    print('assistant:', msg)
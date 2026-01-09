from openai import OpenAI
from dotenv import load_dotenv
from gpt_functions_more import tools, get_current_time, get_yf_stock_info, get_yf_stock_history, get_yf_stock_recommendations
import os
import json
import streamlit as st
from collections import defaultdict

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def tool_list_to_obj(tools):
    tool_calls_dict = defaultdict(lambda: {"id":None, "function":{"arguments":"", "name":None}, "type":None})

    for tool in tools:
        if tool_call.id is not None:
            tool_calls_dict[tool_call.index]["id"] = tool_call.id
        
        if tool_call.function.name is not None:
            tool_calls_dict[tool_call.index]["function"]["name"] = tool_call.function.name

        tool_calls_dict[tool_call.index]["function"]["arguments"] = tool_call.function.arguments
        
        if tool_call.type is not None:
            tool_calls_dict[tool_call.index]["type"] = tool_call.type
    
    tool_calls_list = list(tool_calls_dict.values())

    return tool_calls_list
    

#AI 응답 생성 함수
#GPT가 응답을 한번에 내놓지 않고, 중간중간 값을 내보냄냄
def get_ai_response(messages, tools=None, stream=True):
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        stream = stream,
        messages = messages,
        tools = tools,
    )

    if stream:
        for chunk in response:
            yield chunk
    else:
        return response

st.title("주식도 잘 알려주는 챗봇")

# 초기 시스템 메세지 설정
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "너는 사용자를 도와주는 상담사야."},
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if user_input := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    ai_response = get_ai_response(st.session_state.messages, tools=tools) # AI 응답 생성

    #작은 단위의 글을 출력하기 위해 코드 추가
    content=''
    tool_calls = None
    tool_calls_chunk = []

    with st.chat_message("assistant").empty():
        for chunk in ai_response:
            content_chunk = chunk.choices[0].delta.content
            if content_chunk:
                print(content_chunk, end="")
                content += content_chunk
                st.markdown(content)
            
            if chunk.choices[0].delta.tool_calls:
                tool_calls_chunk += chunk.choices[0].delta.tool_calls
        
        tool_obj = tool_list_to_obj(tool_calls_chunk)
        tool_calls = tool_obj["tool_calls"]

        if len(tool_calls) > 0:
            print(tool_calls)

            tool_call_msg = [tool_call["function"] for tool_call in tool_calls]
            st.write(tool_call_msg)
    
    print('\n=============================')
    print(content)

    tool_obj = tool_list_to_obj(tool_calls_chunk)
    tool_calls = tool_obj["tool_calls"]
    print(tool_calls)
 # 툴 호출 여부 확인
    if tool_calls:
        for tool_call in tool_calls:
            tool_name = tool_call.function.name # 호출된 함수 이름
            tool_call_id = tool_call.id # 호출 ID

            arguments = json.loads(tool_call.function.arguments)

            # 시간 함수 호출 시 처리
            if tool_name == "get_current_time":
                function_result = get_current_time(timezone=arguments['timezone'])
            
            elif tool_name == "get_yf_stock_info":
                function_result = get_yf_stock_info(ticker=arguments['ticker'])
            
            elif tool_name == "get_yf_stock_history":
                function_result = get_yf_stock_history(ticker=arguments['ticker'], period=arguments['period'])
            
            elif tool_name == "get_yf_stock_recommendations":
                function_result = get_yf_stock_recommendations(ticker=arguments['ticker'])
            
            st.session_state.messages.append({
                "role": "function",
                "tool_call_id": tool_call_id,
                "name": tool_name,
                "content": function_result,
            })
        st.session_state.messages.append({"role": "system", "content": "이제 주어진 결과를 바탕으로 답변할 차례다."})
        
        ai_response = get_ai_response(st.session_state.messages) # 도구 결과 반영 후 재응답
        content = ""
        with st.chat_message("assistant").empty():
            for chunk in ai_response:
                content_chunk = chunk.choices[0].delta.content
                if content_chunk:
                    print(content_chunk, end="")
                    content += content_chunk
                    st.markdown(content)

    st.session_state.messages.append({
        "role": "assistant",
        "content":content,
    })

    print("AI\t:",content)
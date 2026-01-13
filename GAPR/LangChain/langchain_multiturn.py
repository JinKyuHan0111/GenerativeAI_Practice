from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI(model = "gpt-4o-mini")

messages = [
    SystemMessage(content = "너는 사용자를 도와주는 상담사야."),
]

while True:
    user_input = input("사용자: ")
    if user_input == "exit":
        break

    messages.append(
        HumanMessage(user_input)
    )#사용자 메시지를 대화 기록에 추가함

    ai_response = llm.invoke(messages)

    messages.append(
        ai_response
    )#대화 기록에 AI 메시지를 추가함

    print("AI: ", ai_response.content)
    #AI의 응답을 출력함
    
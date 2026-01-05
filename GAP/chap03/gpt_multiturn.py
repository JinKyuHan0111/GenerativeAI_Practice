from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=api_key)

def get_ai_response(messages):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.9,
        messages=messages, #대화 기록을 입력으로 전달
    )
    return response.choices[0].message.content #생성된 응답 내용 반환

messages = [
    {"role": "system", "content": "너는 사용자의 비서야."},
] #초기 대화 기록 설정

while True:
    user_input = input("사용자: ")

    if user_input == "exit":
        break
    
    messages.append({"role": "user", "content": user_input}) #사용자 메세지를 messages에 덧붙임
    ai_response = get_ai_response(messages) #대화 기록을 기반으로 AI 응답을 가져옴
    messages.append({"role": "assistant", "content": ai_response}) #GPT의 응답을 messages에 덧붙임
    print("AI: ", ai_response)
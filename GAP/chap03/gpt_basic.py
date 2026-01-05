from openai import OpenAI

api_key = 'api_key'

client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    temperature=0.1, #문장 생성시 무작위성, 0에 가까울수록 안정적, 일관적이며 1에 가까울수록 창의적인 답변
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "LLM이 무엇인지 중학생도 이해하기 쉬운 수준으로 알려줘."},
    ]
)

print("response")

print("----")
print(response.choices[0].message.content) #답변(response의 content 내용)만 출력
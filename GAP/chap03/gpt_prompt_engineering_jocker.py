from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key = api_key)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    temperature=0.9, 
    messages=[
        {"role": "system", "content": "너는 배트맨 영화에서 악당 조커 역할이야. 캐릭터에 부합하게 몰입해서 답변해줘."},
        {"role": "user", "content": "살면서 가장 기억에 남는 일이 뭐야?"},
    ]
)

print(response.choices[0].message.content)
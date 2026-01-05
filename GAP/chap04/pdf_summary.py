from openai import OpenAI
from dotenv import load_dotenv
import os

import pymupdf

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

def pdf_to_text(pdf_file_path: str):
    pdf_file_path = "GAP/data/example.pdf"
    doc = pymupdf.open(pdf_file_path)#PDF 파일을 열어 문서 객체(doc)로 생성

    header_height = 80 # 페이지 상단(헤더) 영역 높이, 필요시 직접 조정
    footer_height = 80 # 페이지 하단(푸터) 영역 높이, 필요시 직접 조정

    full_text = ''

    for page in doc: # 문서 객체(doc)의 각 페이지를 반복
        rect = page.rect # 현재 페이지의 사이즈(Rect 객체, width/height)

        # 상단 header 영역 텍스트 추출(clip: 좌상단에서 header_height까지)
        header = page.get_text(clip=(0, 0, rect.width, header_height))
        # 하단 footer 영역 텍스트 추출(clip: 좌하단에서 footer_height 범위)
        footer = page.get_text(clip=(0, rect.height - footer_height, rect.width, rect.height))
        # 중앙 본문 영역(헤더/푸터 제외) 텍스트 추출
        text = page.get_text(clip=(0, header_height, rect.width, rect.height - footer_height))

        #추출한 본문 텍스트를 덧붙이면서, 페이지 구분선을 추가함
        full_text += text + '\n--------------------------------\n'

    pdf_file_name = os.path.basename(pdf_file_path)
    pdf_file_name = os.path.splitext(pdf_file_name)[0]

    txt_file_path = f"./GAP/data/{pdf_file_name}_with_preprocessing.txt"

    with open(txt_file_path, 'w', encoding='utf-8') as f:
        f.write(full_text)
    return txt_file_path

def summarize_txt(file_path: str):
    client = OpenAI(api_key=api_key)

    with open(file_path, 'r', encoding='utf-8') as f:
        txt = f.read()

    system_prompt = f'''
    너는 다음 글을 요약하는 봇이다. 아래 글을 읽고, 저자의 문제 인식과 주장을 파악하고, 주요 내용을 요약하라.

    작성해야 하는 포맷은 다음과 같다.
    
    # 제목

    ## 저자의 문제 인식 및 주장(15문장 이내)

    ## 저자 소개


    ================ 이하 텍스트 ================

    {txt}
    '''

    print(system_prompt)
    print('================================')

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.1,
        messages=[
            {"role": "system", "content": system_prompt},
        ]
    )
    return response.choices[0].message.content

def summarize_pdf(pdf_file_path: str, output_file_path: str):
    text_file_path = pdf_to_text(pdf_file_path)
    summary = summarize_txt(text_file_path)

    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(summary)

if __name__ == '__main__':
    pdf_file_path = 'GAP/data/example.pdf'
    output_file_path = 'GAP/data/example_summary2.txt'
    summarize_pdf(pdf_file_path, output_file_path)
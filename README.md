# GenerativeAI_Practice

생성형AI를 다루고 실질적으로 원하는 생성형 AI만들기를 위한 연습

#사용 언어

python (3.12.9 ver)

# install 항목

pip install openai==1.58.1

pip install python-dotenv

pip install streamlit==1.41.1 (streamlit 사용)

pip install PyMuPDF (PDF파일 전처리용)

pip install yfinance(야후 파이낸스 가져오는 라이브러리)

# 가상 환경 활성화(터미널 창에 입력)

.\GAP\Scripts\activate

    위의 방법이 안될시
    1. powershell 관리자 권한 실행
    2. Set-ExecutionPolicy-ExecutionPolicy RemoteSigned-Scope CurrentUser 입력 후 실행
    3. get-ExecutionPolicy 입력시 "RemoteSigned" 나오면 다시 활성화 시도

#Run 방법

기본적인 .py 파일 => python (파일위치)/(파일명).py

steamlit 구동 => streamlit run (파일명).py

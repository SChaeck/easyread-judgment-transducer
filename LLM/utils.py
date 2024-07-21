### 환경변수 로드 ###
from dotenv import load_dotenv
import logging

load_dotenv()

### 로깅 설정 ###
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

### 쉬운 판결문 변환 ###
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import pandas as pd
import os

# et: easy translate
# 너는 복잡하고 어려운 판결문들을 정보 약자나, 발달장애인이 이해할 수 있도록 변환해주는 쉬운 판결문 변환기다. 아래에 제시되는 판결문을 명령에 따라 읽기 쉽게 바꿔라.
#아래 판결문을 다음과 같이 순서대로 정리하라 단, 한 문장에서 쉼표는 한 번만 사용해야 한다. 누락된 내용이 없어야 한다.
et_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "형식 유지 변환기"
        ),
        (   
            "human",
            """### 명령: 형식 유지
            
legal_terminology: 모든 법률용어와 그것의 국어적 의미
same_form_judgment: 동사만 쉽게 바꾼 판결문 내용. 구분할 수 있는 문장은 최대한 구분해야 한다.
very_easy_judgment: 법률용어를 사용하지 않고 어린아이에게 설명하듯이 쉽고 자세하게 변환된 판결문 내용. 단, 번호를 비롯한 전체 내용 형식이 제시한 판결문과 동일해야 한다. 

### 판결문:
{judgment}

### 출력양식:
{{
    "legal_terminology": {{}},
    "same_judgment": "",
    "very_easy_judgment": ""
}}"""
        )
    ]
)

et_llm = ChatOpenAI(temperature=0.1, model="gpt-4o-mini")
et_chain = et_prompt | et_llm

def easy_translate(judgment, index, total):
    response = et_chain.invoke(judgment)
    et_judgment = response.content
    logger.info(f"변환 완료: {index + 1}/{total}")
    return et_judgment

def preprocess_judgments(csv_file):
    df = pd.read_csv(csv_file)
    total = len(df)
    
    # 각 판결문에 대해 변환 수행 및 text2 열에 저장
    df['text2'] = [easy_translate(judgment, i, total) for i, judgment in enumerate(df['text'])]
    
    return df

### 메인함수 ###
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(current_dir, '../data/test.csv')

    logger.info("메인 함수 시작")
    translated_df = preprocess_judgments(csv_file)
    translated_df.to_csv(csv_file, index=False)  # 원래 파일에 덮어쓰기
    logger.info("CSV 파일 저장 완료: %s", csv_file)

    print("변환 작업이 완료되었습니다.")

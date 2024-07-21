### 환경변수 로드 ###
from dotenv import load_dotenv

load_dotenv()

### 쉬운 판결문 변환 ###
from langchain_core.prompts import ChatPromptTemplate
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

def easy_translate(judgment):
    response = et_chain.invoke(judgment)
    et_judgment = response.content
    return et_judgment

def preprocess_judgments(csv_file):
    df = pd.read_csv(csv_file)
    
    # 각 판결문에 대해 변환 수행 및 text2 열에 저장
    df['text2'] = df['text'].apply(easy_translate)
    
    return df



### 메인함수 ###
if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(current_dir, '../data/judgment_chunks.csv')

    translated_df = preprocess_judgments(csv_file)
    translated_df.to_csv(csv_file, index=False)  # 원래 파일에 덮어쓰기

    print("변환 작업이 완료되었습니다.")
    






### Legacy ###
"""### 형태소 분석 ###
from kiwipiepy import Kiwi

def sbg_noun_extractor(text: str) -> list[str]:
    # 먼 문단의 내용도 참고해 품사 태깅
    kiwi = Kiwi(model_type='sbg')
    tokens = kiwi.tokenize(text, normalize_coda=True)

    results = set() # 중복 토큰 제거
    for token, pos, _, _ in tokens:
        if pos.startswith('NN'): # 일반 명사, 고유 명사, 의존 명사만 추출
            results.add(token)

    return results


### 법률용어 DB 접근해서 있는지 확인 ###
import json

with open("data/legal_terminology.json", "r", encoding="utf-8") as db:
    legal_term_DB = json.load(db)

def legal_term_DB_check(term_list: list[str]) -> list[bool]:
    check_list = []
    for term in term_list:
        if term in legal_term_DB:
            check_list.append(True)
        else:
            check_list.append(False)

    return check_list


### 법률용어 질의 ###
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI

# ltq: logical terminology question
ltq_template = ""

ltq_llm = OpenAI(temperature=0.1, model=)
ltq_chain = ltq_template | ltq_llm

def logical_terminology_question(judgment, legal_terminology):
    response = ltq_chain.invoke(judgment, legal_terminology)
    
    ltq_judgment = response.content
    
    return ltq_judgment"""
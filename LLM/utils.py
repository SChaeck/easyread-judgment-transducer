### 환경변수 로드 ###
from dotenv import load_dotenv
import logging
import concurrent.futures
import time
import random

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
et_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "형식 유지 변환기"
        ),
        (   
            "human",
            """### 명령: 형식 유지
            
legal_terminology: 모든 법률용어, 이해하기 어려운 용어와 그것의 국어적 의미
same_form_judgment: 목차를 유지하며 내용을 쉽게 바꾼 판결문. 목차는 유지하지만 초등학생도 이해할 수 있는 단어로 대체하라. '-다'체를 사용한다.
summary: 제시한 판결문의 자세한 내용 요약. '-입니다'체를 사용한다. 사건의 원인을 포함한다.

### 판결문:
{judgment}

### 출력양식:
{{
    "legal_terminology": {{}},
    "same_form_judgment": "",
    "summary": ""
}}"""
        )
    ]
)

et_llm = ChatOpenAI(temperature=0.1, model="gpt-4o-mini")
et_chain = et_prompt | et_llm

def easy_translate(judgment, index, total, max_retries=5):
    retries = 0
    while retries < max_retries:
        try:
            response = et_chain.invoke(judgment)
            et_judgment = response.content
            logger.info(f"변환 완료: {index + 1}/{total}")
            return et_judgment
        except Exception as e:
            retries += 1
            wait_time = 2 ** retries + random.uniform(0, 1)
            logger.error(f"에러 발생: {e} (index: {index + 1}/{total}), 재시도 {retries}/{max_retries}, {wait_time}초 대기")
            time.sleep(wait_time)
    return None

def preprocess_judgments(csv_file):
    df = pd.read_csv(csv_file)
    total = len(df)
    
    def process_judgment(judgment, i, total):
        result = easy_translate(judgment, i, total)
        time.sleep(0.012)  # 요청 간격을 줄여 RPM 5000을 유지합니다.
        return (i, result)

    max_workers = 400  # 스레드 수를 대폭 늘립니다.
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(process_judgment, judgment, i, total): i for i, judgment in enumerate(df['text'])}
        
        for future in concurrent.futures.as_completed(futures):
            index = futures[future]
            try:
                result = future.result()
                if result is not None:
                    df.at[index, 'text2'] = result[1]
            except Exception as e:
                logger.error(f"에러 발생: {e} (index: {index + 1}/{total})")
            
            # 중간 결과 저장
            if index % 10 == 0:
                partial_save_path = os.path.splitext(csv_file)[0] + '_partial.csv'
                df.to_csv(partial_save_path, index=False)
                logger.info(f"중간 결과 저장 완료: {partial_save_path}")

    return df

### 메인함수 ###
if __name__ == "__main__":
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # csv_file = os.path.join(current_dir, '400002-1000004.csv')
    csv_file = "data/400002-1000004.csv"
    
    logger.info("메인 함수 시작")
    translated_df = preprocess_judgments(csv_file)
    translated_df.to_csv(csv_file, index=False)  # 원래 파일에 덮어쓰기
    logger.info("CSV 파일 저장 완료: %s", csv_file)

    print("변환 작업이 완료되었습니다.")

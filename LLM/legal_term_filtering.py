import os
import logging
import time
import random
import pandas as pd
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# 환경변수 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# GPT API 설정
et_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "단어 난이도 평가기"),
        (
            "human",
            """### 명령: 단어 난이도 평가
            
word: {word}
단어의 난이도를 평가하여 초등학생 저학년이 이해할 수 있는 아주 쉬운 단어인지 고등학생 이상이 이해할 수 있는 어려운 단어인지 판단하세요. '아주 쉬움' 또는 '어려움'으로 답하세요.
"""
        )
    ]
)

et_llm = ChatOpenAI(temperature=0.1, model="gpt-4o-mini")
et_chain = et_prompt | et_llm

def evaluate_word_difficulty(word, max_retries=5):
    retries = 0
    while retries < max_retries:
        try:
            response = et_chain.invoke({"word": word})
            difficulty = response.content.strip()
            if difficulty in ["아주 쉬움", "어려움"]:
                return difficulty
        except Exception as e:
            retries += 1
            wait_time = 2 ** retries + random.uniform(0, 1)
            logger.error(f"에러 발생: {e} (단어: {word}), 재시도 {retries}/{max_retries}, {wait_time}초 대기")
            time.sleep(wait_time)
    return None

def process_word(word, definition):
    difficulty = evaluate_word_difficulty(word)
    logger.info(f"단어 평가 완료: {word} -> {difficulty}")
    return word, definition, difficulty

def filter_easy_words(input_file, output_file, del_file):
    df = pd.read_csv(input_file)
    filtered_data = []
    removed_data = []

    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(process_word, row['Key'], row['Value']): row for _, row in df.iterrows()}
        
        for future in as_completed(futures):
            word, definition, difficulty = future.result()
            if difficulty == "어려움":
                filtered_data.append({'Key': word, 'Value': definition})
            else:
                removed_data.append({'Key': word, 'Value': definition})

    # 필터링된 데이터를 CSV로 저장
    pd.DataFrame(filtered_data).to_csv(output_file, index=False, encoding='utf-8')
    
    # 제거된 데이터를 CSV로 저장
    pd.DataFrame(removed_data).to_csv(del_file, index=False, encoding='utf-8')

    logger.info(f"필터링된 데이터가 {output_file}에 저장되었습니다.")
    logger.info(f"제거된 데이터가 {del_file}에 저장되었습니다.")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(current_dir, 'input.csv')
    output_file = os.path.join(current_dir, 'output_filtered.csv')
    del_file = os.path.join(current_dir, 'output_removed.csv')
    
    logger.info("메인 함수 시작")
    filter_easy_words(input_file, output_file, del_file)
    logger.info("필터링 작업이 완료되었습니다.")
    print("필터링 작업이 완료되었습니다.")

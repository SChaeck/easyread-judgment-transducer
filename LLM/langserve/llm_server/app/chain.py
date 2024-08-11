import os
import getpass
import json
import numpy as np
import time

from pinecone import Pinecone
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
from konlpy.tag import Kkma
from konlpy.tag import Komoran

from legal_term_string_search import find_longest_keys_in_string

# API 키 불러오기
load_dotenv()
if not os.getenv("PINECONE_API_KEY"):
    os.environ["PINECONE_API_KEY"] = getpass.getpass("Enter your Pinecone API key: ")

# 법률 용어 DB 불러오기
# JSON 파일을 읽어 딕셔너리로 변환
with open('legal_term_deduplicated_and_filtered.json', 'r') as file:
    legal_term_db = json.load(file)

# 모델 구성
llm = ChatOllama(model="transducer:1.1.DPO", temperature=0.05, top_k=10)

# 벡터 스토어 구성
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
index = pc.Index("legal-term")
embeddings_model = HuggingFaceEmbeddings(model_name="Suchae/bge-m3-Korean-Judgment-Transducer-Verifier-v1.1")
vector_store = PineconeVectorStore(index=index, embedding=embeddings_model, text_key="meaning")

# 리트리버 구성
retriever = vector_store.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 5, "score_threshold": 0.8},
)

# 프롬프트 구성
prompt_template = """다음 법률용어를 참고하여 판결문 내용을 요약하고 쉽게 바꾼 뒤, json 형태로 출력해줘. '-입니다'체를 사용해서 답변해.
<법률용어>
{legal_term}
</법률용어>

<판결문> 
{judgment}
</판결문>

<json>
{{
    "same_form_judgment": "",
    "summary": ""
}}
</json> '-입니다'체를 사용해서 답변해.
"""
rag_prompt = ChatPromptTemplate.from_template(prompt_template)

chain =  rag_prompt | llm | JsonOutputParser()

def legal_term_retrival(judgment):
    term_max_len = 10

    # vector_retrival_legal_term = retriever.invoke(judgment)
    legal_term = {}
    # for term in vector_retrival_legal_term:
    #     legal_term[term.metadata['name']] = term.page_content
        

    if len(legal_term.keys()) < term_max_len:
        k = term_max_len - len(legal_term.keys())
        string_search_legal_term = find_longest_keys_in_string(judgment, k) # list

        for term in string_search_legal_term:
            legal_term[term] = legal_term_db[term]
    
    return legal_term

def judgment_transduce(legal_term, input_prompt):
    
    # 최대 3번까지는 반복해서 질문해줌
    max_retries = 2
    attempts = 0
    success = False
    
    while attempts <= max_retries and not success:
        try:
            answer = chain.invoke({'legal_term': legal_term, 'judgment': input_prompt})
            success = True
        except Exception as e:
            attempts += 1
            if attempts > max_retries:
                # If exceeded max_retries, raise the exception
                raise
            else:
                # Log or print the error message if you want to track it
                print(f"Attempt {attempts} failed with error: {e}. Retrying...")  
    
    return answer

def similarity_measurement(text1, text2):
    embeddings_1 = embeddings_model.embed_query(text1)
    embeddings_2 = embeddings_model.embed_query(text2)
    
    # 넘파이 배열로 변환
    embeddings_1 = np.array(embeddings_1)
    embeddings_2 = np.array(embeddings_2)
    
    similarity = embeddings_1 @ embeddings_2.T
    
    return similarity


# 한국어 형태소 분석기
okt = Okt()

def calculate_fog_and_length(text):
    # 텍스트를 문장 단위로 분리
    sentences = re.split(r'[.!?]', text)

    # 문장당 평균 단어 수 계산 (ASL)
    total_words = 0
    total_sentences = len(sentences)
    for sentence in sentences:
        words = okt.morphs(sentence.strip())
        total_words += len(words)

    ASL = total_words / total_sentences if total_sentences > 0 else 0

    # 복잡한 단어 비율 계산 (3음절 이상의 단어)
    complex_words = 0
    for word in okt.morphs(text):
        if len(word) >= 3:
            complex_words += 1

    percentage_of_complex_words = (complex_words / total_words) * 100 if total_words > 0 else 0

    # FOG 계산
    FOG = (ASL + percentage_of_complex_words) * 0.4

    # LENGTH 계산
    Word_num = total_words
    LENGTH = math.log(Word_num) if Word_num > 0 else 0

    return ASL, percentage_of_complex_words, FOG, LENGTH


# 쉬운 변환 검증
kkma = Kkma()
komoran = Komoran()
def syntactic_complexity_korean(text):
    sentences = kkma.sentences(text)  # 텍스트를 문장으로 분리합니다.
    num_sentences = len(sentences)
    
    num_clauses = 0
    for sentence in sentences:
        morphemes = komoran.pos(sentence)  # 문장을 형태소 분석합니다.
        num_clauses += sum(1 for word, tag in morphemes if tag in ['VV', 'VA'])  # 동사나 형용사를 종속 절로 간주합니다.
    
    return num_clauses / num_sentences if num_sentences > 0 else 0

def evaluate_ease(original_text, simplified_text):
    original_syntactic_complexity = syntactic_complexity_korean(original_text)
    simplified_syntactic_complexity = syntactic_complexity_korean(simplified_text)

    return original_syntactic_complexity/simplified_syntactic_complexity

def chain_retriever(input_prompt):
    start_time = time.time()  # 전체 소요 시간 측정을 위한 시작 시간 기록
    
    # 법률 용어 불러오기
    step_start = time.time()  # 해당 단계 시작 시간
    legal_term = legal_term_retrival(input_prompt)  # dict
    step_end = time.time()  # 해당 단계 종료 시간
    print(f"법률 용어 불러오기 소요 시간: {step_end - step_start:.4f}초")
    
    # LLM 답변 생성
    step_start = time.time()
    answer = judgment_transduce(legal_term, input_prompt)
    step_end = time.time()
    print(f"LLM 답변 생성 소요 시간: {step_end - step_start:.4f}초")
    
    if 'same_form_judgement' in answer.keys():
        answer['same_form_judgment'] = answer.pop('same_form_judgement')
    
    # 기존 판결문과 답변의 유사도 측정
    step_start = time.time()
    similarity = similarity_measurement(input_prompt, answer['same_form_judgment'])
    step_end = time.time()
    print(f"유사도 측정 소요 시간: {step_end - step_start:.4f}초")
    
    # 기존 판결문에 비해 얼마나 쉽게 바뀌었는지 측정
    step_start = time.time()
    ease_improvement = evaluate_ease(input_prompt, answer['same_form_judgment'])
    step_end = time.time()
    print(f"쉽게 바뀌었는지 측정 소요 시간: {step_end - step_start:.4f}초")
    
    total_time = time.time() - start_time  # 전체 소요 시간 계산
    print(f"전체 소요 시간: {total_time:.4f}초")
    
    return legal_term, answer, similarity, ease_improvement

if __name__ == "__main__":
    print(chain_retriever("뿐만 아니라,제4차 신용장통일규칙 제16조 혹은 제5차 신용장통일규칙 제14조에서, '신용장 개설은행이 제시된 서류의 불일치를 이유로 서류의 수리를 거절하고자 하는 경우에 지체 없이 제시인에게 그 불일치 사항을 통지하고 서류를 반송하는 등의 조치를 취하지 아니하면 개설은행은 그 서류가 신용장의 조건과 일치하지 않는다는 주장을 할 수 있는 권리를 상실한다'고 규정한 취지는, 신용장 제시 서류에 불일치가 있다 하여도 개설은행이 제시인에게 이를 통지하는 등의 조치를 취하지 아니하면 개설은행은 그 불일치를 주장하지 못하고 원래의 신용장 조건에 따른 대금지급의무를 부담한다는 것에 불과하지, 그 불일치 사항의 통지가 없다고 하여 신용장 수익자나 그 이후의 신용장 매입은행으로 하여금 종전에 없었던 새로운 권리를 취득하게 하는 것은 아니므로, 이 사건 백투백신용장 매입은행인 원고로서는 여전히 그 신용장 개설시에 약정된 바와 같은 이 사건 특수조건 조항이 성취되는 것을 조건으로 하여 이 사건 신용장 대금을 청구할 수 있을 뿐, 위 제4차 신용장통일규칙 제16조 혹은 제5차 신용장통일규칙 제14조의 규정을 들어 원고에게 위 특수조건 조항의 적용을 받지 않는 무조건적인 완전한 신용장 대금지급청구권이 발생하는 것은 아니라고 할 것이다."))
    
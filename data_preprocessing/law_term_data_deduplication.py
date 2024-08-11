from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
from tqdm import tqdm

# 1. JSON 파일에서 key 값을 읽어와 리스트에 저장
print("Loading data from JSON file...")
with open('llm_server/app/legal_term_filtered.json', 'r', encoding='utf-8') as f:
    data_dict = json.load(f)
print("Data loaded successfully.")


# key 값만 리스트로 추출
data = list(data_dict.keys())
print(f"Number of entries loaded: {len(data)}")


# 1. TF-IDF 벡터화
print("Starting TF-IDF vectorization...")
vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 3))
tfidf_matrix = vectorizer.fit_transform(data)
print("TF-IDF vectorization completed.")


# 2. 코사인 유사도 계산
print("Calculating cosine similarity...")
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
print("Cosine similarity calculation completed.")

# 3. 중복 제거 로직
def deduplicate(data, cosine_sim, threshold=0.8):
    to_remove = set()
    for idx in tqdm(range(len(data)), desc="Deduplicating", unit="pair"):
        if idx in to_remove:
            continue
        similar_indices = np.where(cosine_sim[idx] > threshold)[0]
        for sim_idx in similar_indices:
            if sim_idx != idx:
                to_remove.add(sim_idx)
    deduplicated_data = [data[i] for i in range(len(data)) if i not in to_remove]
    return deduplicated_data

# 4. 중복 제거된 최종 데이터 리스트
print("Starting deduplication process...")
deduplicated_data = deduplicate(data, cosine_sim, threshold=0.8)
print("Deduplication process completed.")

# 결과 출력
print(f"중복 제거 전 데이터 개수: {len(data)}")
print(f"중복 제거 후 데이터 개수: {len(deduplicated_data)}")

# 6. 결과를 새로운 JSON 파일로 저장 (필요한 경우)
with open('deduplicated_data.json', 'w', encoding='utf-8') as f:
    json.dump({key: data_dict[key] for key in deduplicated_data}, f, ensure_ascii=False, indent=4)
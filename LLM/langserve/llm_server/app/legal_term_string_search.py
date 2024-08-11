import json
import random
from tqdm import tqdm

json_file = 'legal_term_deduplicated_and_filtered.json'  # Replace with your JSON file path

def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1

    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text, pattern):
    lps = compute_lps(pattern)
    i = j = 0
    results = []

    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == len(pattern):
            results.append(i - j)
            j = lps[j - 1]
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return results

def find_longest_keys_in_string(string, k):
    global json_file
    # Load JSON data
    with open(json_file, 'r') as file:
        data = json.load(file)

    # Extract all keys from the JSON data
    keys = []
    
    def extract_keys(d):
        if isinstance(d, dict):
            for key, value in d.items():
                keys.append(key)
                extract_keys(value)
        elif isinstance(d, list):
            for item in d:
                extract_keys(item)
    
    extract_keys(data)

    # Convert keys to list and sort for consistent order

    # Sample 1/4 of the keys randomly
    sample_size = max(1, len(keys) // 4)  # Ensure at least one key is sampled
    sampled_keys = random.sample(keys, sample_size)

    # sampled_keys = keys

    sampled_keys = sorted(sampled_keys, key=len, reverse=True)


    # Find longest unique keys that are present in the string
    found_keys = []
    for key in sampled_keys:
        if kmp_search(string, key):
            if not any(key in existing_key for existing_key in found_keys):
                found_keys.append(key)

    return found_keys[:k]

if __name__ == "__main__":
    # Example usage
    string = '(2)「의료급여법」 제7조제2항, 동법 시행규칙 제6조의 규정에 의하면, 의료급여의 적용기준 및 방법은 「국민건강보험 요양급여의 기준에 관한 규칙」 제5조제2항 및 별표 1의 규정에 의하도록 되어 있고, 별표 1의 제1호가목, 다목 및 제4호에 의하면, 요양급여는 가입자 등의 연령ㆍ성별ㆍ직업 및 심신상태 등의 특성을 고려하여 진료의 필요가 있다고 인정되는 경우에 정확한 진단을 토대로 하여 환자의 건강증진을 위하여 의학적으로 인정되는 범위 안에서 최적의 방법으로 실시하여야 하고, 경제적으로 비용효과적인 방법으로 행하여야 하며, 치료재료는 「약사법」 기타 다른 관계법령에 의하여 허가ㆍ신고 또는 인정된 사항(효능ㆍ효과 및 사용방법)의 범위 안에서 환자의 증상에 따라 의학적 판단에 따라 필요ㆍ적절하게 사용하도록 하고 있고, 「의료급여법 시행규칙」 제21조제5항 및 「요양급여비용 심사ㆍ지급업무 처리 기준」(보건복지부고시 제2003-25호) 제4조제1항의 규정에 의하면, 심사평가원은 요양급여비용의 심사청구를 받은 때에는 그 심사청구 내역이 보건복지부장관이 정한 요양급여비용의 산정지침 및 기타 심사평가원의 원장이 ○○위원회의 심의를 거쳐 정한 요양급여비용의 심사기준 등에 적합한 지를 심사하여야 한다고 되어 있다.'  # Replace with your target string

    found_keys = find_longest_keys_in_string(string, 10)
    print("found in the string:", found_keys)

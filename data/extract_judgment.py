import os
import json
import csv
from tqdm import tqdm

empty = 0

def extract_text_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        판시사항 = data.get("판시사항", "")
        판결요지 = data.get("판결요지", "")
        판례내용 = data.get("판례내용", "")
        재결요지 = data.get("재결요지", "")
        주문 = data.get("주문", "")
        청구취지 = data.get("청구취지", "")
        이유 = data.get("이유", "")
        
        combined_text = ""
        if 판시사항:
            combined_text += 판시사항
        if 판결요지:
            combined_text += 판결요지
        if 판례내용:
            combined_text += 판례내용
        if 재결요지:
            combined_text += 재결요지
        if 주문:
            combined_text += 주문
        if 청구취지:
            combined_text += 청구취지
        if 이유:
            combined_text += 이유
            
        if combined_text == "":
            empty += 1
            
        return combined_text

def process_json_files_in_folder(folder_path, output_csv_path):
    total_length = 0
    file_count = 0
    with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['instruction', 'text', 'text2'])  # CSV 헤더 작성

        for root, dirs, files in tqdm(os.walk(folder_path)):
            for file in files:
                try:
                    if file.endswith('.json'):
                        json_file_path = os.path.join(root, file)
                        combined_text = extract_text_from_json(json_file_path)
                        
                        if combined_text != "":                        
                            csv_writer.writerow(['_', combined_text, '_'])
                            total_length += len(combined_text)
                            file_count += 1
                except:
                    print('file name:', dirs, file)
    
    if file_count > 0:
        average_length = total_length / file_count
    else:
        average_length = 0
    print(f'Average length of combined_text: {average_length}')

# 실행 예시
folder_path = '115.법률-규정 텍스트 분석 데이터_고도화_상황에 따른 판례 데이터'  # JSON 파일이 있는 폴더 경로로 변경하세요
output_csv_path = 'raw_data/judgment.csv'  # 출력 CSV 파일 경로
process_json_files_in_folder(folder_path, output_csv_path)
print(empty)
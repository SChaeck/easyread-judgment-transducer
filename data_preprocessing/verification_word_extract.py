import csv
import json
import re

# 입력 CSV 파일 경로와 출력 JSONL 파일 경로 설정
input_csv_file = 'vector_db/data/processing_judgment.csv'
output_csv_file = 'vector_db/legal_term.csv'

# CSV 파일 열기
with open(input_csv_file, mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    # 컬럼명 변경
    csv_reader.fieldnames = ['instruction', 'input', 'output']
    
    next(csv_reader)
    
    # CSV 파일의 각 줄을 처리
    total_error = 0
    filtered_rows = []
    for i, row in enumerate(csv_reader):
        try:
            # 여기서 원하는 처리를 수행합니다.
            matches = re.findall(r'\{(?:[^{}]|\{[^{}]*\})*\}', row['output'])
            
            output_dict = json.loads(matches[0])
            
            for key, value in output_dict['legal_terminology'].items():
                filtered_row = [key, value]
                filtered_rows.append(filtered_row)
            
        except Exception as e:
            # print("error:", e)
            # print("line:", i)
            total_error += 1

print('total_error:', total_error)

# 새로운 CSV 파일로 저장
with open(output_csv_file, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.writer(outfile)
    # 헤더 작성
    writer.writerow(['name', 'meaning'])
    # 데이터 작성
    writer.writerows(filtered_rows)
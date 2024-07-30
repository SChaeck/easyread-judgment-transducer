import csv
import json
import re

# 입력 CSV 파일 경로와 출력 JSONL 파일 경로 설정
input_csv_file = 'vector_db/processing_judgment.csv'
output_jsonl_file = 'vector_db/processing_judgment.jsonl'

prompt = """A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions.
Human: 다음 법률용어를 참고하여 판결문 내용을 요약하고 쉽게 바꾼 뒤, json 형태로 출력해줘.
<법률용어>
{legal_terminology}
</법률용어>
<판결문>
{judgment}
</판결문>
Assistant: {{
    "same_form_judgment": {same_form},
    "summary": {summary}
}}"""

# CSV 파일 열기
with open(input_csv_file, mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    
    # 컬럼명 변경
    csv_reader.fieldnames = ['instruction', 'input', 'output']
    
    next(csv_reader)
        
    # JSONL 파일 열기
    with open(output_jsonl_file, mode='w', encoding='utf-8') as jsonl_file:
        # CSV 파일의 각 줄을 처리
        total_error = 0
        for i, row in enumerate(csv_reader):
            try:
                # 여기서 원하는 처리를 수행합니다.
                matches = re.findall(r'\{(?:[^{}]|\{[^{}]*\})*\}', row['output'])
                
                output_dict = json.loads(matches[0])
                
                row['instruction'] = prompt
                
                row['text'] = prompt.format(
                    legal_terminology=output_dict['legal_terminology'], 
                    judgment=row['input'], 
                    same_form=output_dict['same_form_judgment'], 
                    summary=output_dict['summary']
                    )
                
                text_only = {'text': row['text']}
                
                # JSONL 형식으로 저장
                jsonl_file.write(json.dumps(text_only, ensure_ascii=False) + '\n')
            except Exception as e:
                # print("error:", e)
                # print("line:", i)
                total_error += 1

print('total_error:', total_error)
print(f'{input_csv_file} 파일이 {output_jsonl_file} 파일로 변환되었습니다.')

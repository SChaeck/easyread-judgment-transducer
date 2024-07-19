import csv
from utils import easy_translate







if __name__ == "__main__":
    
    # 기존 판결문 데이터를 저장하는 리스트
    judgments = []
    with open('data/raw_data/judgment.csv', 'r', encoding='utf-8') as f:
        csv_judgment = csv.reader(f)
        for row in csv_judgment:
            judgments.append(row)
            
    print(judgments)
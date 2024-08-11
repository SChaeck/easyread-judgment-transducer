from huggingface_hub import HfApi, Repository
from transformers import AutoTokenizer, AutoModelForCausalLM
import os

token = "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"

# 허깅페이스 API 토큰 설정
repo_id = "Suchae/EEVE-Korean-Judgment-Transducer-10.8B-v1.1-DPO"  # 모델을 업로드할 리포지토리 이름

# 로컬 모델 경로
model_dir = "EEVE-Korean-Judgment-Transducer-10.8B-v1.1-DPO"  # 모델이 저장된 로컬 경로로 대체

# 모델과 토크나이저 로드
model = AutoModelForCausalLM.from_pretrained(model_dir)
tokenizer = AutoTokenizer.from_pretrained(model_dir)

# 허깅페이스 API와의 연결 설정
api = HfApi(token=token)

# 리포지토리 생성 (이미 존재하는 경우에는 무시됨)
# api.create_repo(repo_id, private=False)  # `private=True`로 설정하면 비공개로 업로드

# 모델과 토크나이저 저장
model.save_pretrained(model_dir)
tokenizer.save_pretrained(model_dir)

# 리포지토리에 업로드
repo = Repository(local_dir=model_dir, clone_from=repo_id, use_auth_token=token)
repo.push_to_hub(commit_message="Initial commit")

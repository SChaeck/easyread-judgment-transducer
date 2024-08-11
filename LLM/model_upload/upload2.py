from huggingface_hub import Repository

# 허깅페이스 API 토큰
api_token = "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"  # 본인의 허깅페이스 API 토큰으로 대체

# 새로운 디렉토리와 리포지토리 이름 설정
new_model_dir = "/home/ragllama/decs_jupyter_lab/korean-finetuning/Suchae/langserve/new_model_dir"
repo_id = "Suchae/EEVE-Korean-Judgment-Transducer-10.8B-v1.1-DPO"  # 모델을 업로드할 허깅페이스 리포지토리 이름

# 리포지토리 클론
repo = Repository(local_dir=new_model_dir, clone_from=repo_id, use_auth_token=api_token)

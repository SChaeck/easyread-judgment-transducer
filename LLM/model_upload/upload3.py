import shutil
import os

# 기존 모델 디렉토리와 새로운 디렉토리 경로 설정
old_model_dir = "/home/ragllama/decs_jupyter_lab/korean-finetuning/Suchae/langserve/.huggingface/EEVE-Korean-Judgment-Transducer-10.8B-v1.1-DPO"
new_model_dir = "/home/ragllama/decs_jupyter_lab/korean-finetuning/Suchae/langserve/new_model_dir"

# 모델 파일 이동
if os.path.exists(old_model_dir) and os.path.exists(new_model_dir):
    for item in os.listdir(old_model_dir):
        s = os.path.join(old_model_dir, item)
        d = os.path.join(new_model_dir, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, False, True)
        else:
            shutil.copy2(s, d)
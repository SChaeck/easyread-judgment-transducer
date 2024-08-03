import os
import sys
from FlagEmbedding.baai_general_embedding.finetune.run import main as finetune_main

# 현재 스크립트 파일의 디렉토리를 기준으로 상대 경로를 설정합니다.
current_dir = os.path.dirname(os.path.abspath(__file__))
train_data_path = os.path.join(current_dir, "bgem3_data.jsonl")
output_dir = os.path.join(current_dir, "saved_model")

if __name__ == "__main__":
    sys.argv = [
        "run.py",
        "--output_dir", output_dir,
        "--model_name_or_path", "BAAI/bge-large-zh-v1.5",
        "--train_data", train_data_path,
        "--learning_rate", "1e-5",
        "--num_train_epochs", "5",
        "--per_device_train_batch_size", "1",
        "--dataloader_drop_last", "True",
        "--normlized", "True",
        "--temperature", "0.02",
        "--query_max_len", "64",
        "--passage_max_len", "256",
        "--train_group_size", "2",
        "--negatives_cross_device", "True",
        "--logging_steps", "10",
        "--save_steps", "1000",
        "--query_instruction_for_retrieval", ""
    ]

    finetune_main()

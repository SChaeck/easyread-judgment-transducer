from unsloth import FastLanguageModel
from transformers import BitsAndBytesConfig
import torch

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name = "./EEVE-Korean-Judgment-Transducer-10.8B-v1.1-DPO", # Choose ANY! eg teknium/OpenHermes-2.5-Mistral-7B
    max_seq_length = 8192,
    load_in_4bit = False,
    low_cpu_mem_usage=True
)

model.push_to_hub_gguf("Suchae/EEVE-Korean-Judgment-Transducer-10.8B-v1.1-DPO-GGUF", tokenizer, quantization_method = "f16")
model.push_to_hub_gguf("Suchae/EEVE-Korean-Judgment-Transducer-10.8B-v1.1-DPO-GGUF", tokenizer, quantization_method = "q8_0")
model.push_to_hub_gguf("Suchae/EEVE-Korean-Judgment-Transducer-10.8B-v1.1-DPO-GGUF", tokenizer, quantization_method = "q4_k_m")
from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Define the prompt template and create chains
prompt_template = "{prompt}"
prompt = ChatPromptTemplate.from_template(prompt_template)

# Create multiple chains
llm_chains = [
    (prompt | ChatOllama(model="transducer:1.1.f16", temperature=0.15) | StrOutputParser()),
    (prompt | ChatOllama(model="transducer:1.1", temperature=0.15) | StrOutputParser()),
    (prompt | ChatOllama(model="transducer", temperature=0.15) | StrOutputParser()),
    (prompt | ChatOllama(model="EEVE-Korean-10.8B:latest", temperature=0.15) | StrOutputParser()),
    (prompt | ChatOllama(model="transducer:1.1.f16.4", temperature=0.15) | StrOutputParser()),
    (prompt | ChatOllama(model="transducer:1.1.f16.5", temperature=0.15) | StrOutputParser()),
    (prompt | ChatOllama(model="transducer:1.1.f16.6", temperature=0.15) | StrOutputParser()),
]

import json
import concurrent.futures
from tqdm import tqdm

def process_line(line, chain, output_file):
    try:
        data = json.loads(line)
        if 'question' in data:
            prompt = data['question']
            # Use the chain to generate a response
            response = chain.invoke(prompt)
            data['response_k'] = response
        
        # Write the processed result to the output file
        with open(output_file, 'a', encoding='utf-8') as outfile:
            json.dump(data, outfile, ensure_ascii=False)
            outfile.write('\n')
        
        return True
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return False
    except Exception as e:
        print(f"Error occurred: {e}")
        return False


def process_jsonl(input_file, output_file):
    # Create or truncate the output file
    # with open(output_file, 'w', encoding='utf-8') as outfile:
    #     pass

    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()
    lines = lines[11270:]

    total_lines = len(lines)

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        # Submit tasks to the executor
        futures = []
        for i, line in enumerate(lines):
            chain = llm_chains[i % len(llm_chains)]
            futures.append(executor.submit(process_line, line, chain, output_file))

        # Monitor progress
        for future in tqdm(concurrent.futures.as_completed(futures), total=total_lines, desc='Processing'):
            future.result()  # Optionally handle results or errors here


input_file = 'judgment_transducer_DPO_dataset_2.jsonl'
output_file = 'judgment_transducer_DPO_dataset_3.jsonl'
num_workers = len(llm_chains)  # 사용할 스레드 수

process_jsonl(input_file, output_file)

from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# LangChain이 지원하는 다른 채팅 모델을 사용합니다. 여기서는 Ollama를 사용합니다.
llm = ChatOllama(model="EEVE-Korean-10.8B:latest", temperature=0.15)

prompt_template = """A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions.
Human: 다음 판결문을 쉽게 바꿔줘. 먼저 법률 용어의 의미를 설명한 뒤, 일반인이 이해할 수 있는 판결문을 제공하고, 초등학생도 이해할 수 있는 쉬운 판결문을 제공해줘.
{judgment}
Assistant: """

# 프롬프트 설정
prompt = ChatPromptTemplate.from_template(prompt_template)

# LangChain 표현식 언어 체인 구문을 사용합니다.
chain = prompt | llm | StrOutputParser()


from langchain_community.llms.fake import FakeListLLM
from langchain.prompts import PromptTemplate

responses = [
    "您好",
    "我能做什么"
]

fake_list_llm = FakeListLLM(responses=responses)

prompt = PromptTemplate.from_template("你好")

output = fake_list_llm.invoke(prompt.format())
print(output)

output = fake_list_llm.invoke(prompt.format())
print(output)

output = fake_list_llm.invoke(prompt.format())
print(output)
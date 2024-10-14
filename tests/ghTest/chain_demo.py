from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_community.llms.tongyi import Tongyi
from langchain.chains import LLMChain

# pip install langchain==0.0.354 langchain_experimental==0.0.47 langchain-community==0.0.8 langsmith==0.0.77 langchain-core==0.1.6

model = Tongyi(model_name='qwen-max', model_kwarg={'temperature': 0.01})

# 定义期望的数据结构。
class Joke(BaseModel):
    content: str = Field(description="笑话的内容")
    reason: str = Field(description="为什么好笑")

# 设置解析器并将指令注入到提示模板中。
parser = PydanticOutputParser(pydantic_object=Joke)
print(parser.get_format_instructions())
prompt = PromptTemplate(
    template="参考下面的格式回答用户的疑问\n{format_instructions}\n{query}",
    input_variables=["query"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)

# chain = LLMChain(prompt=prompt, llm=model, output_parser=parser)
chain = prompt | model | parser
res = chain.invoke({
    "query": "讲一个笑话"
})
print(res)
# print(res['text'])

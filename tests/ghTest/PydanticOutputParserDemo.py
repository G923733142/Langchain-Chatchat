from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_community.llms.tongyi import Tongyi


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
print(prompt.format(query="给我讲个笑话。"))

output = model.invoke(prompt.format(query="给我讲个笑话。"))
print(output)

joke = parser.parse(output)
print(joke)

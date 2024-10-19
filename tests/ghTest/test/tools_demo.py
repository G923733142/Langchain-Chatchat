import asyncio
import os

from dotenv import load_dotenv
from langchain import hub
from langchain.agents import load_tools, initialize_agent, AgentType, create_react_agent, AgentExecutor, \
    create_structured_chat_agent
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from langchain.tools.render import render_text_description
from langchain_community.llms.tongyi import Tongyi
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv('D:/PycharmProjects/Langchain-Chatchat/.env')  # 指定加载 env 文件
key = os.getenv('DASHSCOPE_API_KEY')  # 获得指定环境变量
DASHSCOPE_API_KEY = os.environ["DASHSCOPE_API_KEY"]  # 获得指定环境变量
model = Tongyi(temperature=1)
"""这种定义方式，只能接受一个参数，且不能封装成类，要不然会报少参数"""
class SearchInput(BaseModel):
    query: str = Field(description="search query")


@tool("search-tool", args_schema=SearchInput, return_direct=True)
def search(query: str) -> str:
    """Look up things online."""
    print("我是一个搜索的工具,我被调用了")
    return "我是一个搜索的工具"

# print(search.name)
# print(search.description)
# print(search.args)
# print(search.return_direct)


"""这种定义方式，可以接受多个参数"""
class CalculatorInput(BaseModel):
    s: str = Field(description="输入字符串")


def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


calculator = StructuredTool.from_function(
    func=multiply,  # 工具具体逻辑
    name="Calculator",  # 工具名
    description="multiply numbers",  # 工具信息
    args_schema=CalculatorInput,  # 工具接受参数信息
    return_direct=True,  # 直接作为工具的输出返回给调用者
    handle_tool_error=True,  # 报错了继续执行，不会吧那些报错行抛出，也可以自定义函数处理，handle_tool_error=函数名
)

# print(calculator)


class SortList(BaseModel):
    num: str = Field(description="待排序列表")


def dort_fun(num):
    """Multiply two numbers."""
    return sorted(eval(num))


sorter = StructuredTool.from_function(
    func=dort_fun,  # 工具具体逻辑
    name="sort_num",  # 工具名
    description="排序列表中的数字",  # 工具信息
    args_schema=SortList,  # 工具接受参数信息
    return_direct=True,  # 直接作为工具的输出返回给调用者
    handle_tool_error=True,  # 报错了继续执行，不会吧那些报错行抛出，也可以自定义函数处理，handle_tool_error=函数名
)

# print(sorter)

from langchain_core.tools import tool


@tool
def multiply(first: int, second: int) -> int:
    """实现两个整数的乘法运算。"""
    return first * second

# 定义一个加法工具
@tool
def add(first: int, second: int) -> int:
  """实现两个整数的加法运算。"""
  return first + second

# 定义一个指数运算工具
@tool
def exponentiate(base: int, exponent: int) -> int:
  """实现指数运算。"""
  return base**exponent

tools = [multiply, add, exponentiate]
# result = multiply.invoke({"first": 4, "second": 5})
# print(result)  # 输出结果：20

def tool_chain(input):
  # 将工具名称映射到工具函数
  tool_map = {tool.name: tool for tool in tools}
  # 根据输入名称选择工具
  choose_tool = tool_map[input["name"]]
  arguments = input["arguments"]
  for key, value in arguments.items():
    # 如果值是字典，递归调用tool_chain
    if isinstance(value, dict):
      arguments[key] = tool_chain(value)
  # 使用参数调用选定的工具
  return choose_tool.invoke(arguments)

rendered_tools = render_text_description([multiply])
system_prompt = f"""你是一个可以访问以下工具集的助手。以下是每个工具的名称和描述：
    {rendered_tools}
    根据用户输入，返回要使用的工具的名称和输入。将你的响应以包含 'name' 和 'arguments' 键的 JSON 格式返回。
"""


prompt = ChatPromptTemplate.from_messages(
    [("system", system_prompt), ("user", "{input}")]
)

chain = prompt | model | JsonOutputParser() | tool_chain
result = chain.invoke({"input": "计算 13 乘以 4 的结果的平方"})
print(result)
"""
zero-shot-react-description
此代理使用ReAct框架，仅基于工具的描述来确定要使用的工具。
可以提供任意数量的工具。
此代理需要为每个工具提供描述
工具只能接受一个参数，不支持多个参数
"""

tools = load_tools(["llm-math"], llm=model)
tools = [search , sorter] + tools
agent = initialize_agent(tools, model, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
# outputstr = agent.run("计算 2 ** 3 + 4，`[10,4,7]`排一下序，并且")
# print(outputstr)


async def run():
    response = await agent.arun(input="算 2 ** 3 + 4，`[10,4,7]`排一下序，")
    print(response)


# if __name__ == '__main__':
    # asyncio.run(run())




class CalculatorInput(BaseModel):
    s: str = Field(description="输入字符串")


def length_cal(s: str) -> int:
    """Multiply two numbers."""
    return len(s)


calculator = StructuredTool.from_function(
    func=length_cal,  # 工具具体逻辑
    name="Calculator",  # 工具名
    description="计算字符长度",  # 工具信息
    args_schema=CalculatorInput,  # 工具接受参数信息
    return_direct=True,  # 直接作为工具的输出返回给调用者
    handle_tool_error=True,  # 报错了继续执行，不会吧那些报错行抛出，也可以自定义函数处理，handle_tool_error=函数名
)


class SearchInput(BaseModel):
    query: str = Field(description="should be a search query")


@tool("search-tool", args_schema=SearchInput, return_direct=True)
def search(query: str) -> str:
    """Look up things online."""
    return "你好啊"

# 这里第二个问题，会丢失
tools = [search, calculator]
prompt = hub.pull("hwchase17/react")
# ReAct agent
agent = create_react_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
# outputstr = agent_executor.invoke({"input": "langchian是什么东西？`阿萨德防守打法`有多少个字符？"})
# print(outputstr)

from langchain_experimental.plan_and_execute import PlanAndExecute, load_agent_executor, load_chat_planner

planner = load_chat_planner(model)
executor = load_agent_executor(model, tools, verbose=True)
# 初始化Plan-and-Execute Agent
agent = PlanAndExecute(planner=planner, executor=executor, verbose=True)
# 运行Agent解决问题 , 这里可以调用多个自定义工具
# outputstr = agent.run("`阿萨德防守打法`有多少个字符？langchian是什么东西？前面的问题都使用中文回答，并汇总一起给我答案")
# print(outputstr)


class CalculatorInput(BaseModel):
    a: str = Field(description="第一个字符串")
    b: str = Field(description="第二个字符串")


def multiply(a: str, b: str) -> int:
    """Multiply two numbers."""
    return len(a) * len(b)


calculator = StructuredTool.from_function(
    func=multiply,  # 工具具体逻辑
    name="Calculator",  # 工具名
    description="计算字符长度的乘积",  # 工具信息
    args_schema=CalculatorInput,  # 工具接受参数信息
    return_direct=True,  # 直接作为工具的输出返回给调用者
    handle_tool_error=True,  # 报错了继续执行，不会吧那些报错行抛出，也可以自定义函数处理，handle_tool_error=函数名
)


class SearchInput(BaseModel):
    query: str = Field(description="should be a search query")


@tool("search-tool", args_schema=SearchInput, return_direct=True)
def search(query: str) -> str:
    """Look up things online."""
    return "你好啊2"


tools = [search, calculator]
prompt = hub.pull("hwchase17/structured-chat-agent")
agent = create_structured_chat_agent(model, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
)
# outputstr = agent_executor.invoke({"input": "`asd`的字符串长度乘以`as`的字符串长度是多少？langchiani是什么？"})
# print(outputstr)

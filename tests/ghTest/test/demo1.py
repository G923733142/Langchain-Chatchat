import os

from dotenv import load_dotenv
from langchain_community.chat_models import ChatTongyi
from langchain_community.llms.tongyi import Tongyi
from langchain_core.messages import SystemMessage
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate

load_dotenv('D:/PycharmProjects/Langchain-Chatchat/.env')  # 指定加载 env 文件
key = os.getenv('DASHSCOPE_API_KEY')  # 获得指定环境变量
DASHSCOPE_API_KEY = os.environ["DASHSCOPE_API_KEY"]  # 获得指定环境变量


model = Tongyi(model_name="qwen-max", model_kwargs={"temperature": 0.01}, streaming=True)
chat_model = ChatTongyi(model_name="qwen-max")

# outputstr = model.predict("你好，欢迎")
#
# print(outputstr)

chat_template3 = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=("你是一个助手")
        ),
        HumanMessagePromptTemplate.from_template("{text}"),
    ]
)
chain = chat_template3 | chat_model

outputstr = chain.invoke({"text": "你好，欢迎tt"}  )

print(outputstr)
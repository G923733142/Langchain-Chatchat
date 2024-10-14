from langchain.chains import APIChain
from langchain_community.llms.tongyi import Tongyi
from langchain_core.prompts import PromptTemplate
from langchain_experimental.llm_bash.base import LLMBashChain

model = Tongyi(model_name='qwen-max', model_kwarg={'temperature': 0.01})
# model_2 = Tongyi(model_name='llama2-13b-chat-v2', model_kwarg={'temperature': 0.01})
# model_3 = GhG4f()



HTTPBIN_DOCS = """
# API 使用文档

## 概述
此API用于向指定的URL发送告警信息。当系统检测到特定的告警条件时，可以调用此API以通知管理员或记录系统的状态。

## API 信息
- **URL**: http://httpbin.org/get
- **业务说明**: 发送告警信息至服务器，用于系统告警通知或日志记录。
- **请求方式**: `GET`

## 请求参数

| 参数名 | 类型 | 描述     | 是否必须 | 示例值 |
|-------|------|----------|---------|--------|
| alarm | string | 具体的告警信息描述 | 是      | "alarm information" |

"""

# 这个要使用linux 系统，才能使用bash命令
query = "我的是window10系统，可以使用 Get-PSDrive D 来查看D 盘的使用情况。帮我查询我的D盘磁盘使用情况。"
base_chain = LLMBashChain.from_llm(model, verbose=True)
# outputStr = base_chain.invoke(query)
# print(outputStr)

prompt = PromptTemplate.from_template(
    """
        {context} \n 根据该内容，判断是否需要磁盘告警。
    """
)

alarm_chain = {
    "context": lambda x: "磁盘c, 一共120G，已使用108G"
} | prompt | model

outputStr = alarm_chain.invoke({})
print(outputStr)

api_charn = APIChain.from_llm_and_api_docs(
    llm=model,
    api_docs=HTTPBIN_DOCS,
    limit_to_domains=["http://httpbin.org"],
    verbose=True
)

alarm_chain2 = alarm_chain | api_charn

outputStr = alarm_chain2.invoke({})
print(outputStr)


import serpapi
from dataclasses import dataclass, field
from typing import List, Optional
import os

from langchain_community.llms.tongyi import Tongyi
from langchain_core.runnables import RunnableLambda
from pydantic import BaseModel, Field
from langchain.prompts import PromptTemplate
from g4f.client import Client
from sympy.polys.polyconfig import query

client = Client()

class SearchResultItem(BaseModel):
    title: str
    link: str
    snippet: str

class SearchResults(BaseModel):
    results: List[SearchResultItem]



def searchResult(query: str):
    params = {
        "q": query,
        "engine": "bing"
    }
    client = serpapi.Client(api_key="06377ea74f55a18db69f0cefdbf5711b98e5f7dcfd3274fcc8a367ccfee3573c")
    result = client.search(params)
    print("搜索结果:", result)
    organic_results = result["organic_results"][:1] # 过长了，截取第一个就行
    organic_results
    search_result = SearchResults(
        results=[
            SearchResultItem(
                title=organic_result["title"],
                link=organic_result["link"],
                snippet=organic_result["snippet"]
            )
            for organic_result in organic_results
        ]
    )
    return search_result

def streamChat(prompt):
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        stream=True,
        messages=[
            {
                "role": "user",
                "content": prompt

            }
        ]
    )
    print("完整回应：", stream)

    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")


prompt = PromptTemplate.from_template(
        """根据搜索引擎的结果，回答用户问题。
        searchResult: {search_result}
        query: {query}
        """)
model = Tongyi(model_name='qwen-max', model_kwarg={'temperature': 0.01})
chain = {
    "search_result": lambda x: searchResult(x["query"]),
    "query": RunnableLambda(lambda x: x["query"]),
} | prompt | model
query = "上春山是什么意思"
outputStr = chain.invoke({
    "query": query
})
print(outputStr)



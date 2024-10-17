from typing import List

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.llms.tongyi import Tongyi
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

model = Tongyi(model_name='qwen-max', model_kwarg={'temperature': 0.01})

def get_docs(role: str="student") -> List[Document]:
    docs = []
    if role == "student":
        docs = [
            Document(page_content="李明喜欢红色但不喜欢黄色"),
            Document(page_content="李华喜欢绿色但他更喜欢的是橙色"),
        ]
    elif role == "teacher":
        docs = [
            Document(page_content="张老师喜欢紫色"),
            Document(page_content="李老师喜欢黄色和蓝色"),
        ]
    return docs

prompt = PromptTemplate.from_template(
    "每个人喜欢的颜色是什么： \n {context}"
)
answer_chain_default = create_stuff_documents_chain(
    llm=model,
    prompt=prompt,
    output_parser=StrOutputParser()
)
# output = answer_chain_default.invoke({"context": get_docs()})
# print(f"first: {output}")

answer_chain_teacher = {"context": get_docs} | answer_chain_default
# output = answer_chain_default.invoke({"context": get_docs()})
# output = answer_chain_default.invoke({"context": get_docs("teacher")})
# output = answer_chain_teacher.invoke("student")
# print(f"second: {output}")

prompt_color = PromptTemplate.from_template(
    "谁最喜欢{color}: \n {context}"
)
who_like_color_chain = {
    "context": RunnableLambda(lambda x: x["role"]) | answer_chain_teacher,
    "color": RunnableLambda(lambda x: x["color"])
} | prompt_color | model
output = who_like_color_chain.invoke({"role": "teacher", "color": "红色"})
print(f"third: {output}")
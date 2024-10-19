import os
from dotenv import load_dotenv
from langchain_community.llms import Tongyi

load_dotenv('D:/PycharmProjects/Langchain-Chatchat/.env')  # 指定加载 env 文件
key = os.getenv('DASHSCOPE_API_KEY')  # 获得指定环境变量
DASHSCOPE_API_KEY = os.environ["DASHSCOPE_API_KEY"]  # 获得指定环境变量
model = Tongyi(temperature=1)

from langchain_core.prompts import PromptTemplate, format_document
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import ArxivLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 加载 arXiv 上的论文《ReAct: Synergizing Reasoning and Acting in Language Models》
loader = ArxivLoader(
    query="2210.03629",
    load_max_docs=1  # 加载第一个匹配的文档
)
docs = loader.load()
print(docs[0].metadata)

# 把文本分割成 500 字一组的切片
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=0  # 要求文本没有重叠
)
chunks = text_splitter.split_documents(docs)

# 构建 Stuff 形态（即文本直接拼合）的总结链
doc_prompt = PromptTemplate.from_template("{page_content}")
chain = (
        {
            "content": lambda docs: "\n\n".join(
                format_document(doc, doc_prompt) for doc in docs
            )
        }
        | PromptTemplate.from_template("用中文总结以下内容，不需要人物介绍，字数控制在 50 字以内：\n\n{content}")
        | model
        | StrOutputParser()
)
# 由于论文很长，我们只选取前 2000 字作为输入并调用总结链
res = chain.invoke(chunks[:4])
print(res)
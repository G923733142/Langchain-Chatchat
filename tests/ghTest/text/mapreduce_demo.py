import os
from dotenv import load_dotenv
from langchain_community.llms import Tongyi

load_dotenv('D:/PycharmProjects/Langchain-Chatchat/.env')  # 指定加载 env 文件
key = os.getenv('DASHSCOPE_API_KEY')  # 获得指定环境变量
DASHSCOPE_API_KEY = os.environ["DASHSCOPE_API_KEY"]  # 获得指定环境变量
model = Tongyi(temperature=1)

from functools import partial
from langchain_core.prompts import PromptTemplate, format_document
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import ArxivLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 加载 arXiv 上的论文《ReAct: Synergizing Reasoning and Acting in Language Models》
loader = ArxivLoader(query="2210.03629", load_max_docs=1)
docs = loader.load()

# 把文本分割成 500 字一组的切片
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50  # 允许文档重叠字数
)
chunks = text_splitter.split_documents(docs)

# 构建工具函数：将 Document 转换成字符串
document_prompt = PromptTemplate.from_template("{page_content}")
partial_format_document = partial(format_document, prompt=document_prompt)

# 构建 Map 链：对每个文档都先进行一轮总结
map_chain = (
        {"context": partial_format_document}
        | PromptTemplate.from_template("Summarize this content:\n\n{context}")
        | model
        | StrOutputParser()
)

# 构建 Reduce 链：合并之前的所有总结内容
reduce_chain = (
        {"context": lambda strs: "\n\n".join(strs)}
        | PromptTemplate.from_template("Combine these summaries:\n\n{context}")
        | model
        | StrOutputParser()
)

# 把两个链合并成 MapReduce 链
map_reduce = map_chain.map() | reduce_chain
res = map_reduce.invoke(chunks[:4], config={"max_concurrency": 2})
print(res)
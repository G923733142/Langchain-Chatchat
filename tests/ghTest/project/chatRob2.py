import datetime

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.output_parsers import PydanticOutputParser
from langchain_community.chat_models import ChatTongyi
from langchain_core.pydantic_v1 import BaseModel, Field
from g4f.client import Client
from langchain_core.outputs.generation import Generation
from langchain_core.outputs.llm_result import LLMResult
from langchain_core.language_models.llms import BaseLLM
from typing import List, Any
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from torch.cpu import stream


model = ChatTongyi(model_name="qwen-max", model_kwargs={"temperature": 0.01}, streaming=True)
memory_key = "history"

prompt = ChatPromptTemplate.from_messages([
    ("system", "you are a help chatbot"),
    MessagesPlaceholder(variable_name=memory_key),
    ("human", "{input}")
])

memory = ConversationBufferMemory(memory_key=memory_key, return_messages=True)

conversation_chain = ConversationChain(
    llm=model,
    prompt=prompt,
    memory=memory,
)

while True:
    user_input = input("user: ")
    if user_input == "quit":
        break
    print(f'{"-"*50} \n {memory.load_memory_variables()} \n {"-"*50}')
    print("Ai: ", end="")
    for chunk in conversation_chain.stream({"input": user_input}):
        print(chunk["response"], end="", flush=True)
    print()





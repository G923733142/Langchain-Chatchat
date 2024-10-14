from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
memory.chat_memory.add_user_message("您好")
memory.chat_memory.add_ai_message("您好")
print(memory)

outputStr = memory.load_memory_variables({})
print(outputStr['chat_history'])

prompt = PromptTemplate.from_template("聊天历史： \n {chat_history} \n")
outputStr = prompt.format(**memory.load_memory_variables({}))
print(outputStr)
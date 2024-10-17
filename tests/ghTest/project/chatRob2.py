from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from mpmath import convert

model = ChatTongyi(model_name="qwen-max", model_kwargs={"temperature": 0.01}, streaming=True)
memory_key = "history"
memory = ConversationBufferMemory(memory_key=memory_key, return_messages=True)
messages_placeholder = MessagesPlaceholder(variable_name=memory_key)
# memory.chat_memory.add_user_message("您好")

# outputstr = messages_placeholder.format_messages(**memory.load_memory_variables({}))
# print(outputstr)

prompt = ChatPromptTemplate.from_messages([
    ("system", "you are a help chatbot"),
    # SystemMessage(content="you are a help chatbot"),
    messages_placeholder,
    ("human", "{input}"),
    # HumanMessagePromptTemplate.from_template("{input}"),
])


conversation_chain = ConversationChain(
    llm=model,
    prompt=prompt,
    memory=memory,
)

while True:
    user_input = input("user: ")
    if user_input == "quit":
        break
    memory_dict = memory.load_memory_variables({})
    print(f'{"-"*50} \n {memory.load_memory_variables({})} \n  {"-"*50}')
    print(f'{"-" * 50} \n {prompt.format(input=user_input, history=memory_dict[memory_key])} \n  {"-" * 50}')

    print("Ai: ", end="")
    for chunk in conversation_chain.stream({"input": user_input}):
        # print(f"chunk: {chunk}")
        print(chunk["response"], end="", flush=True)
    print()





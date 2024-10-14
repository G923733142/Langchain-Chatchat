from langchain_community.chat_models import ChatTongyi
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate

chat_template = ChatPromptTemplate.from_messages(
    [
        ("system", "you name is {name}"),
        ("human", "你好"),
        ("ai", "你好"),
        ("human", "{user_input}"),
    ]
)

message = chat_template.format_messages(name="老王", user_input="你叫啥")
print(message)
#
# human_message_template = HumanMessagePromptTemplate.from_template("{text}")
# print(human_message_template)
#
# chat_template2 = ChatPromptTemplate.from_messages(
#     [
#         SystemMessage(
#             content=("你喜欢讲笑话")
#         ),
#         human_message_template
#     ]
# )
# message = chat_template2.format_messages(text="今天天气真好")
# print(message)

chat_template3 = ChatPromptTemplate.from_messages(
    [
        SystemMessage(
            content=("你是一个翻译官，你的任务是将用户的输入文本，翻译成英文")
        ),
        HumanMessage(content="你好"),
        AIMessage(content="hello"),
        HumanMessagePromptTemplate.from_template("{text}"),
    ]
)

model = ChatTongyi(model_name="qwen-max")
chain = chat_template3 | model
outputStr = chain.invoke({"text": "我喜欢跑步"})
print(outputStr)


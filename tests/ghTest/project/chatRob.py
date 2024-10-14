import datetime

from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field
from g4f.client import Client
from langchain_core.outputs.generation import Generation
from langchain_core.outputs.llm_result import LLMResult
from langchain_core.language_models.llms import BaseLLM
from typing import List, Any
from langchain_core.prompts import PromptTemplate


chat_history = [
    {
        "role": "system",
        "content": "you are a helpful assistant"
    }
]

class GhG4f(BaseLLM):
    client: Client = Client()

    def streamChat(self, prompt):
        stream = self.client.chat.completions.create(
            # model="gpt-4o-mini",
            model="gpt-3.5-turbo",
            stream=True,
            messages=[
                {
                    "role": "user",
                    "content": prompt

                }
            ]
        )

        model_response = "";
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                model_response += chunk.choices[0].delta.content
                # print(chunk.choices[0].delta.content, end="")
        print("完整回应：", model_response)
        return model_response

    def _generate(self, prompts: List[str], *args, **kwargs: Any) -> LLMResult:
        results = []
        for prompt in prompts:
            model_response = self.streamChat(prompt=prompt)
            result = Generation(text=f"Ai返回：{model_response}")
            results.append(result)
        return LLMResult(generations=[results])

    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "GhG4f"

class LogModel(BaseModel):
    user_input: str = Field(description="用户输入的内容")
    llm_output: str = Field(description="大模型的输出")

# model = GhG4f()
# prompt_template = PromptTemplate.from_template("今天天气")
# outStr = model.invoke(prompt_template.format())
# print(outStr)


model = GhG4f()
prompt_template = PromptTemplate.from_template("按照如下的格式回答用户的问题 \n {_format} \n {query}")
parser = PydanticOutputParser(pydantic_object=LogModel)

while True:
    user_input = input("user: ")
    if user_input == "quit":
        break
    response = model.invoke(prompt_template.format(
            query=user_input,
            _format=parser.get_format_instructions()
        )
    )
    log_model_obj = parser.parse(response)
    print(f"Ai: {log_model_obj.llm_output}")
    now = datetime.datetime.now()
    formatted_time = now.strftime("%I:%M:%S %p")
    print(f"{formatted_time}-INFO: User: {user_input}, Ai: {log_model_obj.llm_output}" )






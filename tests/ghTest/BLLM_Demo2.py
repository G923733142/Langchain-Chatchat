from typing import List, Optional, Any

from langchain_core.outputs.generation import Generation
from langchain_core.outputs.llm_result import LLMResult
from langchain_core.language_models.llms import BaseLLM
from langchain_core.prompts import PromptTemplate
from sympy.polys.polyconfig import query


# model = Tongyi(model_name='qwen-max')
# str = model.invoke("say hello")
# print(str)

class Superman(BaseLLM):

    def _generate(self, prompts: List[str], *args, **kwargs: Any) -> LLMResult:
        results = []
        for prompt in prompts:
            # results = self.llm.generate(prompt, *args, **kwargs)
            result = Generation(text=f"收到{prompt}")
            results.append(result)
        return LLMResult(generations=[results])

    @property
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "superman"

model = Superman()
prompt_template = PromptTemplate.from_template("say hello, {query}")
chain = prompt_template | model
output = chain.invoke({"query": "gh"})
print(output)



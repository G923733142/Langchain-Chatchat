from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_community.llms.tongyi import Tongyi

# langchain-core==0.1.5 可以

if __name__ == '__main__':
    model = Tongyi(model_name='qwen-plus',  streaming=True)
    parser = JsonOutputParser()

    prompt = PromptTemplate(
        template="Answer the user query.\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()}
    )

    chain = prompt | model | parser
    print(parser.get_format_instructions().format())

    # for s in chain.stream({"query": "给我讲个101字的笑话"}):
    #     print(s)
    print(prompt.format(query="给我讲3个101字的笑话"))
    output = model.invoke(prompt.format(query="给我讲个101字的笑话"))
    print(output)
    print(parser.parse(output))
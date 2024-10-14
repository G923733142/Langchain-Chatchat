

from langchain_community.llms.tongyi import Tongyi
from langchain.prompts import PromptTemplate
from langchain.prompts.few_shot import FewShotPromptTemplate


from langchain_community.vectorstores import Chroma

from langchain.prompts.example_selector import SemanticSimilarityExampleSelector

from langchain_community.embeddings import DashScopeEmbeddings



def prompt_template_demo():
    prompt_template = PromptTemplate.from_template(
        "给我讲一个关于{topic}的笑话"
    )
    str = prompt_template.format(topic="足球")
    print(str)

def tongyi_demo():
    prompt_template = PromptTemplate.from_template(
        "给我讲一个关于{topic}的笑话"
    )
    model = Tongyi()
    str = model.invoke(prompt_template.format(topic="足球"))
    print(str)

# tongyi_demo()

"""
根据示例格式来回答问题
"""
def few_shot_demo():
    examples = [
        {
            "question": "介绍下python",
            "answer": """ 介绍下python，回答：找p老师 """
        },
        {
            "question": "介绍下清朝的历史",
            "answer": """ 介绍下清朝的历史，回答：找无老师 """
        }
    ]

    example_prompt = PromptTemplate(
        input_variables=["question", "answer"], template="Question: {question}\n Answer: {answer}"
    )
    question = "明朝最出名的历史人物是谁"
    all_examples_prompt = FewShotPromptTemplate(
        examples=examples,
        example_prompt=example_prompt,
        prefix="参考下面的示例，回答问题：\n<example>",
        suffix="</example>\n\n Question: {input}\n AI:",
        input_variables=["input"],
    )

    str = all_examples_prompt.format(input=question)
    print(str)
    model = Tongyi()
    str = model.invoke(str)
    print(str)

# few_shot_demo()
# tongyi_demo()
# 从 示例中找出，与语义最相近的示例，来回答
def examples_selector_demo():

    examples = [
        {
            "question": "介绍下python",
            "answer": """ 介绍下python，回答：找p老师 """
        },
        {
            "question": "介绍下清朝的历史",
            "answer": """ 介绍下清朝的历史，回答：找无老师 """
        }
    ]

    example_prompt = PromptTemplate(
        input_variables=["question", "answer"], template="Question: {question}\n Answer: {answer}"
    )
    question = "明朝最出名的历史人物是谁"
    embeddings = DashScopeEmbeddings()

    print("Examples:", examples)
    print("Embeddings:", embeddings)
    print("Vector store class:", Chroma)

    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples=examples,
        embeddings=embeddings,
        vectorstore_cls=Chroma,
        k=1
    )

    selected_examples = example_selector.select_examples({"question": question})
    print(f"Example most similar to the input: {question}")
    for example in selected_examples:
        print("\n")
        for k, v in example.items():
            print(f"{k}: {v}")

examples_selector_demo()
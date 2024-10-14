from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma
from langchain.vectorstores import Redis
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain_community.embeddings import QianfanEmbeddingsEndpoint
# 初始化OpenAI Embeddings（这里使用OpenAI的Embeddings，您也可以选择其他Embeddings）
embeddings = QianfanEmbeddingsEndpoint(
    model="Embedding-V1",
    qianfan_ak="7FAxtDxjQKg3hinsjnDLwTrA",
    qianfan_sk="yZje8joVWI32rkcaNZ7UNPeyirxeweoH"
)

# 示例数据
examples = [
    # {
    #     "question": "介绍下Python",
    #     "answer": "Python是一种高级编程语言，以其简洁的语法和强大的功能受到广泛欢迎。"
    # },
    {
        "question": "介绍下清朝的历史",
        "answer": "清朝是中国历史上最后一个封建王朝，存在了近三百年。"
    },
    {
        "question": "明朝最出名的历史人物是谁",
        "answer": "明朝最出名的历史人物之一是朱元璋，他是明朝的开国皇帝。"
    }
]

# 创建PromptTemplate
example_prompt = PromptTemplate(
    input_variables=["question", "answer"],
    template="Question: {question}\nAnswer: {answer}"
)

# 创建SemanticSimilarityExampleSelector实例
example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    embeddings,
    Chroma,
    k=1
)

# 测试用例
test_question = "明朝的开国皇帝是谁"

# 选择最相似的例子
selected_examples = example_selector.select_examples({"question": test_question})

# 输出结果
print(f"Example most similar to the input: {test_question}")
for example in selected_examples:
    print("\n ", example)
    for k, v in example.items():
        print(f"{k}: {v}")
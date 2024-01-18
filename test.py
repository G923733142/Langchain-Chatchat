import os

# 获取当前文件的绝对路径
current_file_path = os.path.abspath(__file__)

model_path = os.path.join(os.path.dirname(current_file_path), 'moka-ai/m3e-base')

from sentence_transformers import SentenceTransformer

print('time to load model')

model = SentenceTransformer(model_path)

print('time to encode')
#Our sentences we like to encode
sentences = [
    '* Moka 此文本嵌入模型由 MokaAI 训练并开源，训练脚本使用 uniem',
    '* Massive 此文本嵌入模型通过**千万级**的中文句对数据集进行训练',
    '* Mixed 此文本嵌入模型支持中英双语的同质文本相似度计算，异质文本检索等功能，未来还会支持代码检索，ALL in one'
]


#Sentences are encoded by calling model.encode()
embeddings = model.encode(sentences)

print('time to print')
#Print the embeddings
for sentence, embedding in zip(sentences, embeddings):
    print("Sentence:", sentence)
    print("Embedding:", embedding)
    print("")
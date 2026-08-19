from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()

llm = ChatOpenAI(
    model=os.getenv("llm_model"),
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("base_url")
)

chunks = []
text_parts = []

for index,chunk in enumerate(llm.stream(input="请用三句话解释RAG")):
    chunks.append(chunk)
    print(f"\n===== chunk {index} =====")
    print("chunk_type:", type(chunk).__name__)
    print("content_type:", type(chunk.content).__name__)
    print("content:", repr(chunk.content))
    print("response_metadata:", chunk.response_metadata)
    print("usage_metadata:", chunk.usage_metadata)

    # 当前实验限定为纯文本输出
    if isinstance(chunk.content, str) and chunk.content:
        text_parts.append(chunk.content)

print("\n===== 边界汇总 =====")

if chunks:
    print("chunk_count:", len(chunks))
    print("first_chunk:", repr(chunks[0].content))
    print("last_chunk:", repr(chunks[-1].content))

    if len(chunks) >= 3:
        middle_index = len(chunks) // 2
        print("middle_index:", middle_index)
        print("middle_chunk:", repr(chunks[middle_index].content))

empty_indexes = [
    index
    for index, chunk in enumerate(chunks)
    if chunk.content == ""
]

print("empty_content_indexes:", empty_indexes)
print("empty_content_count:", len(empty_indexes))
print("final_text:", "".join(text_parts))


"""
实验记录：

===== chunk 0 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 1 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 2 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 3 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 4 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 5 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 6 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 7 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 8 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 9 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 10 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 11 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 12 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 13 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 14 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 15 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 16 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 17 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 18 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 19 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 20 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 21 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 22 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 23 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 24 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 25 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 26 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 27 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 28 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 29 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 30 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 31 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 32 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 33 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 34 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 35 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 36 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 37 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 38 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 39 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 40 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 41 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 42 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 43 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 44 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 45 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 46 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 47 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 48 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 49 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 50 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 51 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 52 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 53 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 54 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 55 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 56 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 57 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 58 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 59 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 60 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 61 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 62 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 63 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 64 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 65 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 66 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 67 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 68 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 69 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 70 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 71 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 72 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 73 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 74 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 75 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 76 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 77 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 78 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 79 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 80 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 81 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 82 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 83 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 84 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 85 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 86 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 87 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 88 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 89 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 90 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 91 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 92 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 93 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 94 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 95 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 96 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 97 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 98 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 99 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 100 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 101 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 102 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 103 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 104 =====
chunk_type: AIMessageChunk
content_type: str
content: 'RAG（'
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 105 =====
chunk_type: AIMessageChunk
content_type: str
content: '检索增强生成）'
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 106 =====
chunk_type: AIMessageChunk
content_type: str
content: '是一种将外部知识'
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 107 =====
chunk_type: AIMessageChunk
content_type: str
content: '检索与大语言模型'
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 108 =====
chunk_type: AIMessageChunk
content_type: str
content: '生成能力相结合的人工智能'
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 109 =====
chunk_type: AIMessageChunk
content_type: str
content: '技术。它在生成'
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 110 =====
chunk_type: AIMessageChunk
content_type: str
content: '回答前，'
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 111 =====
chunk_type: AIMessageChunk
content_type: str
content: '会先从外部知识库'
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 112 =====
chunk_type: AIMessageChunk
content_type: str
content: '中检索出与'
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 113 =====
chunk_type: AIMessageChunk
content_type: str
content: '问题相关的准确信息'
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 114 =====
chunk_type: AIMessageChunk
content_type: str
content: '，并将其作为上下文'
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 115 =====
chunk_type: AIMessageChunk
content_type: str
content: '提供给大模型。'
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 116 =====
chunk_type: AIMessageChunk
content_type: str
content: '这种方式不仅让模型'
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 117 =====
chunk_type: AIMessageChunk
content_type: str
content: '的回答更加准确和'
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 118 =====
chunk_type: AIMessageChunk
content_type: str
content: '具有时效性，'
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 119 =====
chunk_type: AIMessageChunk
content_type: str
content: '还有效解决了大'
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 120 =====
chunk_type: AIMessageChunk
content_type: str
content: '模型容易产生“幻觉'
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 121 =====
chunk_type: AIMessageChunk
content_type: str
content: '”和知识滞'
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 122 =====
chunk_type: AIMessageChunk
content_type: str
content: '后的问题。'
response_metadata: {'model_provider': 'openai'}
usage_metadata: None

===== chunk 123 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {'finish_reason': 'stop', 'model_name': 'qwen3.7-plus', 'model_provider': 'openai'}
usage_metadata: None

===== chunk 124 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {}
usage_metadata: {'input_tokens': 16, 'output_tokens': 440, 'total_tokens': 456, 'input_token_details': {'cache_read': 0}, 'output_token_details': {'reasoning': 362}}

===== chunk 125 =====
chunk_type: AIMessageChunk
content_type: str
content: ''
response_metadata: {}
usage_metadata: None

===== 边界汇总 =====
chunk_count: 126
first_chunk: ''
last_chunk: ''
middle_index: 63
middle_chunk: ''
empty_content_indexes: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 123, 124, 125]
empty_content_count: 107
final_text: RAG（检索增强生成）是一种将外部知识检索与大语言模型生成能力相结合的人工智能技术。它在生成回答前，会先从外部知识库中检索出与问题相关的准确信息，并将其作 为上下文提供给大模型。这种方式不仅让模型的回答更加准确和具有时效性，还有效解决了大模型容易产生“幻觉”和知识滞后的问题。

实验结论：
本次llm.stream()共返回126个AIMessageChunk.首块的content为''，中间块包含''和'值'，末块的content为''。
共有107个块正文为空，但其response_metadata包含provider、finish_reason、model_name，第124个块还计算了总的token消费量。
因此，应用不能假设每个chunk都有正文，应检查content后再显示或拼接。跳过空正文块不会丢失最终回答。
"""

    
        

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()

prompt_template = PromptTemplate.from_template(
    "你现在需要完成文本分类任务，任务要求：{task},分类标签：{labels},待分类文本：{text}"
)
task1 = "情感分类"
task1_labels = ["正面","负面","中性"]
task1_text = "这个产品体验很好，运行速度也很快，我很满意。"
prompt_text_1 = prompt_template.invoke({"task":task1,"labels":task1_labels,"text":task1_text})

task2 = "文本主题分类"
task2_labels = ["科技","金融","体育","娱乐"]
task2_text = "英伟达发布了新一代 GPU，并重点提升了 AI 推理性能。"
prompt_text_2 = prompt_template.format(task=task2,labels=task2_labels,text=task2_text)

llm = ChatOpenAI(
    model=os.getenv("llm_model"),
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("base_url")
)
print(prompt_text_1.to_string())
res = llm.invoke(input=prompt_text_1)
print(res.content)

print(prompt_text_2)
for chunk in llm.stream(input=prompt_text_2):
    print(chunk.content,end="",flush=True)
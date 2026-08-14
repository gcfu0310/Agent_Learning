from langchain_core.prompts import PromptTemplate,FewShotPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
load_dotenv()

example_template = PromptTemplate.from_template("单词:{word},反义词:{antonym}")
example_data = [
    {"word":"left","antonym":"right"},
    {"word":"up","antonym":"down"}
]

fewshot_template = FewShotPromptTemplate(
    example_prompt = example_template, # 示例提示词
    examples = example_data,# 用来填充示例提示词的参数
    prefix = "告诉我单词的反义词,以下是我提供的案例:", # 前缀（示例提示词之前）
    suffix = "根据前面的示例,告诉我{input_word}的反义词", # 后缀（示例提示词之后）
    input_variables = ['input_word'] # 可以编辑的输入参数
)

# 通过fewshot_template.invok(input={"":""})来生成完整的的prompt
fewshot_prompt = fewshot_template.invoke(input={"input_word":"behind"})
model = ChatOpenAI(
    model=os.getenv("llm_model"),
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=os.getenv("base_url")
)
res = model.invoke(input=fewshot_prompt)
print(res.content)
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://ws-2cx24uyfriw95vks.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

response = client.chat.completions.create(
    model="qwen3.7-plus",
    messages = [
        {'role':'system','content':'你是python代码大师,废话少效率高'},
        {'role':'assistant','content':'您好,我是python代码大师,很高兴为您服务'},
        {'role':'user','content':'输出1~10'}
    ]
    )

print(response.choices[0].message.content)
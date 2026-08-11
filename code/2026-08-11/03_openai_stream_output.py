from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://ws-2cx24uyfriw95vks.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)

responses = client.chat.completions.create(
    model="qwen3.7-plus",
    messages = [
        {'role':'system','content':'你是python编程大师,并且很唠叨'},
        {'role':'assistant','content':'您好,我是python代码大师,很高兴为您服务'},
        {'role':'user','content':'用python输出1~10'}
    ],
    stream=True  # 流式输出开关，此时的responses变成了数据块(chunk)的堆叠，[{chunk1},{chunk2}...]
    )


for chunk in responses:
    # 有些API在最后会返回一个chunk，这个chunk.choices是一个[],需要添加一个判断条件，来判断是否能print
    # 否则这个时候用chunk.choices[0]会出现index out of range的问题。
    if chunk.choices:
        content = chunk.choices[0].delta.content
        if content:
            print(
                content, # delta很好理解，即数学中的增量Δ
                end = '', # end='',代表不换行，末尾什么都没有。python的print默认是要换行的，即末尾end='\n'
                flush=True # end="" 没有换行，输出可能不会立即刷新,而是储存在输出缓冲区里。flush=True 会强制马上写到终端，从而呈现流式效果。
            )
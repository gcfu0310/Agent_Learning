from langchain_core.prompts import PromptTemplate,FewShotPromptTemplate,ChatPromptTemplate

"""
PromptTemplate->StringPromptTemplate->BasePromptTemplate->RunnableSerializable->Runnable
FewShotPromptTemplate->StringPromptTemplate->BasePromptTemplate
三个prompt模板类都是继承于Runnable类,可以作为chain连接的一部分
"""

prompt_template = PromptTemplate.from_template("我是{name},我喜欢{hobby}")
res1 = prompt_template.format(name="熊莉",hobby="睡觉")
print(res1,type(res1)) # format生成的prompt是str类型的
res2 = prompt_template.invoke({"name":"熊莉","hobby":"睡觉"})
print(res2,type(res2)) # invoke生成的prompt是StringPromptValue
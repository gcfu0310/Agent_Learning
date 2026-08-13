import json

s = {
    "name":"yuanshen",
    "age":7,
    "gender":"neutral"
}

# json.dunmps(s,ensure_ascii=False),将python的列表或是字典对象，转换成json格式
s1 = json.dumps(s,ensure_ascii=False)
print(s1)

c = [
    {
    "name":"yuanshen",
    "age":7,
    "gender":"neutral"
    },
    {
    "name":"xingqiongguidao",
    "age":4,
    "gender":"neutral"
    },
    {
    "name":"zzz",
    "age":2,
    "gender":"neutral"
    }
]
c1 = json.dumps(c,ensure_ascii=False)
print(c1)

# json.loads(s):将json字符串s转变为python的字典或列表格式
# 注意json.load()是从json文件中读取并解析，json.loads()是解析json字符串
s = """
{
    "name":"yuanshen",
    "age":7,
    "gender":"neutral"
}
"""
s1 = json.loads(s)
print(type(s1))


c = """
[
    {
    "name":"yuanshen",
    "age":7,
    "gender":"neutral"
    },
    {
    "name":"xingqiongguidao",
    "age":4,
    "gender":"neutral"
    },
    {
    "name":"zzz",
    "age":2,
    "gender":"neutral"
    }
]
"""
c1 = json.loads(c)
print(type(c1))
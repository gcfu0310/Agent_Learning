from langchain_community.document_loaders import JSONLoader

# 依托jq schema语法
json_loader = JSONLoader(
    file_path="./code/2026-08-18/data/stu.json",
    jq_schema=".name"
)
doc = json_loader.load()
# print(doc)

# 待取内容不是字符串时
json_loader_1 = JSONLoader(
    file_path="./code/2026-08-18/data/stu.json",
    jq_schema=".",
    text_content=False # text_content:默认你取的内容是字符串，所以当你取的内容不是字符串，如：字典、数组...,需要把它设置成False,否则报错
)
doc_1 = json_loader_1.load()
# print(doc_1)

# json文件是json数组形式时
json_loader_2 = JSONLoader(
    file_path="./code/2026-08-18/data/stus.json",
    jq_schema=".[].name", # 注意jq_schema的写法，[]代表整个数组,前后两个'.'的含义不同
    text_content=False # text_content:默认你取的内容是字符串，所以当你取的内容不是字符串，如：字典、数组...,需要把它设置成False,否则报错
)
doc_2 = json_loader_2.load()
# print(doc_2)

# json文件是json_line的形式时
json_loader_3 = JSONLoader(
    file_path="./code/2026-08-18/data/stu_json_lines.json",
    jq_schema=".name", # 注意jq_schema的写法
    text_content=False, # text_content:默认你取的内容是字符串，所以当你取的内容不是字符串，如：字典、数组...,需要把它设置成False,否则报错
    json_lines=True # json_line:默认读取的json文件不是json_lines的形式(False)，所以当你取的内容是json_lines时，需要把它设置成True
)
doc_3 = json_loader_3.load()
print(doc_3)
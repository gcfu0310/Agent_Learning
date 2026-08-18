from langchain_community.document_loaders import CSVLoader

# langchain中加载文件，加载器+加载方法
# 定义加载器
loader = CSVLoader(
    file_path="D:/Agent-Learning/code/2026-08-18/data/stu.csv",
    csv_args={
        "delimiter":",", # 指定分隔符
        "quotechar":'"', # 指定带有分隔符文本的引号包围是双引号还是单引号
        # 如果有表头就不需要下面这部分内容了
        # "fieldnames":['name','age','gender','爱好']
    },
    encoding="utf-8"
)

# 批量加载 .load() -> [Document,Document...]
# documents = loader.load()
# for doc in documents:
#     print(type(doc),doc)

# 懒加载 .lazy_load() -> 迭代器[Document] 当需要加载的数据很大的时候
for doc in loader.lazy_load():
    print(doc)
from langchain_community.document_loaders import PyPDFLoader

pdf_loader = PyPDFLoader(
    file_path="D:/Agent-Learning/code/2026-08-19/data/pdf2.pdf",
    mode="page", # mode="page"每个页面返回一个Document对象，mode="single"返回一整个Document对象
    password="itheima"
)

i = 0
for chunk in pdf_loader.lazy_load():
    i += 1
    print(chunk.page_content)
    print("="*20,i)
import streamlit as st
import time
from knowledge_base import KnowledgeBaseService
# streamlit特点:只要组件发生变化，代码都要重头跑一遍，这样会导致丢失状态，因此需要保存状态
st.title("知识库更新服务")

uploader_file = st.file_uploader(
    label = "请上传TXT文件",
    accept_multiple_files=False, # Fasle代表只支持单文件
    type=["txt"]
)

if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()

if uploader_file is not None:
    # 提取文件的信息
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size / 1024 # 单位是KB

    st.subheader(file_name)
    st.write(f"格式：{file_type} | 大小：{file_size:.2f}KB")

    # get_value -> Byte -> decode(utf-8) -> str
    text = uploader_file.getvalue().decode(encoding="utf-8")
    with st.spinner("载入知识库中..."): # 在st.spinner下面的代码执行过程中，会有一个转圈动画
        time.sleep(1)
        result = st.session_state["service"].upload_by_str(text,file_name)
        st.write(result)
    # st.write(text)
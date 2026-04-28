"""
基于Streamlit完成web网页上传文件服务
当web页面元素发生变化，整个代码会重新执行
"""

import time

import streamlit as st
from knowledge_base import KnowledgeBaseService

# 设置页面标题
st.title("知识库更新服务")

# 文件上传组件
uploaded_file = st.file_uploader(
    "选择一个文件上传", 
    type=["txt"], 
    accept_multiple_files=False
)

if "service" not in st.session_state:
    st.session_state["service"] = KnowledgeBaseService()  # 创建知识库服务实例



if uploaded_file is not None:
    # 处理上传的文件
    file_name = uploaded_file.name
    file_type = uploaded_file.type
    file_size = uploaded_file.size / 1024  # 转换为KB

    st.subheader("文件信息")
    st.write(f"文件名: {file_name}")
    st.write(f"文件类型: {file_type}")
    st.write(f"文件大小: {file_size:.2f} KB")

    # 读取文件内容 getvalue() -> bytes -> decode() -> str
    text = uploaded_file.getvalue().decode("utf-8") 
    
    with st.spinner("正在处理文件..."):
        time.sleep(1)  # 模拟处理时间
        result = st.session_state["service"].upload_by_str(text , file_name)
        st.write(result)
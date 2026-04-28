import time
from rag import RagServer
import streamlit as st
import config_data as config


# 标题
st.title("知识库问答服务")
st.divider()     # 分割线

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role":"assistant", "content":"你好！有什么我可以帮你的吗？"}]  # 存储对话历史记录的列表

if "rag" not in st.session_state:
    st.session_state["rag"] = RagServer()

for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])  # 根据角色显示消息

# 页面最下方提供输入框
prompt = st.chat_input("请输入您的问题")

if prompt:

    st.chat_message("user").write(prompt)

    st.session_state["messages"].append({"role":"user", "content":prompt})
    
    ai_res_list = []
    with st.spinner("正在处理您的问题..."):
        res_stream = st.session_state["rag"].chain.stream({"input": prompt}, config.session_config)

        def capture(generator, capture_list):
            for chunk in generator:
                capture_list.append(chunk)
                yield chunk
            

        st.chat_message("assistant").write_stream(capture(res_stream, ai_res_list))
        st.session_state["messages"].append({"role":"assistant", "content":"".join(ai_res_list)})

        # ["a", "b", "c"]  "".join() -> "abc"
        # ["a", "b", "c"]  ",".join() -> "a,b,c"


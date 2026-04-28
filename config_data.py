
md5_path = "md5.text"

# chroma
collection_name = "rag"
persist_directory = "chroma_db"


#spliter
chunk_size = 100
chunk_overlap = 10
separators = ["\n\n", "\r\n\r\n", "\n", "。", "！", "？", ".", "!", "?", "，", ",", " ", ""]
max_split_char_number = 1000        # 文本分割的阈值
top_k = 3


similarity_threshold = 0.8

embedding_model_name = "text-embedding-v4"
chat_model_name = "deepseek-v3.1"

session_config = {
        "configurable": {"session_id": "user_001"}
    }
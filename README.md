# RAG知识库问答系统

一个基于LangChain和Streamlit构建的RAG（Retrieval-Augmented Generation）知识库问答系统，支持文档上传、向量化存储和智能问答功能。

## 🚀 功能特性

### 核心功能
- **📚 知识库管理**：支持文本文件的上传和管理
- **🔍 智能检索**：基于向量相似度的文档检索
- **🤖 AI问答**：集成通义千问大模型进行智能回答
- **💬 对话历史**：自动保存会话记录，支持上下文理解
- **🌐 Web界面**：基于Streamlit的可视化操作界面

### 技术栈
- **Python 3.8+**
- **LangChain**：RAG框架核心
- **Streamlit**：Web界面
- **Chroma**：向量数据库
- **通义千问**：语言模型
- **DashScope**：嵌入模型服务

## 📦 快速开始

### 环境要求
- Python 3.8或更高版本
- pip包管理器

### 安装依赖
```bash
pip install streamlit langchain langchain-chroma langchain-community dashscope
```

### 配置API密钥
在运行前，请确保设置DashScope API密钥：
```bash
export DASHSCOPE_API_KEY="your-api-key-here"
```

或者直接在代码中设置：
```python
import os
os.environ["DASHSCOPE_API_KEY"] = "your-api-key-here"
```

### 运行应用

1. **启动知识库问答服务**：
   ```bash
   streamlit run app_qa.py
   ```

2. **上传文档到知识库**：
   ```bash
   streamlit run app_file_uploader.py
   ```

## 🏗️ 项目结构

```
├── app_qa.py                 # 主问答界面
├── app_file_uploader.py      # 文件上传界面
├── rag.py                    # RAG核心服务
├── knowledge_base.py         # 知识库管理
├── vector_stores.py          # 向量存储服务
├── file_history_store.py     # 对话历史存储
├── config_data.py            # 配置文件
└── README.md                # 本文件
```

## ⚙️ 配置说明

主要配置项位于 `config_data.py` 文件中：

### 向量数据库配置
- `collection_name`: 向量集合名称（默认："rag"）
- `persist_directory`: 向量数据库存储路径（默认："chroma_db"）

### 文本分割配置
- `chunk_size`: 文本块大小（默认：100字符）
- `chunk_overlap`: 块重叠长度（默认：10字符）
- `max_split_char_number`: 分割阈值（默认：1000字符）

### 检索配置
- `top_k`: 返回结果数量（默认：3）
- `similarity_threshold`: 相似度阈值（默认：0.8）

### 模型配置
- `embedding_model_name`: 嵌入模型（默认："text-embedding-v4"）
- `chat_model_name`: 聊天模型（默认："deepseek-v3.1"）

## 📝 使用说明

### 1. 准备知识库
- 通过 `app_file_uploader.py` 上传您的文档
- 支持 `.txt` 格式文本文件
- 系统会自动计算MD5值避免重复处理

### 2. 开始问答
- 运行 `app_qa.py` 启动问答界面
- 输入您的问题
- 系统会自动检索相关文档并生成回答

### 3. 查看对话历史
- 所有会话记录会自动保存在 `chat_histories/` 目录
- 每个会话ID对应一个JSON文件

## 🔧 高级配置

### 自定义分隔符
在 `config_data.py` 中修改 `separators` 数组来自定义文本分割逻辑：
```python
separators = ["\n\n", "\n", "。", "！", "？", ".", "!", "?", "，", ",", " ", ""]
```

### 调整检索参数
- 增加 `top_k` 值获取更多相关文档
- 降低 `similarity_threshold` 提高召回率
- 调整 `chunk_size` 控制文本块大小

## 🐛 常见问题

### Q: 如何处理中文文本？
A: 系统已内置中文分词支持，无需额外配置。

### Q: 如何清理向量数据库？
A: 删除 `chroma_db/` 目录即可清空所有存储的向量数据。

### Q: 如何重置对话历史？
A: 删除 `chat_histories/` 目录下的对应会话文件。

### Q: 文件重复上传会怎样？
A: 系统会通过MD5值检测，重复文件会被自动跳过。

## 📊 性能优化建议

1. **增大chunk_size**：适合文档结构清晰的场景
2. **减小chunk_overlap**：减少冗余信息，提高效率
3. **调整top_k值**：根据响应质量需求平衡速度和准确性
4. **定期清理历史**：长时间运行后清理旧的对话记录

## 🤝 贡献指南

欢迎提交Issue和Pull Request来帮助改进项目。

## 📄 许可证

[MIT License](LICENSE)

## 🙏 致谢

- [LangChain](https://github.com/langchain-ai/langchain) - 强大的LLM应用开发框架
- [Streamlit](https://github.com/streamlit/streamlit) - 快速构建Web应用的工具
- [Chroma](https://github.com/chroma-core/chroma) - 友好的向量数据库
- [通义千问](https://tongyi.aliyun.com/) - 阿里巴巴的大语言模型服务
from langchain_chroma import Chroma
import config_data as config


class VectorStoreService:
    def __init__(self, embedding):
        self.embedding = embedding
        self.vector_store = Chroma(
            collection_name=config.collection_name,        #数据库的表名
            embedding_function=embedding,
            persist_directory=config.persist_directory,    #数据库的存储目录
        )
        
    def get_retriever(self):
        retriever = self.vector_store.as_retriever(search_kwargs={"k": config.top_k})
        return retriever


if __name__ == "__main__":
    from langchain_community.embeddings import DashScopeEmbeddings
    
    retriever  = VectorStoreService(DashScopeEmbeddings(model="text-embedding-v4")).get_retriever()

    res = retriever.invoke("晚饭想吃点清淡的，有什么推荐吗？")
    print(res)
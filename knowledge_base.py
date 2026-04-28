"""
知识库
"""

import os
import config_data as config
import hashlib
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime


def check_md5(md5_str:str):
    """
    检查文件的MD5值是否已经被处理过了
    retuen True 表示已经处理过， False 表示没有处理过
    """
    if not os.path.exists(config.md5_path):
        open(config.md5_path, "w", encoding="utf-8").close()  # 创建空文件
        return False
    else:
        for line in open(config.md5_path, "r", encoding="utf-8").readlines():
            line = line.strip()
            if line  == md5_str:
                return True
        return False



def save_md5(md5_str):
    """
    将文件的MD5值保存到一个文本文件中
    """
    with open(config.md5_path, "a", encoding="utf-8") as f:
        f.write(md5_str + "\n")



def get_string_md5(input_str):
    """
    计算字符串的MD5值
    """
    
    #将字符串转换为字节
    str_bytes = input_str.encode("utf-8")
    #创建MD5对象
    md5_obj = hashlib.md5()
    #更新MD5内容
    md5_obj.update(str_bytes)
    md5_hex = md5_obj.hexdigest()  #获取MD5的16进制字符串表示

    return md5_hex



class KnowledgeBaseService(object):

    def __init__(self):
        os.makedirs(config.persist_directory, exist_ok=True)  # 创建存储目录

        self.chroma = Chroma(
            collection_name=config.collection_name,        #数据库的表名
            embedding_function=DashScopeEmbeddings(model="text-embedding-v4"),
            persist_directory=config.persist_directory,    #数据库的存储路径
        )                                                  #向量存储的实例Chroma向量库对象
        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,                  #分隔后的文本段最大长度
            chunk_overlap=config.chunk_overlap,            #分隔后的文本段重叠长度
            separators=config.separators,                 #自然语言文本分割的分隔符列表
            length_function=len
        )  #文本分割器对象


    def upload_by_str(self , data , file_name):
        """
        将传入的字符串进行向量化，存入向量数据库中
        """
        md5_hex = get_string_md5(data)

        if check_md5(md5_hex):
            return f"文件 {file_name} 已经处理过了，跳过处理"
        
        #文本分割
        if len(data) > config.max_split_char_number:
            data_list = self.spliter.split_text(data)
        else:
            data_list = [data]
        
        metadata = {
            "source": file_name,
            "create_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "operator": "admin"
        }

        self.chroma.add_texts(data_list, metadatas=[metadata] * len(data_list)) # 将文本数据和对应的元数据添加到向量数据库中

        save_md5(md5_hex)  # 保存MD5值到文件

        return "文件 {} 已经成功处理并存储到知识库中".format(file_name)


if __name__ == "__main__":
    service = KnowledgeBaseService()
    r = service.upload_by_str("周杰伦", "testfile")
    print(r)
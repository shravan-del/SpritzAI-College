from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import JSONLoader, CSVLoader
from langchain.text_splitter import CharacterTextSplitter

def get_documents():
    loaders = [
        JSONLoader(file_path="data/anaanu_data.json", jq_schema="."),
        JSONLoader(file_path="data/reddit_data.json", jq_schema="."),
        JSONLoader(file_path="data/vt_courses.json", jq_schema="."),
        CSVLoader(file_path="data/VirginiaTech_Reddit_Classes.csv"),
        CSVLoader(file_path="data/VT_Grade_UDC_Distribution.csv"),
    ]
    docs = []
    for loader in loaders:
        docs.extend(loader.load())
    return docs

def get_retriever():
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = get_documents()
    texts = text_splitter.split_documents(docs)
    vectorstore = FAISS.from_documents(texts, OpenAIEmbeddings())
    return vectorstore.as_retriever()

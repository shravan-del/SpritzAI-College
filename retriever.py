from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import JSONLoader, CSVLoader
from langchain.text_splitter import CharacterTextSplitter

def get_documents():
    loaders = [
        JSONLoader("data/anaanu_data.json"),
        JSONLoader("data/reddit_data.json"),
        JSONLoader("data/vt_courses.json"),
        CSVLoader("data/VirginiaTech_Reddit_Classes.csv"),
        CSVLoader("data/VT_Grade_UDC_Distribution.csv"),
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
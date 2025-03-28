from langchain_community.document_loaders import JSONLoader

def get_documents():
    docs = []
    for file_path in ["anaanu_data.json", "reddit_data.json"]:
        loader = JSONLoader(
            file_path=file_path,
            jq_schema=".[]",
            content_key="GPA",  # or any other field you want to summarize
            text_content=False  # critical fix for Render crash
        )
        docs.extend(loader.load())
    return docs

def get_retriever():
    from langchain_community.vectorstores import FAISS
    from langchain_community.embeddings import OpenAIEmbeddings

    documents = get_documents()
    db = FAISS.from_documents(documents, OpenAIEmbeddings())
    return db.as_retriever()
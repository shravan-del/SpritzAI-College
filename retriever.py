import os
import pickle
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from typing import List, Dict, Optional
from dotenv import load_dotenv
from supabase_client import fetch_data


load_dotenv()

def get_documents(tags: Optional[List[str]] = None):
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

def get_retriever(tags: Optional[List[str]] = None):
    documents = get_documents(tags=tags)
    if not documents:
        raise ValueError("No documents loaded.")

    embeddings = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
    db = FAISS.from_documents(documents, embeddings)

    retriever = db.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 15,
            "fetch_k": 50,
            "lambda_mult": 0.7
        }
    )
    return retriever
def get_supabase_documents(table_name: str = "courses") -> list[Document]:
    """Fetch and convert Supabase rows into LangChain Documents."""
    rows = fetch_data(table_name)
    documents = []
    for row in rows:
        content = f"{row.get('course_code')} - {row.get('course_name')} taught by {row.get('professor')} | GPA: {row.get('GPA')} | A%: {row.get('A_grade_percentage')}"
        metadata = {
            "source": "supabase",
            "tags": ["course", "supabase"],
            "course_code": row.get("course_code"),
            "professor": row.get("professor"),
            "avg_gpa": row.get("GPA"),
            "A_percent": row.get("A_grade_percentage")
        }
        documents.append(Document(page_content=content, metadata=metadata))
    return documents

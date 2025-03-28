from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from retriever import get_retriever
import os

def get_answer(query):
    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(openai_api_key=os.environ.get("OPENAI_API_KEY"), temperature=0),
        retriever=get_retriever()
    )
    return qa.run(query)
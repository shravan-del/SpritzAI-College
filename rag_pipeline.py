from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from retriever import get_retriever

def get_answer(query):
    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(temperature=0),
        retriever=get_retriever()
    )
    return qa.run(query)
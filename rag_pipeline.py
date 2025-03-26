from retriever import get_retriever
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

retriever = get_retriever()
llm = ChatOpenAI(temperature=0)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=False
)

def get_answer(question: str) -> str:
    return qa_chain.run(question)
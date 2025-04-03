import os
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from retriever import get_retriever
from dotenv import load_dotenv

load_dotenv()

def get_answer(query: str, tags=None) -> dict:
    try:
        retriever = get_retriever(tags=tags)
        retriever.search_kwargs["k"] = 10

        prompt_template = PromptTemplate.from_template("""
        You are a helpful assistant answering questions about Virginia Tech courses.
        Use only the following context to answer. If the answer is unknown, say "I don’t know based on the data."

        Context: {context}
        Question: {question}
        """)

        qa = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(
                model_name="gpt-3.5-turbo",
                temperature=0,
                openai_api_key=os.getenv("OPENAI_API_KEY")
            ),
            retriever=retriever,
            chain_type="stuff",
            chain_type_kwargs={"prompt": prompt_template},
            return_source_documents=True
        )

        result = qa.invoke({"query": query})
        return {
            "query": query,
            "answer": result.get("result"),
            "sources": [doc.metadata.get("source", "") for doc in result.get("source_documents", [])]
        }

    except Exception as e:
        return {"error": str(e)}

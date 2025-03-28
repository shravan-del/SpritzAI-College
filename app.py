from fastapi import FastAPI
from pydantic import BaseModel
from rag_pipeline import get_answer
from pydantic import BaseModel

app = FastAPI()

class Question(BaseModel):
    question: str

@app.get("/")
def health():
    return {"status": "running"}

@app.post("/ask")
def ask(data: Question):
    response = get_answer(data.question)
    return {"response": response}

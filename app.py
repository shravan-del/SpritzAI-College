from fastapi import FastAPI
from pydantic import BaseModel
from rag_pipeline import get_answer
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    query: str

@app.get("/")
async def root():
    return {"status": "running"}

@app.post("/ask")
def ask(query: Query):
    response = get_answer(query.query)
    return {"response": response}

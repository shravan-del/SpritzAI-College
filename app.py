from fastapi import FastAPI, Request
from rag_pipeline import get_answer

app = FastAPI()

@app.get("/")
def health():
    return {"status": "running"}

@app.post("/ask")
async def ask_question(request: Request):
    body = await request.json()
    question = body.get("question")
    answer = get_answer(question)
    return {"question": question, "answer": answer}
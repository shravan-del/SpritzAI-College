from rag_pipeline import get_answer
import json

with open("evaluation_set.json", "r") as f:
    eval_set = json.load(f)

results = []

for item in eval_set:
    question = item["question"]
    expected_keywords = item["expected_keywords"]
    
    response = get_answer(question)
    answer = response["answer"].lower() if isinstance(response, dict) else str(response).lower()
    
    matched_keywords = [kw for kw in expected_keywords if kw.lower() in answer]
    accuracy_score = round((len(matched_keywords) / len(expected_keywords)) * 100, 2) if expected_keywords else 0.0

    results.append({
        "question": question,
        "answer": answer,
        "expected_keywords": expected_keywords,
        "matched_keywords": matched_keywords,
        "accuracy_score": accuracy_score
    })

with open("evaluation_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("✅ Evaluation complete and saved to evaluation_results.json")

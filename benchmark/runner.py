import json
import os
import re
import pandas as pd
from benchmark.base_dataset import ImageQADataSet
from benchmark.evaluator import evaluate_predictions
from models.unified_api import query_model, build_judge

model_name = "gemini" # "gpt-4o"  # Change to your desired model
data_path = "" # "path/to/your/dataset.json"  # Path to your dataset file
force_eval = False # True  # Set to True to force re-evaluation even if results exist

print(f"Using model: {model_name}")

os.makedirs("results_cn_mcq", exist_ok=True)
predict_cache_path = f"results_cn_mcq/{model_name}_pred_cache.json"
eval_cache_path = f"results_cn_mcq/{model_name}_eval_cache.json"
out_path = f"results_cn_mcq/{model_name}_results.json"
summary_path = "results_cn_mcq/summary.json"

dataset = ImageQADataSet(data_path)
samples = [dataset.build_sample(x) for x in dataset.data]
print(f"Total samples built: {len(samples)}")

if os.path.exists(predict_cache_path):
    with open(predict_cache_path, "r", encoding="utf-8") as f:
        pred_cache = json.load(f)
    print(f"Prediction cache loaded: {len(pred_cache)} entries")
else:
    pred_cache = {}

predictions = []
print("Running model inference...")

for i, sample in enumerate(samples):
    sid = str(sample["id"])
    if sid in pred_cache:
        pred = pred_cache[sid]
    else:
        try:
            pred = query_model(model_name, prompt=sample["prompt"], image_path=sample["image"])
        except Exception as e:
            pred = f"[ERROR] {str(e)}"
        pred_cache[sid] = pred
        with open(predict_cache_path, "w", encoding="utf-8") as f:
            json.dump(pred_cache, f, indent=2, ensure_ascii=False)

    predictions.append(pred)

    if (i + 1) % 10 == 0 or (i + 1) == len(samples):
        print(f"Progress: {i + 1}/{len(samples)} ({(i + 1)/len(samples):.1%})")

# Build judge model
judge_model = build_judge(model="gpt-4o")

# Evaluate predictions
if not force_eval and os.path.exists(out_path):
    print(f"\nEvaluation result already exists, skipping: {out_path}")
    with open(out_path, "r", encoding="utf-8") as f:
        result_data = json.load(f)
    eval_result = {
        "results": result_data,
        "overall_acc": 0.0,
        "mcq_acc": None,
        "vqa_acc": None,
        "by_difficulty": {},
        "by_subject": {}
    }
else:
    print("\nEvaluating predictions...")
    eval_result = evaluate_predictions(
        samples,
        predictions,
        judge_model=judge_model,
        cache_path=eval_cache_path
    )

# Print summary
print(f"\nOverall accuracy: {eval_result['overall_acc']:.2f}%")
if eval_result.get("mcq_acc") is not None:
    print(f"MCQ accuracy: {eval_result['mcq_acc']:.2f}%")
if eval_result.get("vqa_acc") is not None:
    print(f"VQA accuracy: {eval_result['vqa_acc']:.2f}%")

print("\nAccuracy by difficulty:")
for diff, score in sorted(eval_result["by_difficulty"].items()):
    print(f" - Difficulty {diff}: {score:.2f}%")

print("\nAccuracy by subject:")
for subject, score in sorted(eval_result["by_subject"].items()):
    print(f" - {subject}: {score:.2f}%")

# Save detailed results
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(eval_result["results"], f, indent=2, ensure_ascii=False)
print(f"\nPer-sample results saved to: {out_path}")

# Save summary
if os.path.exists(summary_path):
    with open(summary_path, "r", encoding="utf-8") as f:
        summary_data = json.load(f)
else:
    summary_data = {}

summary_data[model_name] = {
    "overall_accuracy": round(eval_result["overall_acc"] / 100, 4),
    "accuracy_by_difficulty": {str(k): round(v / 100, 4) for k, v in eval_result["by_difficulty"].items()},
    "accuracy_by_subject": {str(k): round(v / 100, 4) for k, v in eval_result["by_subject"].items()}
}

with open(summary_path, "w", encoding="utf-8") as f:
    json.dump(summary_data, f, indent=2, ensure_ascii=False)
print(f"Summary file updated: {summary_path}")

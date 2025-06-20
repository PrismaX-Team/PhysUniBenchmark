import re
import os
import json
from collections import defaultdict
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from benchmark.vqa_evaluator import evaluate_single_vqa


def extract_mcq_answer(pred):
    match = re.search(r"\b([A-D])\b", pred.upper())
    return match.group(1) if match else None


def evaluate_predictions(samples, predictions, judge_model=None, cache_path=None):
    """
    Evaluation function supporting both MCQ and VQA types.
    Supports concurrent VQA evaluation with optional cache loading/saving.

    :param samples: List of input samples
    :param predictions: Corresponding model predictions
    :param judge_model: Optional LLM for equivalence judgment (used for VQA)
    :param cache_path: Optional path to cache file for VQA results
    """
    assert len(samples) == len(predictions)

    for i, sample in enumerate(samples):
        sample["prediction"] = predictions[i]

    # Load cached VQA results if available
    cached_vqa_results = {}
    if cache_path and os.path.exists(cache_path):
        with open(cache_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    item = json.loads(line)
                    cached_vqa_results[item["id"]] = item
                except Exception:
                    continue
        print(f"📂 Loaded cached VQA evaluation results: {len(cached_vqa_results)}")

    # Split samples by type
    mcq_samples = [s for s in samples if s.get("type") == "mcq"]
    vqa_samples = [s for s in samples if s.get("type") == "vqa"]

    result_mcq = []
    correct_mcq = 0
    result_vqa = []
    correct_vqa = 0
    by_difficulty = defaultdict(list)
    by_subject = defaultdict(list)

    # Evaluate MCQs
    for sample in mcq_samples:
        pred_letter = extract_mcq_answer(sample["prediction"])
        gt = sample["answer"]
        is_correct = (pred_letter == gt)

        result = {
            "id": sample["id"],
            "gt": gt,
            "pred": pred_letter,
            "correct": is_correct,
            "difficulty": sample["difficulty"],
            "subject": sample["subject"],
            "type": "mcq"
        }
        result_mcq.append(result)

        by_difficulty[sample["difficulty"]].append(is_correct)
        by_subject[sample["subject"]].append(is_correct)
        if is_correct:
            correct_mcq += 1

    # Concurrent VQA evaluation
    print("⚙️ Starting VQA evaluation with concurrency...")
    cached_ids = set(cached_vqa_results.keys())
    to_eval_samples = [s for s in vqa_samples if s["id"] not in cached_ids]
    print(f"📌 New samples to evaluate: {len(to_eval_samples)}, cached: {len(cached_ids)}")

    cache_file = open(cache_path, "a", encoding="utf-8") if cache_path else None

    def safe_evaluate(sample):
        try:
            result = evaluate_single_vqa(sample, judge_model)
            if cache_file:
                cache_file.write(json.dumps(result, ensure_ascii=False) + "\n")
            return result
        except Exception as e:
            return {
                "id": sample["id"],
                "gt": "",
                "pred": "",
                "correct": False,
                "difficulty": sample["difficulty"],
                "subject": sample["subject"],
                "type": "vqa",
                "log": f"[ERROR] {str(e)}"
            }

    # Parallel execution
    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_sample = {executor.submit(safe_evaluate, s): s for s in to_eval_samples}

        for future in tqdm(as_completed(future_to_sample), total=len(future_to_sample), desc="Evaluating VQA"):
            sample = future_to_sample[future]
            result = future.result()
            result_vqa.append(result)
            by_difficulty[result["difficulty"]].append(result["correct"])
            by_subject[result["subject"]].append(result["correct"])
            if result["correct"]:
                correct_vqa += 1

    # Append cached VQA results
    for result in cached_vqa_results.values():
        result_vqa.append(result)
        by_difficulty[result["difficulty"]].append(result["correct"])
        by_subject[result["subject"]].append(result["correct"])
        if result["correct"]:
            correct_vqa += 1

    if cache_file:
        cache_file.close()

    # Final metrics
    total = len(samples)
    total_correct = correct_mcq + correct_vqa

    return {
        "overall_acc": round(total_correct / total * 100, 2),
        "mcq_acc": round(correct_mcq / len(mcq_samples) * 100, 2) if mcq_samples else None,
        "vqa_acc": round(correct_vqa / len(vqa_samples) * 100, 2) if vqa_samples else None,
        "by_difficulty": {k: round(sum(v) / len(v) * 100, 2) for k, v in by_difficulty.items()},
        "by_subject": {k: round(sum(v) / len(v) * 100, 2) for k, v in by_subject.items()},
        "results": result_mcq + result_vqa
    }

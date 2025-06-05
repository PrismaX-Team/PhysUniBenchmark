import re
from collections import defaultdict

def extract_choice(text):
    """从模型输出中提取 A/B/C/D 字母"""
    match = re.search(r"\b([A-D])\b", text.upper())
    return match.group(1) if match else None

def evaluate(samples, predictions):
    correct = 0
    total = len(samples)
    results = []

    # 记录不同难度等级的正确/总数
    difficulty_stats = defaultdict(lambda: {"correct": 0, "total": 0})

    for sample, pred in zip(samples, predictions):
        pred_choice = extract_choice(pred)
        gt = sample["correct_choice"].strip().upper()
        hit = pred_choice == gt
        difficulty = sample.get("meta_data", {}).get("difficulty", "unknown")

        results.append({
            "id": sample["id"],
            "difficulty": difficulty,
            "prediction": pred,
            "predicted_choice": pred_choice,
            "correct_choice": gt,
            "hit": hit
        })

        
        if hit:
            correct += 1

        
        difficulty_stats[difficulty]["total"] += 1
        if hit:
            difficulty_stats[difficulty]["correct"] += 1

    # 总体准确率
    overall_acc = correct / total if total > 0 else 0.0

    # 每个 difficulty 的准确率
    per_difficulty_acc = {
        k: round(v["correct"] / v["total"], 4) if v["total"] > 0 else 0.0
        for k, v in difficulty_stats.items()
    }

    return overall_acc, per_difficulty_acc, results

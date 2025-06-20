from benchmark.physic_eval_utils import extract_final_answer_allform, is_equiv

def evaluate_single_vqa(sample, judge_model=None):
    """
    对单个 VQA 样本进行评估（返回结果 dict，包括正确性与日志）
    """
    pred_text = sample["prediction"]
    gt = sample["answer"].strip()
    sample_id = sample["id"]

    boxed_preds = extract_final_answer_allform(pred_text)
    flat_preds = [x.strip() for group in boxed_preds for x in (group if isinstance(group, list) else [group])]

    is_correct = False
    log = ""

    if gt in flat_preds:
        is_correct = True
        log = "Exact match in boxed prediction."
    else:
        for p in flat_preds:
            try:
                eq_res = is_equiv(judge_model, p, gt)
                log = eq_res.get("LOG", "") or eq_res.get("error", "")
                if eq_res.get("final_result"):
                    is_correct = True
                    break
            except Exception as e:
                log = f"Judge model error: {e}"
                is_correct = False

    return {
        "id": sample_id,
        "gt": gt,
        "pred": flat_preds,
        "correct": is_correct,
        "difficulty": sample["difficulty"],
        "subject": sample["subject"],
        "type": "vqa",
        "log": log
    }

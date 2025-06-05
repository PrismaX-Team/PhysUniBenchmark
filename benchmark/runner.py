import json
import os
from benchmark.base_dataset import ImageMCQDataset
from benchmark.evaluator import evaluate
from models.unified_api import query_model


model_name = "gpt-4o" 
print(f"使用模型: {model_name}")


dataset = ImageMCQDataset(
    data_path="/fs-computility/ai4sData/shared/physics/instruction_data/multi_modal_benchmark/v1/PhysicsProblemEncyclopedia-SFT_TextImage/v1.2/physics_physicsproblemencyclopedia_num2801_20250512_MCQ.json"
)
samples = [dataset.build_sample(x) for x in dataset.data]
print(f"构造样本数: {len(samples)}")


predictions = []
print("正在调用模型进行预测...")

for i, sample in enumerate(samples):
    try:
        pred = query_model(model_name, prompt=sample["prompt"], image_path=sample["image"])
    except Exception as e:
        pred = f"[ERROR] {str(e)}"
    predictions.append(pred)

    if i < 2:
        print("\n" + "="*60)
        print(f"样例 {i+1}")
        print(f"图像路径: {sample['image']}")
        print(f"Prompt:\n{sample['prompt']}")
        print(f"模型回答: {pred}")
        print("="*60)

   
    if (i + 1) % 10 == 0 or (i + 1) == len(samples):
        print(f"完成 {i + 1} / {len(samples)} 道题 ({(i + 1) / len(samples):.1%})")

print("模型预测完成，正在评估准确率...")


acc, difficulty_acc, results = evaluate(samples, predictions)
print(f"模型整体准确率：{acc:.2%}")


for diff, score in sorted(difficulty_acc.items(), key=lambda x: str(x[0])):
    print(f"难度 {diff}: {score:.2%} 准确率")


os.makedirs("results", exist_ok=True)
out_path = f"results/{model_name}_results.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print(f"预测结果已保存至：{out_path}")


summary_path = "results/summary.json"


if os.path.exists(summary_path):
    with open(summary_path, "r", encoding="utf-8") as f:
        summary_data = json.load(f)
else:
    summary_data = {}


summary_data[model_name] = {
    "overall_accuracy": round(acc, 4),
    "accuracy_by_difficulty": {str(k): round(v, 4) for k, v in difficulty_acc.items()}
}


with open(summary_path, "w", encoding="utf-8") as f:
    json.dump(summary_data, f, indent=2, ensure_ascii=False)
print(f"已更新：{summary_path}")

import json
import os
import re


class ImageQADataSet:
    def __init__(self, data_path):
        self.data_path = data_path
        self.root_dir = os.path.dirname(data_path)
        self.data = self.load_data()

        fname = os.path.basename(data_path).lower()
        if "_mcq" in fname:
            self.task_type = "mcq"
        elif "_qa" in fname:
            self.task_type = "vqa"
        else:
            raise ValueError(f"Cannot infer task type from filename: {data_path}")

        self.dataset_type = "shym" if "shym" in fname else "classic"

    def load_data(self):
        with open(self.data_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def resolve_image_path(self, rel_path):
        return os.path.abspath(os.path.join(self.root_dir, rel_path))

    def extract_options(self, mcq_str):
        lines = mcq_str.strip().split('\n')
        return {
            line[0]: line[3:].strip()
            for line in lines if re.match(r"^[A-D]\.\s", line)
        }

    def build_sample(self, sample):
        image_path = None
        if sample.get("images"):
            image_path = self.resolve_image_path(sample["images"][0])

        meta = sample.get("meta_data", {})
        if self.dataset_type == "classic":
            difficulty = meta.get("difficulty", "unknown")
            source = meta.get("source", "unknown")
            subject = "unknown"
            if isinstance(source, str) and "-" in source:
                parts = source.split("-")
                if len(parts) >= 2:
                    subject = parts[1].strip()
        else:
            difficulty = meta.get("difficulty", "unknown")
            subject = meta.get("subtopic", "unknown")
            source = "shym"

        conversations = sample.get("conversations", [])
        if not conversations or not isinstance(conversations, list):
            raise ValueError(f"Sample ID {sample['id']} is missing valid 'conversations' field.")

        question = conversations[0]["content"].replace('<image>', '[Image]')

        if self.task_type == "mcq":
            options = self.extract_options(sample.get("MCQ", ""))
            options_prompt = '\n'.join([f"{k}. {v}" for k, v in options.items()])
            prompt = (
                "You are a helpful assistant. Based on the following question and options, "
                "choose the most appropriate answer. The image is provided separately.\n\n"
                f"Question: {question}\n\n"
                f"Options:\n{options_prompt}\n\n"
                "Please respond with only the letter of the correct answer (A, B, C, or D)."
            )
            correct = sample.get("correct_choice", "").strip().upper()

        else:  # VQA
            prompt = (
                "You are a physics expert assistant. Solve the following question step-by-step.\n\n"
                "At the VERY END of your answer, output ONLY the FINAL ANSWER in this format:\n\n"
                "\\[\n\\boxed{{your_final_answer_here}}\n\\]\n\n"
                "You MUST put the final answer in the `\\boxed{}` environment.\n"
                "This applies even if the answer is a text explanation like \"The singlet state is lower in energy.\"\n"
                "Do NOT include multiple boxes.\n"
                "Do NOT include \\boxed anywhere else in your reasoning.\n"
                "The box must appear on the last line of the response.\n\n"
                f"Question: {question}\nAnswer:"
            )

            if len(conversations) < 2 or "content" not in conversations[1]:
                raise ValueError(f"Sample ID {sample['id']} is missing a valid GPT answer.")
            correct = conversations[1]["content"].strip()

        return {
            "id": sample["id"],
            "prompt": prompt,
            "image": image_path,
            "answer": correct,
            "difficulty": str(difficulty),
            "subject": subject,
            "source": source,
            "type": self.task_type
        }

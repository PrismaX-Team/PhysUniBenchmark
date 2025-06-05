import json
import re
import os

class ImageMCQDataset:
    def __init__(self, data_path):
        self.data_path = data_path
        self.root_dir = os.path.dirname(data_path)  
        self.data = self.load_data()

    def load_data(self):
        """Load the dataset from a JSON file."""
        with open(self.data_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def resolve_image_path(self, rel_path):
        """将 images/xxx.jpg 相对路径转换为绝对路径"""
        return os.path.abspath(os.path.join(self.root_dir, rel_path))

    def build_sample(self, sample):
        """
        构建一个包含图像路径和 Prompt 的输入，供模型推理使用。

        返回：
            {
                "id": 19,
                "prompt": "你构造的图文 prompt",
                "image": "/fs-computility/.../images/xxx.jpg",  # 如果有图
                "correct_choice": "A"
            }
        """
        
        question = sample['conversations'][0]['content'].replace('<image>', '[Image]')

       
        options_raw = sample['MCQ'].strip().split('\n')
        options = {
            opt[0]: opt[3:].strip()
            for opt in options_raw
            if re.match(r'^[A-D]\.\s', opt)
        }
        options_prompt = '\n'.join([f"{key}. {value}" for key, value in options.items()])

        prompt = (
            "You are a helpful assistant. Based on the following question and options, "
            "choose the most appropriate answer. The image is provided separately.\n\n"
            f"Question: {question}\n\n"
            f"Options:\n{options_prompt}\n\n"
            "Please respond with only the letter of the correct answer (A, B, C, or D)."
        )

        
        if sample.get("images"):
            image_path = self.resolve_image_path(sample["images"][0])
        else:
            image_path = None

        return {
            "id": sample["id"],
            "prompt": prompt,
            "image": image_path,
            "correct_choice": sample["correct_choice"].strip().upper()
        }

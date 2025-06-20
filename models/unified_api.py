import os
import requests
import base64
import mimetypes
from dotenv import load_dotenv

load_dotenv()

# Model configuration using environment variables for API keys
MODEL_MAP = {
    "gpt-4o": {
        "model": "gpt-4o",
        "api_key": os.getenv("API_KEY_GPT4O")
    },
    "claude": {
        "model": "anthropic/claude-3.5-sonnet",
        "api_key": os.getenv("API_KEY_CLAUDE")
    },
    "qwen": {
        "model": "Qwen/Qwen2.5-VL-72B-Instruct",
        "api_key": os.getenv("API_KEY_QWEN")
    },
    "grok": {
        "model": "grok-3",
        "api_key": os.getenv("API_KEY_GROK")
    },
    "gemini": {
        "model": "gemini-2.5-pro-preview-03-25",
        "api_key": os.getenv("API_KEY_GEMINI")
    },
    "gpt-4o-mini": {
        "model": "gpt-4o-mini",
        "api_key": os.getenv("API_KEY_GPT4O_MINI")
    },
    "gpt-o4mini": {
        "model": "o4-mini",
        "api_key": os.getenv("API_KEY_GPT_O4MINI")
    }
}

# API gateway endpoint
API_URL = ""


def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as f:
            image_data = f.read()
            mime_type, _ = mimetypes.guess_type(image_path)
            mime_type = mime_type or "image/png"
            base64_str = base64.b64encode(image_data).decode("utf-8")
            return f"data:{mime_type};base64,{base64_str}"
    except Exception as e:
        print(f"[ERROR] Failed to encode image: {image_path}, reason: {str(e)}")
        return None


def query_model(model_name, prompt, image_path=None):
    if model_name not in MODEL_MAP:
        raise ValueError(f"Unknown model name: {model_name}")

    model_info = MODEL_MAP[model_name]
    api_key = model_info["api_key"]
    if not api_key:
        raise EnvironmentError(f"Missing API key for model: {model_name}")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    messages = []

    if image_path:
        image_base64 = encode_image_to_base64(image_path)
        if image_base64:
            messages.append({
                "type": "image_url",
                "image_url": {
                    "url": image_base64
                }
            })

    messages.append({
        "type": "text",
        "text": prompt
    })

    payload = {
        "model": model_info["model"],
        "messages": [{"role": "user", "content": messages}],
        "temperature": 0
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"[ERROR {response.status_code}] {response.text}"


class DummyJudgeModel:
    def __init__(self, model_name):
        self.model_name = model_name
        self.sys_prompt = ""

    def generate(self, prompt):
        return query_model(self.model_name, prompt=prompt)

    def working(self):
        try:
            out = self.generate("Say 'test'.")
            return isinstance(out, str) and "test" in out.lower()
        except Exception:
            return False


def build_judge(model="gpt-4o", **kwargs):
    return DummyJudgeModel(model)

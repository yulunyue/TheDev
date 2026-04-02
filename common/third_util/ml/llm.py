"""
irm https://ollama.com/install.ps1 | iex
ollama pull qwen2.5:1.5b
ollama run qwen2.5:1.5b
"""

from transformers import AutoModelForCausalLM, AutoTokenizer
import json

model_name = "Qwen/Qwen2.5-1.5B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name, torch_dtype="auto", device_map="auto"
)


def natural_language_to_json(text):
    # 设计清晰的系统提示词，要求只输出 JSON
    messages = [
        {
            "role": "system",
            "content": "你是一个将自然语言转换为 JSON 的助手。只输出有效的 JSON，不要包含其他文字。",
        },
        {"role": "user", "content": f"请将以下内容转换为 JSON：\n{text}"},
    ]
    # 应用聊天模板
    prompt = tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(
        **inputs,
        max_new_tokens=256,
        temperature=0.1,  # 低温度使输出更确定
        do_sample=False,  # 贪婪解码，保证格式稳定
    )
    response = tokenizer.decode(
        outputs[0][inputs.input_ids.shape[1] :], skip_special_tokens=True
    )

    # 尝试解析 JSON
    try:
        return json.loads(response.strip())
    except json.JSONDecodeError:
        return {"error": "无效 JSON", "raw": response}


# 测试
result = natural_language_to_json("明天下午3点在北京开会，需要准备投影仪和笔记本电脑")
print(json.dumps(result, ensure_ascii=False, indent=2))

# -*- coding: utf-8 -*-
import json
import hashlib
from pathlib import Path
from openai import OpenAI
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

# 初始化 LLM 客户端（以 DeepSeek 为例）
client = OpenAI(
    api_key="sk-6c091a32c2d34f869a20620222c0abde",
    base_url="https://api.deepseek.com/v1"
)

# 提示词模板
PROMPT_TEMPLATE = """
请你对以下中文回答进行清洗：
1. 删除冗余表达、语气词、套话、重复内容；
2. 删除所有“题主你好”、“我是XXX”等问候语和自我介绍；
3. 将内容控制在800字以内，尽量保留有效观点、逻辑与情感支持。
4. 主要保留的内容是共情的语言语句和情感支持的内容。
5. 删除所有的“谢谢你的邀请”、“感谢你的分享”等感谢语；

原始回答如下：
---
{answer}
---
清洗后的结果：
"""

# 缓存字典（防止重复调用）
cache = {}

def get_cache_key(text):
    return hashlib.md5(text.encode("utf-8")).hexdigest()

# 封装调用函数 + 缓存
def clean_with_gpt_cached(answer: str) -> str:
    key = get_cache_key(answer)
    if key in cache:
        return cache[key]

    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个擅长语言精简和心理支持的写作助手。"},
                {"role": "user", "content": PROMPT_TEMPLATE.format(answer=answer)}
            ],
            temperature=0.4,
            max_tokens=1024
        )
        cleaned = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"调用出错: {e}")
        cleaned = ""

    cache[key] = cleaned
    return cleaned

# 多线程并发清洗单个 JSON 文件
def clean_json_file_parallel(input_path: Path, output_path: Path, max_workers: int = 5):
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    answers = data.get("answers", [])
    cleaned_answers = [None] * len(answers)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_idx = {
            executor.submit(clean_with_gpt_cached, ans["answer"]): idx
            for idx, ans in enumerate(answers)
        }

        for future in tqdm(as_completed(future_to_idx), total=len(answers), desc=f"清洗 {input_path.name}", unit="条"):
            idx = future_to_idx[future]
            ans = answers[idx]
            try:
                cleaned_text = future.result()
            except Exception as e:
                print(f"第 {idx} 条清洗失败: {e}")
                cleaned_text = ""

            cleaned_answers[idx] = {
                "user": ans.get("user", ""),
                "votes": ans.get("votes", 0),
                "cleaned_answer": cleaned_text,
                "original_length": len(ans["answer"]),
                "cleaned_length": len(cleaned_text),
                "reduced_chars": len(ans["answer"]) - len(cleaned_text)
            }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_answers, f, ensure_ascii=False, indent=2)

# 批量清洗整个文件夹
def batch_clean_folder(input_dir, output_dir, max_workers=5):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    json_files = list(input_dir.glob("*.json"))
    print(f"共发现 {len(json_files)} 个 JSON 文件，开始处理...\n")

    for input_file in tqdm(json_files, desc="整体进度", unit="文件"):
        output_file = output_dir / input_file.name
        clean_json_file_parallel(input_file, output_file, max_workers=max_workers)

    print("\n✅ 所有文件处理完毕！")

# 主入口
if __name__ == "__main__":
    input_folder = "/Users/gongshengxiao/Desktop/yixinli150/jiaolvclean"
    output_folder = "/Users/gongshengxiao/Desktop/yixinli150/jiaolv123"
    batch_clean_folder(input_folder, output_folder, max_workers=5)  # 可调整并发数量
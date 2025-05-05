import json
import re
from pathlib import Path

def clean_text(text):
    # 删除 emoji（匹配表情符号范围）
    text = re.sub(r'[\U00010000-\U0010ffff]', '', text)
    # 删除破折号（全角、半角）
    text = re.sub(r'[—–-]', '', text)
    # 删除序号符号 ①②③④⑤⑥⑦⑧⑨⑩
    text = re.sub(r'[①②③④⑤⑥⑦⑧⑨⑩]', '', text)
    # 删除换行符
    text = text.replace('\n', ' ').replace('\r', ' ')
    # 合并多余空格
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else -1

def process_folder(input_folder, output_file):
    input_path = Path(input_folder)
    all_results = []

    json_files = sorted(input_path.glob("*.json"), key=lambda x: extract_number(x.name))
    print(f"找到 {len(json_files)} 个文件")

    for json_file in json_files:
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            question = data.get("question", {})
            title = clean_text(question.get("title", ""))
            content = clean_text(question.get("content", ""))

            all_results.append({
                "file": json_file.name,
                "title": title,
                "content": content
            })

        except Exception as e:
            print(f"读取 {json_file.name} 出错: {e}")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print(f"已完成，保存到 {output_file}")

if __name__ == "__main__":
    input_folder = "/Users/gongshengxiao/Desktop/yixinli150/yuerclean"  # ← 替换为你的文件夹路径
    output_file = "/Users/gongshengxiao/Desktop/yixinli150/yuer_question.json"  # ← 替换为你的输出文件路径

    process_folder(input_folder, output_file)
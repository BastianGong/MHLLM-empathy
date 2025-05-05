import json
import re

def clean_text(text):
    text = re.sub(r'[\U00010000-\U0010ffff]', '', text)
    text = re.sub(r'[—–-]', '', text)
    text = re.sub(r'[①②③④⑤⑥⑦⑧⑨⑩]', '', text)
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def process_file(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    cleaned_data = []
    for item in data:
        cleaned_item = {
            "file": item.get("file", ""),
            "title": clean_text(item.get("title", "")),
            "content": clean_text(item.get("content", ""))
        }
        cleaned_data.append(cleaned_item)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

    print(f"清理完成，已保存到 {output_path}")

if __name__ == "__main__":
    input_file = "/Users/gongshengxiao/Desktop/yixinli150/renjiguanxiqueation.json"   
    output_file = "//Users/gongshengxiao/Desktop/yixinli150/renjiguanxiquestion_clean.json"  
    process_file(input_file, output_file)
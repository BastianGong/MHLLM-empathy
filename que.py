import json
from pathlib import Path

def collect_questions(input_folder, output_file):
    input_path = Path(input_folder)
    all_results = []


    json_files = sorted(input_path.glob("*.json"), key=lambda x: x.name)
    print(f"numbers: {len(json_files)} ")

    for json_file in json_files:
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)


            title = data.get("question", {}).get("title", "")
            content = data.get("question", {}).get("content", "")

            all_results.append({
                "file": json_file.name,
                "title": title,
                "content": content
            })

        except Exception as e:
            print(f"error {json_file.name} : {e}")


    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print(f"save as {output_file}")

if __name__ == "__main__":
    input_folder = "/Users/gongshengxiao/Desktop/yixinli150/yiyuclean"
    output_file = "/Users/gongshengxiao/Desktop/yixinli150/yiyuqueation.json"

    collect_questions(input_folder, output_file)
import json

with open("books_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(json.dumps(data, indent=4, ensure_ascii=False))

import os
import re
import json

DATA_DIR = "data"
OUTPUT_FILE = "cleaned_medical_texts.json"

def remove_html_tags(text: str) -> str:
    """Remove HTML tags like <B> and </B>"""
    return re.sub(r"<[^>]+>", "", text)

def normalize_whitespace(text: str) -> str:
    """Convert multi-line text into a single clean line"""
    text = text.replace("\n", " ").replace("\r", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def process_files(data_dir: str):
    result = {}
    start = 0

    for filename in os.listdir(data_dir):
        start += 1
        if filename.endswith(".txt"):
            file_path = os.path.join(data_dir, filename)

            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                raw_text = f.read()

            cleaned = remove_html_tags(raw_text)
            cleaned = normalize_whitespace(cleaned)

            result[filename] = cleaned
    print(f"Processed {start} files.")
    return result

if __name__ == "__main__":
    cleaned_data = process_files(DATA_DIR)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

    print(f"Processed {len(cleaned_data)} files → saved to {OUTPUT_FILE}")

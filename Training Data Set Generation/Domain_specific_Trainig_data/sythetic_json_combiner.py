import json
from pathlib import Path
from tqdm import tqdm


## THIS WAS USE TO COMBINE THE GENERATED DATASETS INTO ONE FILE ##




folders = [
    Path("training_data_jebs_synthetic"),
    Path("training_data_jebs_synthetic")  # change if second folder name differs
]

all_pairs = []

# Collect all json files
json_files = []
for folder in folders:
    json_files.extend(folder.glob("*.json"))

# Read and combine
for file in tqdm(json_files, desc="Processing JSON files"):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

        if isinstance(data, list):
            all_pairs.extend(data)
        elif isinstance(data, dict):
            all_pairs.append(data)
        else:
            raise ValueError(f"Unsupported JSON format in {file}")

# Count total pairs
total_pairs = len(all_pairs)

# Output file name
output_file = f"training_data_{total_pairs}.json"

# Save combined data
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_pairs, f, indent=2, ensure_ascii=False)

print(f"\n✅ Combined {total_pairs} pairs")
print(f"📁 Saved to {output_file}")

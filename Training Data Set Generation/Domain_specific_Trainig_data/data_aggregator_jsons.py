import json
import csv
import os

def aggregate_jsons(json_files):
    aggregated = []

    # Load and aggregate
    for path in json_files:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

            if not isinstance(data, list):
                raise ValueError(f"{path} is not a list of records")

            for item in data:
                if "medical" in item and "layman" in item:
                    aggregated.append({
                        "medical": str(item["medical"]),
                        "layman": str(item["layman"])
                    })

    total_rows = len(aggregated)

    # Output filenames
    json_out = f"training_data_{total_rows}.json"
    csv_out = f"training_data_{total_rows}.csv"

    # Save JSON
    with open(json_out, "w", encoding="utf-8") as f:
        json.dump(aggregated, f, ensure_ascii=False, indent=2)

    # Save CSV
    with open(csv_out, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["medical", "layman"])
        writer.writeheader()
        writer.writerows(aggregated)

    print(f"Saved {json_out}")
    print(f"Saved {csv_out}")
    print(f"Total rows aggregated: {total_rows}")


# ---------------- USAGE ----------------
if __name__ == "__main__":
    aggregate_jsons([
        "training_data_2248.json",
        "cochrane_simplification_full.json",
        "cbasu_Med-EASi.json"
    ])

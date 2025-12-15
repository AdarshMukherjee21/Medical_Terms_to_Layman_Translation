import pandas as pd
import json
import os

def csv_to_med_layman_json(
    csv_path: str,
    medical_col: str,
    layman_col: str
):
    # Load CSV
    df = pd.read_csv(csv_path)

    # Sanity check
    if medical_col not in df.columns:
        raise ValueError(f"Column '{medical_col}' not found in CSV")
    if layman_col not in df.columns:
        raise ValueError(f"Column '{layman_col}' not found in CSV")

    # Build JSON list
    data = []
    for _, row in df.iterrows():
        data.append({
            "medical": str(row[medical_col]),
            "layman": str(row[layman_col])
        })

    # Output path (same name as CSV)
    base_name = os.path.splitext(csv_path)[0]
    output_path = base_name + ".json"

    # Save JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(data)} rows to {output_path}")


# ---------------- USAGE ----------------
if __name__ == "__main__":
    csv_to_med_layman_json(
        csv_path="cochrane_simplification_full.csv",
        medical_col="source",
        layman_col="target"
    )

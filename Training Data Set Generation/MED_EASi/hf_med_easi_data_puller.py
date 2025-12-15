from datasets import load_dataset
import pandas as pd

print("Starting HF data puller...")

# Load dataset (GEM uses custom loader)
dataset = load_dataset(
    "cbasu/Med-EASi",
    trust_remote_code=True
)

print(dataset)

# Choose split
split = "train"   # or "validation", "test"

# Convert entire split to pandas
df = dataset[split].to_pandas()

# Save EVERYTHING to CSV
output_path = "cbasu_Med-EASi.csv"
df.to_csv(output_path, index=False)

print(f"Saved {len(df)} rows to {output_path}")
print("Columns:", list(df.columns))

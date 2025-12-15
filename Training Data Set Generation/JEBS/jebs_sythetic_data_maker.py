import os
import json
import time
import traceback
from tqdm import tqdm
import ollama
from datetime import datetime

# ----------------------------
# CONFIG
# ----------------------------
INPUT_JSON = "jebs_data.json"
OUTPUT_DIR = "training_data_jebs_synthetic"
FAILED_LOG = "FAILED_LOG.json"

MODEL_NAME = "gpt-oss:20b-cloud"
PRINT_EVERY = 20

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ----------------------------
# OLLAMA FUNCTION
# ----------------------------
def generate_pair(med: str, simp: str) -> dict:
    prompt = f"""
You are a medical language simplification system.

Task:
Given a medical term and a hint, generate TWO things:

1. A short medical-style sentence that naturally uses the medical term.
2. A layman-friendly simplified version of that sentence.

Rules:
- Keep the meaning accurate
- Do NOT add medical advice
- Do NOT add new facts
- Medical sentence should sound clinical
- Layman sentence should use plain everyday English
- Layman sentence should NOT repeat medical jargon
- Keep both concise (1–2 sentences each)

Output FORMAT (JSON ONLY):
{{
  "medical": "<medical sentence>",
  "layman": "<layman sentence>"
}}

Medical term:
{med}

Hint (for context only):
{simp}
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You generate paired medical and layman text accurately."},
            {"role": "user", "content": prompt}
        ],
        options={
            "temperature": 0.3,
            "top_p": 0.9,
            "num_ctx": 4096
        }
    )

    raw = response["message"]["content"].strip()

    # Parse JSON safely
    return json.loads(raw)



# ----------------------------
# MAIN PIPELINE
# ----------------------------
def main():
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    last_index = 714 # start with 0 or last failed index 
    print(f"[RESUME] Last completed sample: {last_index}")

    failures = []

    for idx, item in enumerate(
        tqdm(data, desc="Generating JEBS-style synthetic data"),
        start=1
    ):
        if idx <= last_index:
            continue

        med = item.get("med", "").strip()
        simp = item.get("simp", "").strip()

        output_path = os.path.join(
            OUTPUT_DIR, f"sample_{idx:05d}.json"
        )

        try:
            pair = generate_pair(med, simp)

            if "medical" not in pair or "layman" not in pair:
                raise ValueError("Invalid model output format")

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(pair, f, ensure_ascii=False, indent=2)

            if idx % PRINT_EVERY == 0:
                print(f"[OK] Processed {idx} samples")

            time.sleep(0.1)

        except Exception as e:
            print("\n[ERROR] Generation failed")
            traceback.print_exc()

            failures.append({
                "index": idx,
                "medical_term": med,
                "error": str(e)
            })

            # Append-safe failure log
            existing = []
            if os.path.exists(FAILED_LOG):
                with open(FAILED_LOG, "r", encoding="utf-8") as f:
                    existing = json.load(f)

            existing.extend(failures)

            with open(FAILED_LOG, "w", encoding="utf-8") as f:
                json.dump(existing, f, indent=2)

            print(f"[STOPPED] Failure logged to {FAILED_LOG}")
            return

    print(f"\n✅ Completed {len(data)} samples")

# ----------------------------
# ENTRY POINT
# ----------------------------
if __name__ == "__main__":
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    main()
    print(f"End time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

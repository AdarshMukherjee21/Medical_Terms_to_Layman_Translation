import os
import json
import time
import traceback
from tqdm import tqdm

# import google.generativeai as genai
import ollama

# ----------------------------
# CONFIG
# ----------------------------
INPUT_JSON = "cleaned_medical_texts.json"
OUTPUT_DIR = "training_data"
FAILED_LOG = "FAILED_LOG.json"
PRINT_EVERY = 20
MODEL_NAME = "gpt-oss:20b-cloud"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# genai.configure(api_key="AIzaSyBgs9b_qEllVzvRgSxSKKx6bRwAdCkN0VI")
# model = genai.GenerativeModel(MODEL_NAME)



def medical_to_layman(medical_text: str) -> str:
    prompt = f"""
You are a medical language simplification system.

Task:
Rewrite the following medical text into clear, simple English
for a non-medical reader.

Rules:
- Keep the same meaning
- Do NOT add medical advice
- Do NOT remove important details
- Use plain, everyday English
- Keep it roughly the same length
- Output ONLY the simplified text

Medical text:
{medical_text}
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You simplify medical language accurately."},
            {"role": "user", "content": prompt}
        ],
        options={
            "temperature": 0.25,
            "top_p": 0.9,
            "num_ctx": 8192  # important for long medical notes
        }
    )

    return response["message"]["content"].strip()

# ----------------------------
# GEMINI FUNCTION
# ----------------------------
# def medical_to_layman(medical_text: str) -> str:
#     prompt = f"""
# You are a medical language simplification system.

# Task:
# Convert the following medical text into clear, simple English
# that a non-medical person can easily understand.

# Rules:
# - Keep the same meaning
# - Do NOT add medical advice
# - Do NOT remove important information
# - Use simple words
# - Output ONLY the simplified text

# Medical Text:
# {medical_text}
# """

#     response = model.generate_content(
#         prompt,
#         generation_config={
#             "temperature": 0.3,
#             "max_output_tokens": 1024
#         }
#     )

#     return response.text.strip()

# ----------------------------
# MAIN PIPELINE
# ----------------------------
def main():
    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        medical_data = json.load(f)

    failures = []
    sample_index = 0

    for filename, medical_text in tqdm(medical_data.items(), desc="Generating synthetic data"):
        sample_index += 1
        output_path = os.path.join(
            OUTPUT_DIR, f"sample_{sample_index:05d}.json"
        )

        try:
            layman_text = medical_to_layman(medical_text)

            sample = {
                "medical": medical_text,
                "layman": layman_text
            }

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(sample, f, ensure_ascii=False, indent=2)

            if sample_index % PRINT_EVERY == 0:
                print(f"[OK] Processed {sample_index} samples")

            time.sleep(0.4)  # avoid rate limits

        except Exception as e:
            print("\n[ERROR] Generation failed")
            traceback.print_exc()

            failure_entry = {
                "index": sample_index,
                "source_file": filename,
                "error": str(e)
            }
            failures.append(failure_entry)

            with open(FAILED_LOG, "w", encoding="utf-8") as f:
                json.dump(failures, f, indent=2)

            print(f"[STOPPED] Failure saved to {FAILED_LOG}")
            return

    print(f"\n✅ Completed {sample_index} samples successfully")

if __name__ == "__main__":
    main()

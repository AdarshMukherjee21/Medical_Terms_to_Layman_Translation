import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# --- Configuration ---
MODEL_PATH = "flan_t5_base_lora_merged"
SAMPLE_INPUTS = [
    "The dermatophyte infection was confined to the cutaneous surface of the corporis.",
    "The CUP permits the use of investigational drugs not yet approved for clinical use.",
    "The patient has progressed to end‑stage renal disease, necessitating dialysis or transplantation."
]

# --- Model Loading (Cached) ---
@st.cache_resource
def load_model_and_tokenizer():
    print("Loading model...")
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_PATH,
        use_fast=False
    )
    
    # Updated 'torch_dtype' to 'dtype' to fix the warning you saw earlier
    model = AutoModelForSeq2SeqLM.from_pretrained(
        MODEL_PATH,
        dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto"
    )
    model.eval()
    return tokenizer, model

try:
    tokenizer, model = load_model_and_tokenizer()
except OSError:
    st.error(f"Could not find the model directory: '{MODEL_PATH}'. Please ensure the folder is in the same directory as this script.")
    st.stop()

# --- Inference Function ---
def simplify_medical_text(text, max_new_tokens=128):
    prompt = f"Simplify:\n {text}"
    
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    ).to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            num_beams=4,
            early_stopping=True
        )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# --- Streamlit UI ---
st.title(" Medical to Layman Translator")
st.write("Translate complex medical terms into simple, easy-to-understand language.")

# 1. Sample Inputs Selection
selected_sample = st.selectbox(
    "Try an example:", 
    options=["Custom Input"] + SAMPLE_INPUTS,
    index=0
)

# Determine what text to show in the box
default_text = ""
if selected_sample != "Custom Input":
    default_text = selected_sample

# 2. Input Area
user_input = st.text_area("Enter Medical Text:", value=default_text, height=150)

# 3. Button & Output
if st.button("Translate", type="primary"):
    if user_input.strip():
        # The loading bubble
        with st.spinner("Translating..."):
            result = simplify_medical_text(user_input)
            
        st.success("Translation Complete!")
        st.markdown(f"### Result:\n>{result}")
    else:
        st.warning("Please enter some text first.")
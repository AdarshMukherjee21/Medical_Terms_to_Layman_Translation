import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# --- Configuration ---
MODEL_PATH = "flan_t5_base_lora_merged"

# New samples specific to Clinical Trials (Scenario C)
SAMPLE_INPUTS = {
    "Study Design": "This is a multicenter, randomized, double-blind, placebo-controlled, parallel-group study to evaluate the efficacy and safety of the investigational drug.",
    "Inclusion Criteria": "Subjects must have a histological or cytological diagnosis of adenocarcinoma of the breast with measurable disease defined by RECIST v1.1.",
    "Adverse Events": "The most common treatment-emergent adverse events were pyrexia, neutropenia, and thrombocytopenia, which were managed with dose interruptions."
}

# --- Page Config ---
st.set_page_config(
    page_title="Plain Language Summarizer",
    page_icon="💊",
    layout="centered"
)

# --- Model Loading (Cached) ---
@st.cache_resource
def load_model_and_tokenizer():
    # Only verify this print once in the terminal
    print("Loading model...")
    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_PATH,
        use_fast=False
    )
    
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
    st.error(f"❌ Error: Model folder '{MODEL_PATH}' not found. Please ensure it is in the same directory.")
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

# Sidebar for "Project" context
with st.sidebar:
    st.header(" Project Details")
    st.info("Tool: Plain Language Summary Generator")
    st.text_input("Protocol Number", value="NCT04592201")
    st.selectbox("Target Audience", ["Patients", "General Public", "Caregivers"])
    st.divider()
    st.caption("Use this tool to draft lay summaries for regulatory compliance (EU CTR 536/2014).")

# Main Interface
st.title(" Clinical Trial Summarizer")
st.markdown("""
**Convert technical study protocols into patient-friendly language.** *Paste a section from your Clinical Study Report (CSR) below to generate a draft.*
""")

st.divider()

# 1. Sample Selector
selected_label = st.selectbox(
    "Load a specific section example:", 
    options=["Custom Input"] + list(SAMPLE_INPUTS.keys()),
    index=0
)

# Determine text based on selection
default_text = ""
if selected_label != "Custom Input":
    default_text = SAMPLE_INPUTS[selected_label]

# 2. Input Area
col1, col2 = st.columns(2)
with col1:
    st.markdown("#### 📄 Technical Input")
    user_input = st.text_area(
        "Paste Protocol/CSR text here:", 
        value=default_text, 
        height=200,
        label_visibility="collapsed"
    )

# 3. Action & Output
with col2:
    st.markdown("#### 🗣️ Layman Output")
    
    # Placeholder for the result
    result_container = st.empty()
    
    # Logic to run only when button is clicked OR if we want live updates (sticking to button)
    if st.button("Generate Summary", type="primary", use_container_width=True):
        if user_input.strip():
            with st.spinner("Drafting summary..."):
                simplified_text = simplify_medical_text(user_input)
            
            # Display result in a nice box
            result_container.success(simplified_text)
        else:
            result_container.warning("Waiting for input...")

# Footer / Disclaimer
st.markdown("---")
st.caption(" **Disclaimer:** This is an AI-assisted drafting tool. All summaries must be reviewed by a qualified medical professional.")
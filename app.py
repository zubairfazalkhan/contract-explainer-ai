import streamlit as st
from transformers import pipeline
import fitz  # PyMuPDF

# Must be the first Streamlit command
st.set_page_config(page_title="Contract Clause Explainer AI", layout="centered")

# Load the model
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="openai-community/gpt2", max_new_tokens=100)

generator = load_model()

# App UI
st.title("📄 Contract Clause Explainer AI")
st.markdown("Explain legal language in plain English using AI.")

# Input method
input_type = st.radio("Choose input method:", ["📄 Paste text", "📁 Upload PDF"])

text = ""

if input_type == "📄 Paste text":
    text = st.text_area("Enter contract clause:", height=200)
elif input_type == "📁 Upload PDF":
    uploaded_file = st.file_uploader("Upload a contract PDF", type=["pdf"])
    if uploaded_file:
        pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        pdf_text = "\n".join(page.get_text() for page in pdf)
        text = st.text_area("Extracted text from PDF (you can edit):", pdf_text, height=300)

if text:
    think_mode = st.checkbox("🤖 Use /think mode (for deeper reasoning)", value=False)
    lang = st.selectbox("🌐 Output language", ["English", "Spanish", "French", "German", "Italian", "Portuguese"])
    if st.button("Explain"):
        with st.spinner("Thinking..."):
            prompt = f"""### Instruction:
You are a legal assistant AI that simplifies and explains legal contract language.

### Input:
{text.strip()}

### Task:
Explain the above clause in simple {lang}.

{"Use deeper reasoning and analogy. /think" if think_mode else ""}

### Response:
"""
            output = generator(prompt)[0]["generated_text"]
            response = output.split("### Response:")[-1].strip()
            st.success("Explanation:")
            st.write(response)

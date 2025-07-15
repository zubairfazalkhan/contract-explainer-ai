import gradio as gr
from transformers import pipeline

# Load model
generator = pipeline("text-generation", model="openai-community/gpt2", max_new_tokens=100)

def explain_clause(text, think_mode=False, lang="English"):
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
    return response

iface = gr.Interface(
    fn=explain_clause,
    inputs=[
        gr.Textbox(label="Contract Clause", lines=6, placeholder="Paste legal text here..."),
        gr.Checkbox(label="Use /think mode"),
        gr.Dropdown(["English", "Spanish", "French", "German", "Italian", "Portuguese"], label="Output Language")
    ],
    outputs="text",
    title="📄 Contract Clause Explainer AI",
    description="Paste any legal clause and get a simplified explanation. Powered by GPT-2."
)

if __name__ == "__main__":
    iface.launch()

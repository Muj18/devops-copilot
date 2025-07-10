import os
import streamlit as st
from openai import OpenAI

# Set Streamlit page config
st.set_page_config(
    page_title="DevOps Copilot",
    page_icon="🧠",
)

# Initialize OpenAI client
if "OPENAI_API_KEY" not in os.environ:
    st.warning("⚠️ OpenAI API key is not set. Please add it as an environment variable.")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))

# Track generated code across reruns
if "generated_code" not in st.session_state:
    st.session_state.generated_code = ""

# App Title and Intro
st.title("🧠 DevOps Copilot")
st.markdown("Build production-ready infrastructure code in seconds.")

st.markdown("""
### 🚀 How It Works:
1. Select a template  
2. Click **Generate Code**  
3. Copy the output or download (if enabled)  
""")

# Step 1 – Choose a template
with st.form("template_form"):
    template = st.selectbox(
        "Choose your infrastructure template:",
        ["EKS + RDS", "Static S3 Website", "Lambda + API Gateway"]
    )
    submitted = st.form_submit_button("🚧 Generate Code")

# Step 2 – Generate code on submit
if submitted:
    st.info("⏳ Generating Terraform code with AI...")

    prompt = f"""
    Generate Terraform code for the following infrastructure:
    - {template}
    Keep it production-ready but easy to understand for a DevOps beginner.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a DevOps assistant that writes clean, production-ready Terraform code using best practices."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
        )
        st.session_state.generated_code = response.choices[0].message.content
        st.success("✅ Code generated successfully!")

    except Exception as e:
        st.error(f"❌ Error generating code: {str(e)}")

# Step 3 – Display generated code
if st.session_state.generated_code:
    st.markdown("### 🧾 Generated Terraform Code")
    st.code(st.session_state.generated_code, language='hcl')

    with st.expander("📦 Download Project Files"):
        st.warning("🔒 Download restricted in public demo. Sign up to unlock full download.")
        st.button("Download ZIP (Pro Only)", disabled=True)

# Feedback Footer
st.markdown("---")
st.markdown("Made by DevOps Copilot | v0.1")
st.text_area("💬 Have feedback? Let us know:")

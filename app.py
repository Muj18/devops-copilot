import os
import io
import streamlit as st
from openai import OpenAI

# Load OpenAI key securely from environment
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Streamlit page setup
st.set_page_config(page_title="DevOps Copilot", page_icon="🧠")
st.title("🧠 DevOps Copilot")
st.markdown("Build production-grade DevOps code in seconds using AI.")

# Tool selection
tool = st.selectbox("Select a DevOps tool:", [
    "Terraform",
    "Docker",
    "CI/CD (GitHub Actions)",
    "Kubernetes",
    "Monitoring (Prometheus)",
    "IAM Policies",
    "Helm Charts",
    "Other"
])

# Suggested prompts per tool
default_prompts = {
    "Terraform": "Generate Terraform to create an EKS cluster with 2 node groups and S3 backend.",
    "Docker": "Create a Dockerfile for a Python Flask app with gunicorn.",
    "CI/CD (GitHub Actions)": "Generate a GitHub Actions workflow to deploy a Node.js app to AWS EC2.",
    "Kubernetes": "Generate Kubernetes Deployment and Service YAML for a Django app.",
    "Monitoring (Prometheus)": "Write Prometheus alert rules for high CPU and memory usage.",
    "IAM Policies": "Create an IAM policy allowing S3 read/write for a Lambda function.",
    "Helm Charts": "Create a Helm chart for a basic Go web app.",
    "Other": ""
}

# User input
user_prompt = st.text_area("Describe what you want:", value=default_prompts.get(tool, ""), height=150)

# File extension mapping
file_extensions = {
    "Terraform": "tf",
    "Docker": "Dockerfile",
    "CI/CD (GitHub Actions)": "yml",
    "Kubernetes": "yml",
    "Monitoring (Prometheus)": "yml",
    "IAM Policies": "json",
    "Helm Charts": "yml",
    "Other": "txt"
}

# Code generation
if st.button("🚀 Generate Code"):
    if not user_prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Generating code using GPT..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a DevOps assistant. Return production-ready code only. No markdown or explanations. Use correct formats: HCL, YAML, Dockerfile, etc.",
                        },
                        {
                            "role": "user",
                            "content": user_prompt,
                        },
                    ],
                    temperature=0.2,
                    max_tokens=2000,
                )
                code = response.choices[0].message.content
                st.code(code)

                # Download setup
                ext = file_extensions.get(tool, "txt")
                filename = ext if ext == "Dockerfile" else f"generated.{ext}"
                buffer = io.BytesIO(code.encode("utf-8"))

                st.download_button(
                    label="💾 Download Code",
                    data=buffer,
                    file_name=filename,
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"❌ Error generating code: {e}")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by DevOps Copilot | v0.2")

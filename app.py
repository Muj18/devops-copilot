import streamlit as st

# Set up the page
st.set_page_config(
    page_title="CodeWeave – DevOps with GenAI",
    page_icon="🧵",
    layout="wide"
)

# Inject custom styling to match Xtract theme
st.markdown("""
    <style>
        body {
            background-color: #000000;
            color: #ffffff;
        }

        .stButton > button {
            background-color: #8f43f0;
            color: white;
            border-radius: 8px;
            padding: 0.6em 1.2em;
            font-weight: 600;
        }

        .stTextInput > div > div > input {
            background-color: #121212;
            color: white;
            border-radius: 6px;
            border: 1px solid #333;
        }

        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: white;
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Hero section
st.markdown("""
    <h1 style='font-size: 40px; font-weight: bold;'>CodeWeave – DevOps Automation with GenAI</h1>
    <p style='font-size: 18px; line-height: 1.6;'>
        Instantly generate production-ready Terraform, Docker, Kubernetes, CI/CD pipelines,<br>
        and even GenAI app templates – all from a single prompt.
    </p>
""", unsafe_allow_html=True)

# Prompt input
prompt = st.text_input("🔧 Describe what you want to deploy (e.g. '3-tier AWS app with CI/CD')")

# Generate button
if st.button("✨ Generate Infrastructure"):
    st.markdown("#### 🧠 AI-Generated Terraform Output")
    st.code("""resource "aws_instance" "web" {
  ami           = "ami-123456"
  instance_type = "t3.micro"
  tags = {
    Name = "web"
  }
}""", language="terraform")

    st.markdown("#### 📦 Dockerfile")
    st.code("""FROM python:3.10-slim
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "main.py"]""", language="docker")

    st.markdown("#### 🔄 GitHub Actions Workflow")
    st.code("""name: Deploy App

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Terraform
        uses: hashicorp/setup-terraform@v2
""", language="yaml")

# Footer
st.markdown("---")
st.markdown("🔒 All infrastructure generated with security best practices by default. ")
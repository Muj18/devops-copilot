import streamlit as st

st.set_page_config(page_title="CodeWeave", layout="centered")

st.title("CodeWeave – DevOps Copilot")

st.write("Enter your infrastructure prompt below and let AI generate the code for you.")

prompt = st.text_input("What do you want to generate?", "")

if st.button("Generate"):
    st.subheader("Terraform Output")
    st.code("""
resource "aws_instance" "web" {
  ami           = "ami-123456"
  instance_type = "t3.micro"
}
""", language="terraform")

    st.subheader("Dockerfile")
    st.code("""
FROM python:3.10
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
""", language="docker")

    st.subheader("CI/CD Pipeline")
    st.code("""
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy with Terraform
        run: terraform apply
""", language="yaml")

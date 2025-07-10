import os
import streamlit as st
import streamlit.components.v1 as components
import httpx
from openai import OpenAI

# ✅ Plausible Analytics tracking script
components.html("""
<script defer data-domain="devops-copilot.onrender.com" src="https://plausible.io/js/script.js"></script>
""", height=0)

# ✅ Function to fetch today's visitor count from Plausible
def get_visitor_count():
    try:
        headers = {
            "Authorization": f"Bearer " + os.environ["PLAUSIBLE_API_KEY"]
        }
        params = {
            "site_id": "devops-copilot.onrender.com",
            "period": "day"
        }
        response = httpx.get(
            "https://plausible.io/api/v1/stats/visitors",
            headers=headers,
            params=params,
            timeout=5
        )
        if response.status_code == 200:
            return response.json().get("value", 0)
    except Exception as e:
        print(f"Visitor count error: {e}")
    return None

# ✅ Show visitor count in sidebar
visitor_count = get_visitor_count()
if visitor_count is not None:
    st.sidebar.markdown(f"👥 **Visitors Today:** {visitor_count}")

# 🔑 Load OpenAI key securely
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# 📄 Page setup
st.set_page_config(page_title="DevOps Copilot", page_icon="🧠")
st.title("🧠 DevOps Copilot")
st.markdown("Build production-grade DevOps code in seconds using AI.")

# 🧰 Tool selection
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

# 💬 Suggested prompts
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

# 📝 Prompt input
user_prompt = st.text_area("Describe what you want:", value=default_prompts.get(tool, ""), height=150)

# 🚀 Generate button with Plausible custom event
if st.button("🚀 Generate Code"):
    # 🔘 Track click event
    components.html("""
    <script>
      if (window.plausible) {
        plausible('generate-code-clicked');
      }
    </script>
    """, height=0)

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
                st.markdown("### 🧾 Generated Code")
                st.code(code)

            except Exception as e:
                st.error(f"❌ Error generating code: {e}")

# 🧾 Footer
st.markdown("---")
st.markdown("Made by DevOps Copilot | v0.2")

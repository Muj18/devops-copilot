import os
import streamlit as st
import streamlit.components.v1 as components
import httpx
from openai import OpenAI
from datetime import datetime

# ✅ Embed Plausible Analytics
components.html("""
<script defer data-domain="devops-copilot.onrender.com" src="https://plausible.io/js/script.js"></script>
""", height=0)

def get_visitor_count():
    try:
        headers = {"Authorization": f"Bearer {os.environ['PLAUSIBLE_API_KEY']}"}
        params = {"site_id": "devops-copilot.onrender.com", "period": "day"}
        response = httpx.get("https://plausible.io/api/v1/stats/visitors", headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            return response.json().get("value", 0)
    except Exception as e:
        print(f"Visitor count error: {e}")
    return None

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

st.set_page_config(page_title="DevOps Copilot", page_icon="🧠")

st.markdown("# 🧠 DevOps Copilot")
st.markdown("""
### Generate production-grade DevOps code with AI  
No boilerplate. No guesswork. Just structured HCL, YAML, and CI/CD pipelines — ready to deploy.
""")

# State setup
for key in ["user_prompt", "code_result", "request_count", "selected_tool", "is_generating", "should_generate"]:
    if key not in st.session_state:
        st.session_state[key] = "" if "prompt" in key or "code" in key else 0 if "count" in key else False
st.session_state["selected_tool"] = st.session_state.get("selected_tool", "Terraform")

# Prompt suggestions
default_prompts = {
    "Terraform": "Generate Terraform to create an EKS cluster with 2 node groups and S3 backend.",
    "Docker": "Create a Dockerfile for a Python Flask app with gunicorn.",
    "CI/CD (GitHub Actions)": "Generate a GitHub Actions workflow to deploy a Node.js app to AWS EC2.",
    "Kubernetes": "Generate Kubernetes Deployment and Service YAML for a Django app.",
    "Monitoring (Prometheus)": "Write Prometheus alert rules for high CPU and memory usage.",
    "IAM Policies": "Create an IAM policy allowing S3 read/write for a Lambda function.",
    "Helm Charts": "Create a Helm chart for a basic Go web app.",
    "AWS": "Generate AWS CLI commands to launch an EC2 instance and create an S3 bucket.",
    "GCP": "Write a GCP Deployment Manager config to deploy a Cloud Function with Pub/Sub trigger.",
    "Azure": "Write Azure CLI commands to provision an AKS cluster with autoscaling.",
    "Other": ""
}

# Sidebar
visitor_count = get_visitor_count()
st.sidebar.markdown("## 📊 Session Stats")
if visitor_count is not None:
    st.sidebar.markdown(f"👥 **Visitors Today:** {visitor_count}")
MAX_REQUESTS = 5
remaining = MAX_REQUESTS - st.session_state["request_count"]
st.sidebar.markdown(f"🔄 **Free Runs Left:** {remaining} / {MAX_REQUESTS}")
st.sidebar.caption("Limit resets on browser refresh or using reset button.")

if st.sidebar.button("♻️ Reset Session"):
    st.session_state["user_prompt"] = default_prompts.get(st.session_state["selected_tool"], "")
    st.session_state["code_result"] = ""
    st.session_state["request_count"] = 0
    st.rerun()

# Tool selection
tool = st.selectbox(
    "🔧 Select a DevOps tool or platform:",
    list(default_prompts.keys()),
    index=list(default_prompts.keys()).index(st.session_state["selected_tool"]),
    disabled=st.session_state["is_generating"]
)

if tool != st.session_state["selected_tool"]:
    st.session_state["user_prompt"] = default_prompts.get(tool, "")
    st.session_state["selected_tool"] = tool

# Example prompt
example = default_prompts.get(tool, "")
with st.expander("📌 Example Prompt"):
    st.code(example)
    if st.button("Use this example prompt"):
        st.session_state["user_prompt"] = example
        st.rerun()

# Limit check
if remaining <= 0:
    st.error("⚠️ Daily free limit reached. Please come back tomorrow or reset.")
    st.stop()

# Prompt input
user_prompt = st.text_area(
    "📝 Describe what you want:",
    value=st.session_state["user_prompt"],
    height=200
)

if st.button("🚀 Generate Code"):
    st.session_state["is_generating"] = True
    st.session_state["should_generate"] = True
    st.rerun()

# Code generation
if st.session_state["should_generate"]:
    st.session_state["should_generate"] = False

    components.html("""
    <script>
      if (window.plausible) {
        plausible('generate-code-clicked');
      }
    </script>
    """, height=0)

    with st.spinner("🤖 Generating code using AI..."):
        try:
            timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            st.sidebar.markdown("---")
            st.sidebar.markdown(f"🕒 **Last Used**: {timestamp}")
            st.sidebar.markdown(f"🔧 **Tool**: {tool}")
            st.sidebar.markdown(f"📝 **Prompt**: {user_prompt[:60]}...")

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
            st.session_state["code_result"] = code
            st.session_state["user_prompt"] = user_prompt
            st.session_state["request_count"] += 1

        except Exception as e:
            st.error(f"❌ Error generating code: {e}")
        finally:
            st.session_state["is_generating"] = False
            st.rerun()

# Full-width code output
if st.session_state["code_result"]:
    st.markdown("### 🧾 Generated Code")
    st.code(st.session_state["code_result"])
    st.download_button(
        label="💾 Download Code",
        data=st.session_state["code_result"],
        file_name="devops_code.txt",
        mime="text/plain"
    )

# Footer
st.markdown("---")
st.markdown("""
Made by [DevOps Copilot](https://devops-copilot.onrender.com) | v0.2  
""")

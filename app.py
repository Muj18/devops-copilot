import os
import streamlit as st
import streamlit.components.v1 as components
import httpx
from openai import OpenAI
from datetime import datetime

# ✅ Config
st.set_page_config(page_title="Codeweave Copilot", page_icon="🧠", layout="wide")

# ✅ Custom styles
st.markdown("""
<style>
.big-title {
    font-size: 2.5rem;
    font-weight: 800;
    color: #2E8B57;
    margin-bottom: 0;
}
.sub-title {
    font-size: 1.1rem;
    color: #444;
    margin-top: 0;
    margin-bottom: 1rem;
}
.stTextArea textarea {
    font-family: monospace;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# ✅ Plausible analytics
components.html("""
<script defer data-domain="devops-copilot.onrender.com" src="https://plausible.io/js/script.js"></script>
""", height=0)

# ✅ Visitor count (from Plausible)
def get_visitor_count():
    try:
        headers = {"Authorization": f"Bearer " + os.environ['PLAUSIBLE_API_KEY']}
        params = {"site_id": "devops-copilot.onrender.com", "period": "day"}
        response = httpx.get("https://plausible.io/api/v1/stats/visitors", headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            return response.json().get("value", 0)
    except Exception as e:
        print(f"Visitor count error: {e}")
    return None

# ✅ OpenAI client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# ✅ Prompt templates
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
    "GenAI App Templates": "Create a Python-based LangChain chatbot with OpenAI, memory, and a Streamlit frontend.",
    "Other": ""
}

# ✅ Session state
for key, default in {
    "user_prompt": "",
    "code_result": "",
    "request_count": 0,
    "is_generating": False,
    "should_generate": False,
    "selected_tool": "Terraform"
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ✅ Sidebar
visitor_count = get_visitor_count()
MAX_REQUESTS = 5
remaining = MAX_REQUESTS - st.session_state["request_count"]

st.sidebar.title("📊 Session Stats")
if visitor_count is not None:
    st.sidebar.markdown(f"👥 **Visitors Today:** {visitor_count}")
st.sidebar.markdown(f"🔄 **Free Runs Left:** {remaining} / {MAX_REQUESTS}")

# ✅ Feedback Link (Sidebar)
st.sidebar.markdown("---")
st.sidebar.markdown("🗣️ **Feedback**")
st.sidebar.markdown(
    "[Click here to share feedback](https://docs.google.com/forms/d/e/1FAIpQLScSlOGUp-uFMR-_420rLU2SBoASfP77blWUVPkYjTediSrQ2A/viewform?usp=header)",
    unsafe_allow_html=True
)

if st.sidebar.button("♻️ Reset Session"):
    st.session_state.update({
        "user_prompt": default_prompts[st.session_state["selected_tool"]],
        "code_result": "",
        "request_count": 0,
        "is_generating": False,
        "should_generate": False,
        "prompt_input": default_prompts[st.session_state["selected_tool"]]
    })
    st.rerun()

# ✅ Hero Section
st.markdown('<div class="big-title">🧠 Codeweave Copilot</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Your AI-powered DevOps + GenAI assistant. Generate infra, pipelines, apps instantly.</div>', unsafe_allow_html=True)

# ✅ Tool dropdown
tool = st.selectbox("🔧 Choose a DevOps or GenAI Template:", list(default_prompts.keys()), index=list(default_prompts.keys()).index(st.session_state["selected_tool"]), disabled=st.session_state["is_generating"])
if tool != st.session_state["selected_tool"]:
    st.session_state["selected_tool"] = tool
    st.session_state["user_prompt"] = default_prompts[tool]
    st.session_state["prompt_input"] = default_prompts[tool]
    st.rerun()

# ✅ Example prompt
example = default_prompts.get(tool, "")
with st.expander("📌 Example Prompt", expanded=False):
    st.code(example)
    if st.button("Use this example prompt"):
        st.session_state["user_prompt"] = example
        st.session_state["prompt_input"] = example
        st.rerun()

# ✅ Usage limit
if remaining <= 0:
    st.error("⚠️ Daily free limit reached. Please come back tomorrow or reset.")
    st.stop()

# ✅ Prompt Input
user_prompt = st.text_area("📝 Describe what you want:", value=st.session_state.get("prompt_input", st.session_state["user_prompt"]), height=200, key="prompt_input")

# ✅ Generate Button
if st.button("🚀 Generate Code"):
    st.session_state.update({
        "is_generating": True,
        "should_generate": True,
        "user_prompt": user_prompt
    })
    st.rerun()

# ✅ OpenAI Request
if st.session_state["should_generate"]:
    st.session_state["should_generate"] = False
    with st.spinner("🤖 Generating code using OpenAI..."):
        try:
            timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            st.sidebar.markdown("---")
            st.sidebar.markdown(f"🕒 **Last Used**: {timestamp}")
            st.sidebar.markdown(f"🔧 **Tool**: {tool}")
            st.sidebar.markdown(f"📝 **Prompt**: {user_prompt[:60]}...")

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a DevOps and GenAI assistant. Return production-ready code only. Use correct formats: HCL, YAML, Dockerfile, Python, etc. No markdown or explanations."},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,
                max_tokens=2000,
            )

            code = response.choices[0].message.content
            st.session_state["code_result"] = code
            st.session_state["request_count"] += 1
        except Exception as e:
            st.error(f"❌ Error generating code: {e}")
        finally:
            st.session_state["is_generating"] = False
            st.rerun()

# ✅ Output Section
if st.session_state["code_result"]:
    st.markdown("### 🧾 Generated Code")
    st.code(st.session_state["code_result"])
    st.download_button("💾 Download Code", data=st.session_state["code_result"], file_name="generated_code.txt", mime="text/plain")

# ✅ Footer & Feedback
st.markdown("---")
st.markdown("💬 Have feedback or ideas? [Tell us here](https://docs.google.com/forms/d/e/1FAIpQLScSlOGUp-uFMR-_420rLU2SBoASfP77blWUVPkYjTediSrQ2A/viewform?usp=header)", unsafe_allow_html=True)
st.caption("🚀 Built by Codeweave — v0.3 | [Visit Site](https://codeweave.co)")

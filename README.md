# 🧠 DevOps Copilot

**AI-powered Infrastructure Generator** — instantly build production-ready DevOps code using natural language prompts.

---

## 🚀 What It Does

DevOps Copilot is an AI assistant that generates infrastructure code for:

- **Terraform** (EKS, Lambda, RDS, S3, etc.)
- **Dockerfiles**
- **Kubernetes manifests**
- **GitHub Actions workflows**
- **IAM policies**
- **Helm charts**
- ... and more.

Just describe what you want, and DevOps Copilot returns ready-to-use code — no copy-pasting from ChatGPT and tweaking manually.

---

## ✨ Demo (Live on Render)

🖥️ Try it here (no sign-up):  
**🔗 https://devops-copilot.onrender.com/**

---

## 🔧 Tech Stack

- [Streamlit](https://streamlit.io/)
- [OpenAI GPT-4](https://platform.openai.com/)
- Python 3.10+
- Deployed on [Render](https://render.com)

---

## 📦 Features

- Simple UI: Pick a template or enter a custom prompt
- Clean, production-ready code generation
- Multi-tool support for DevOps and Cloud Engineers
- No downloads or installs needed

---

## 🛡️ Security

- **No secrets stored.** API key is loaded via environment variable.
- Sensitive files like `secrets.toml` are excluded via `.gitignore`.

---

## 📚 Usage (Local Setup)

```bash
git clone https://github.com/Muj18/devops-copilot.git
cd devops-copilot
pip install -r requirements.txt

# Set your OpenAI key (you can also export it in your shell)
export OPENAI_API_KEY=your-key-here

streamlit run app.py

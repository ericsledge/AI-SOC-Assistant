# 📘 Part A – Install and Run the Finished Project

> **Estimated Time:** 45–90 minutes  
> **Difficulty:** 🟢 Beginner  
> **Prerequisites:** None

---

# 👋 Welcome

Welcome to the **AI SOC Analyst Assistant** installation guide!

This guide is written for beginners and assumes you have **little or no experience** with:

- 🐍 Python
- 💻 Visual Studio Code
- 🌿 Git
- ☁️ GitHub
- 🤖 Artificial Intelligence
- 📚 Retrieval-Augmented Generation (RAG)
- 🛡️ Cybersecurity

By the end of this guide, you will have a fully working copy of the **AI SOC Analyst Assistant** running on your own computer.

Unlike many setup guides, this tutorial explains **what you are doing**, **why you are doing it**, and **how to fix common problems** if something doesn't work as expected.

One of the primary goals of this project is to demonstrate how modern AI-assisted cybersecurity tools can operate entirely on your local machine.

After the initial installation and model download, the application performs knowledge retrieval and AI inference locally without requiring cloud AI services or API keys.

> 💡 **Tip:** Take your time. Don't skip steps. Every section builds on the previous one.

---

# 🎯 What You'll Accomplish

By completing Part A, you will:

- ✅ Install all required software
- ✅ Download the project from GitHub
- ✅ Configure a Python virtual environment
- ✅ Install the project's dependencies
- ✅ Install Ollama
- ✅ Download the local Llama 3.2 language model
- ✅ Build the local cybersecurity knowledge base
- ✅ Launch the AI SOC Analyst Assistant
- ✅ Verify that everything is working correctly

When you're finished, you'll have the completed project running locally and be ready to explore its cybersecurity features.

---

# 🖥️ What You'll Build

By the end of this project, you'll have a local AI-powered cybersecurity assistant capable of:

- Answering cybersecurity questions using Retrieval-Augmented Generation (RAG)
- Searching MITRE ATT&CK, MITRE ATLAS, MITRE D3FEND, NIST, OWASP, CVEs, and Log4Shell documentation
- Performing local phishing email analysis
- Running completely offline after installation using Ollama
- Operating without cloud AI APIs or paid AI subscriptions

---

# 💻 System Requirements

Before installing the project, make sure your computer meets the following minimum requirements.

| Component | Minimum Requirement | Recommended |
|-----------|---------------------|-------------|
| Operating System | Windows 10 | Windows 11 |
| Processor | Dual-Core CPU | Quad-Core CPU or better |
| Memory (RAM) | 8 GB | 16 GB or more |
| Storage | 15 GB free | 25 GB or more |
| Internet | Required during initial setup | Broadband |

> ℹ️ The project uses a locally hosted Large Language Model (LLM). More RAM generally results in better AI performance.

> 💡 A dedicated GPU is **not required**. The project runs on standard CPUs using Ollama, although systems with more CPU cores, additional RAM, or GPU acceleration will generally generate responses faster.

---

# 🛠️ Required Software

You'll install the following tools during this guide.

| Software | Purpose |
|----------|---------|
| Python | Runs the application |
| Git | Downloads and manages the project repository |
| GitHub | Hosts the project source code |
| Visual Studio Code | Development environment |
| Ollama | Runs the local Large Language Model |
| Streamlit | Provides the application's web interface (installed automatically) |

Don't worry if you've never used any of these tools before. Every installation is explained step by step.

All commands shown throughout this guide are executed from **Windows PowerShell inside Visual Studio Code**.

---

# 🌐 Internet Requirements

An internet connection is only required during the initial setup to:

- Download the project from GitHub
- Install Python packages
- Download Ollama
- Download the Llama 3.2 language model
- Download the cybersecurity knowledge base

After setup is complete, the AI SOC Analyst Assistant is designed to perform:

- Local AI inference
- Local semantic search
- Local phishing analysis
- Local Retrieval-Augmented Generation (RAG)

without relying on cloud AI services or API keys.

---

# 📚 Before You Continue

Before moving to the next section, confirm that:

- ☐ You have access to a Windows computer.
- ☐ You have an internet connection.
- ☐ You have permission to install software on your computer.
- ☐ You have at least 15 GB of free storage available.

If you've checked all four boxes, you're ready to begin installing the required software.

Next, you'll install Git, which allows you to download the project from GitHub and keep your local copy updated as the project evolves.

➡️ **Continue to Section 5 – Installing Git**
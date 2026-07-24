<div align="center">

# 🛡️ AI SOC Analyst Assistant

### 🤖 Retrieval-Augmented Generation (RAG) Cybersecurity Assistant

### Built with Python • Ollama • FAISS • Streamlit • MITRE ATT&CK • NIST • OWASP

---

![Python](https://img.shields.io/badge/Python-3.13+-blue?style=for-the-badge&logo=python)

![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-red?style=for-the-badge&logo=streamlit)

![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-green?style=for-the-badge)

![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-black?style=for-the-badge)

![GitHub](https://img.shields.io/badge/GitHub-Portfolio_Project-lightgrey?style=for-the-badge&logo=github)

![License](https://img.shields.io/badge/License-Educational-blueviolet?style=for-the-badge)

---

### 🧠 Local AI • 📚 RAG • 🔍 Cybersecurity Knowledge • 💻 No API Keys Required

</div>

---

# 📖 Table of Contents

- 🎯 Project Overview
- 🚀 Why This Project?
- ✨ Features
- 🛠 Technology Stack
- 🧠 What is Retrieval-Augmented Generation (RAG)?
- 🏗 Project Architecture
- 📂 Repository Structure
- 📘 Complete Beginner Documentation
- 📸 Project Screenshots
- 🎓 Learning Outcomes
- 💼 Skills Demonstrated
- 🚀 Future Improvements
- 👨‍💻 Author

---

# 🎯 Project Overview

The **AI SOC Analyst Assistant** is a fully local Retrieval-Augmented Generation (RAG) application designed to assist Security Operations Center (SOC) analysts with cybersecurity investigations.

Instead of relying only on a Large Language Model (LLM), this application retrieves relevant cybersecurity documentation before generating a response. This approach significantly improves answer quality, reduces hallucinations, and provides traceable citations.

The project combines modern Artificial Intelligence with trusted cybersecurity frameworks to produce grounded responses based on real documentation.

Everything runs locally on your own computer using Ollama.

✅ No OpenAI API

✅ No monthly subscription

✅ No internet connection required after setup

---

# 🚀 Why This Project?

Large Language Models are incredibly powerful—but they also have limitations.

Traditional AI assistants can:

❌ Hallucinate

❌ Invent cybersecurity facts

❌ Misquote frameworks

❌ Forget important details

❌ Produce answers without evidence

Retrieval-Augmented Generation (RAG) solves these problems by allowing the AI to search trusted cybersecurity documents before answering.

This project demonstrates how modern AI systems can be combined with trusted knowledge sources to produce more accurate and transparent results.

---

# ✨ Features

## 🤖 Artificial Intelligence

- Local LLM using Ollama
- Llama 3.2 integration
- Retrieval-Augmented Generation (RAG)
- Context-aware prompting
- Citation-supported answers

---

## 📚 Knowledge Base

The assistant searches documents from:

- 🛡 MITRE ATT&CK
- 🏛 NIST Cybersecurity Framework
- 🔐 NIST Password Guidelines
- 🌐 OWASP
- 🎣 CISA Phishing Guidance
- 📄 Incident Response Playbooks

---

## 🔍 Cybersecurity Features

- IOC Extraction
- Threat Intelligence Lookup
- Incident Response Assistance
- MITRE ATT&CK Explanations
- Phishing Detection
- Password Security Guidance
- Authentication Best Practices
- Logging Recommendations
- SQL Injection Guidance
- XSS Prevention Guidance

---

## 💻 Software Features

- Streamlit Web Interface
- Modular Backend
- PDF Document Loading
- Automatic Text Chunking
- Embedding Generation
- FAISS Vector Database
- Semantic Search
- Automated Testing
- Git Version Control
- Complete Documentation

---

# 🛠 Technology Stack

| Category | Technology |
|-----------|------------|
| Programming Language | Python |
| Artificial Intelligence | Ollama |
| Large Language Model | Llama 3.2 |
| Retrieval System | RAG |
| Embeddings | Sentence Transformers |
| Vector Database | FAISS |
| Frontend | Streamlit |
| PDF Processing | PyMuPDF |
| Testing | Pytest |
| Version Control | Git |
| Repository Hosting | GitHub |
| IDE | Visual Studio Code |

---

# 🧠 What is Retrieval-Augmented Generation (RAG)?

Retrieval-Augmented Generation (RAG) is an AI architecture that combines document retrieval with language generation.

Instead of answering solely from the model's internal knowledge, the assistant first searches a trusted knowledge base, retrieves the most relevant information, and then uses that information to generate an evidence-based response.

This project uses RAG to reduce hallucinations and provide cybersecurity answers grounded in trusted documentation.

---

# 🏗 Project Architecture

```text
                   User Question
                         │
                         ▼
              Streamlit Web Interface
                         │
                         ▼
                  RAG Processing Engine
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
   FAISS Vector Search           Ollama (Llama 3.2)
          │                             │
          ▼                             ▼
 Cybersecurity Documents         AI Response Generation
          │                             │
          └──────────────┬──────────────┘
                         ▼
              Citation Supported Answer
```

---

# 📂 Repository Structure

```text
AI-SOC-Assistant/
│
├── backend/
│
├── frontend/
│
├── knowledge_base/
│   ├── documents/
│   └── indexes/
│
├── tests/
│
├── docs/
│
├── screenshots/
│
├── evaluation/
│
├── data/
│
├── app.py
├── dashboard.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🌟 What Makes This Project Different?

Unlike many AI chatbot projects, this application focuses on **grounded cybersecurity assistance** rather than general conversation.

The assistant retrieves relevant documentation before generating a response, allowing users to verify where information came from.

This creates a more transparent and trustworthy workflow for cybersecurity education, investigation, and analysis.

---

# 📘 Complete Beginner Documentation

One of the primary goals of this repository is education.

This project includes a complete beginner-friendly guide that teaches readers how to recreate the entire application from scratch.

The documentation assumes **no previous experience** with:

- Python
- Git
- GitHub
- Artificial Intelligence
- Retrieval-Augmented Generation
- Streamlit
- FAISS
- Ollama
- Cybersecurity

Each guide walks through every step in detail, from installing software to building every module and deploying the finished project.

The documentation is divided into four parts:

## 📘 Complete Beginner Documentation

This repository includes a complete beginner-friendly guide that teaches readers how to recreate this project from start to finish.

### Documentation

📘 [Part A – Install and Run the Finished Project](docs/Part-A-Install-and-Run.md)

📘 [Part B – Build the Entire Project from Scratch](docs/Part-B-Build-From-Scratch.md)

📘 [Part C – Testing and Validation](docs/Part-C-Testing-and-Validation.md)

📘 [Part D – GitHub Deployment, Troubleshooting, and Final Submission](docs/Part-D-GitHub-Deployment-and-Troubleshooting.md)

---

## ⏭ Continue Reading...

The next section of this README includes:

- 📸 Project Screenshots
- 🎓 Learning Outcomes
- 💼 Skills Demonstrated
- 🚀 Future Improvements
- 👨‍💻 Author Information

---

# 📸 Project Screenshots

Visual demonstrations of the completed AI SOC Analyst Assistant.

> **Note:** If the screenshots below do not appear on GitHub, verify they are located inside the `screenshots/` folder using the same filenames.

---

## 🖥️ Main Dashboard

![Dashboard](screenshots/dashboard.png)

The main interface allows users to ask cybersecurity questions using natural language while interacting with a locally hosted Large Language Model.

---

## 🔍 Retrieval-Augmented Generation (RAG)

![RAG Response](screenshots/rag_response.png)

Every response is generated after searching the cybersecurity knowledge base, helping produce grounded, evidence-supported answers instead of relying only on the language model's memory.

---

## 🎣 Phishing Email Analysis

![Phishing Analysis](screenshots/phishing_analysis.png)

Analyze suspicious emails to identify indicators commonly associated with phishing attempts.

Examples include:

- Suspicious URLs
- Urgent language
- Credential harvesting
- Sender impersonation
- Social engineering tactics

---

## 📚 Source Citations

![Sources](screenshots/source_citations.png)

Rather than simply answering questions, the assistant displays the supporting cybersecurity documentation used to generate the response.

---

## 🧪 Automated Testing

![Pytest](screenshots/pytest_results.png)

Automated tests help ensure the application's core functionality continues working correctly as new features are added.

---

## 🤖 Ollama Running Locally

![Ollama](screenshots/ollama.png)

The entire application runs locally using Ollama, eliminating the need for paid AI APIs.

---

# 🔄 How the Application Works

The following diagram illustrates the complete workflow from a user's question to the final AI-generated response.

```text
                 👤 User

                   │
                   ▼

        💻 Streamlit Web Interface

                   │
                   ▼

         🧠 RAG Processing Engine

        ┌──────────────┬──────────────┐
        ▼                              ▼

📚 Search FAISS Index          🤖 Ollama (Llama 3.2)

        │                              │

        ▼                              ▼

Retrieve Relevant         Generate AI Response
Cybersecurity Chunks

        └──────────────┬──────────────┘

                       ▼

       📄 Citation Supported Response

                       ▼

                👤 Display to User
```

---

# 🎯 Project Goals

The primary objectives of this project were to:

✅ Learn Retrieval-Augmented Generation (RAG)

✅ Build an AI application that runs entirely locally

✅ Integrate a Large Language Model with cybersecurity documentation

✅ Improve response accuracy through document retrieval

✅ Reduce AI hallucinations using trusted knowledge sources

✅ Design a modular and maintainable Python application

✅ Create a beginner-friendly educational resource

✅ Demonstrate software engineering best practices

---

# 📚 What You'll Learn

Working through this repository will introduce you to:

### 🐍 Python Development

- Virtual environments
- Package management
- Project organization
- Modular programming
- Error handling

---

### 🤖 Artificial Intelligence

- Large Language Models
- Prompt Engineering
- Retrieval-Augmented Generation
- Embeddings
- Semantic Search

---

### 📚 Vector Databases

- FAISS
- Document indexing
- Similarity search
- Vector embeddings
- Chunk retrieval

---

### 🛡️ Cybersecurity

- Incident Response
- Threat Intelligence
- MITRE ATT&CK
- NIST Framework
- OWASP
- Phishing Detection
- Indicators of Compromise (IOCs)

---

### 💻 Software Engineering

- Git
- GitHub
- Streamlit
- Testing with Pytest
- Documentation
- Debugging
- Version Control

---

# 🏆 Skills Demonstrated

This project demonstrates practical experience with the following technologies and concepts.

## Programming

- Python
- Object-Oriented Programming
- Modular Software Design

---

## Artificial Intelligence

- Retrieval-Augmented Generation (RAG)
- Local Large Language Models
- Prompt Engineering
- Embedding Generation
- Semantic Search

---

## Cybersecurity

- Security Operations Center (SOC)
- Incident Response
- Threat Intelligence
- Phishing Detection
- MITRE ATT&CK
- NIST Cybersecurity Framework
- OWASP Security Principles

---

## Software Development

- Streamlit
- FAISS
- Git
- GitHub
- Pytest
- Documentation
- Debugging
- Dependency Management

---

# 🚀 Future Improvements

This project establishes a strong foundation for future enhancements.

Potential improvements include:

- 🔍 Advanced threat hunting workflows
- 🌐 Live threat intelligence integrations
- 📊 Interactive security dashboards
- ☁️ Cloud deployment options
- 🔒 User authentication
- 📁 Multi-user document libraries
- 📈 Analytics and reporting
- 🤖 Support for additional local language models
- 📄 Expanded cybersecurity knowledge base
- ⚡ Faster vector indexing
- 🧠 Conversation memory
- 🔄 Automated document synchronization

---

# 🤝 Contributing

Contributions, suggestions, and constructive feedback are always welcome.

If you discover an issue or have an idea for improving the project:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

---

# 🙏 Acknowledgments

This project was made possible through the incredible work of the open-source community.

Special thanks to:

- Python
- Ollama
- Streamlit
- FAISS
- Sentence Transformers
- PyMuPDF
- Hugging Face
- Git
- GitHub

for providing the tools and libraries used throughout this project.

---

# 👨‍💻 Author

## Eric Sledge

**AI • Cybersecurity • Software Development**

GitHub:

https://github.com/ericsledge

---

# ⭐ If You Found This Project Helpful

If this repository helped you learn about:

- Artificial Intelligence
- Cybersecurity
- Retrieval-Augmented Generation (RAG)
- Python Development
- Streamlit
- FAISS
- Ollama

please consider giving the repository a ⭐ on GitHub.

It helps others discover the project and supports continued development.

---

<div align="center">

## 🎉 Thank You for Visiting!

### Happy Learning, Happy Coding, and Stay Curious! 🚀

</div>

---

# ❓ Frequently Asked Questions (FAQ)

### 🔹 Do I need an OpenAI API key?

**No.**

This project runs entirely on your local machine using **Ollama**, so no paid AI subscription or API key is required.

---

### 🔹 Can this project run offline?

**Yes.**

Once Python, Ollama, the required model, and project dependencies are installed, the application can run without an internet connection.

---

### 🔹 Is this project beginner friendly?

**Absolutely.**

This repository is designed for learners.

The documentation assumes little to no experience with:

- Python
- Git
- GitHub
- Artificial Intelligence
- Retrieval-Augmented Generation (RAG)
- Streamlit
- FAISS
- Ollama

The accompanying documentation guides readers through every stage of building, testing, and deploying the application.

---

### 🔹 Can I expand this project?

Yes.

The modular architecture makes it straightforward to add new capabilities, such as:

- Additional cybersecurity frameworks
- New document collections
- Different local language models
- Cloud deployment
- Authentication
- Threat intelligence APIs
- SIEM integrations
- Memory and conversation history

---

### 🔹 Why use Ollama instead of cloud AI services?

Using a local language model provides several advantages.

| Local AI (Ollama) | Cloud AI |
|-------------------|----------|
| 🔒 Greater privacy | Data sent externally |
| 💲 No API costs | Usage-based pricing |
| 📶 Can run offline | Internet required |
| ⚙️ Full local control | Provider-managed |
| 🛡 Suitable for sensitive learning environments | Depends on provider policies |

---

# 📚 Why Retrieval-Augmented Generation (RAG)?

Traditional Large Language Models generate responses using the knowledge they were trained on.

Retrieval-Augmented Generation improves this process by searching a trusted knowledge base before generating an answer.

This project follows that workflow to provide responses that are more accurate, transparent, and grounded in documentation.

| Traditional LLM | Retrieval-Augmented Generation (RAG) |
|-----------------|--------------------------------------|
| Answers from model knowledge | Searches trusted documents first |
| May produce unsupported claims | Grounds responses in retrieved context |
| Limited transparency | Can reference supporting sources |
| General-purpose responses | Tailored to your cybersecurity knowledge base |

---

# 🎯 Project Highlights

This project demonstrates practical experience across multiple disciplines.

### 🤖 Artificial Intelligence

- Local Large Language Models
- Retrieval-Augmented Generation (RAG)
- Prompt Engineering
- Embedding Generation
- Semantic Search

---

### 🛡 Cybersecurity

- Security Operations Center (SOC) concepts
- Incident Response
- Threat Intelligence
- Phishing Analysis
- MITRE ATT&CK
- NIST Cybersecurity Framework
- OWASP Security Guidance

---

### 💻 Software Engineering

- Python application development
- Modular software architecture
- Streamlit web applications
- Automated testing with Pytest
- Version control using Git
- GitHub repository management
- Technical documentation

---

# 🌱 Why This Repository Exists

This repository was created to demonstrate how modern Artificial Intelligence can be combined with trusted cybersecurity documentation to build practical tools that support learning and analysis.

Rather than sharing only the finished source code, the goal is to provide a complete educational resource that explains how the project is organized, how each component works, and how the entire application can be recreated from scratch.

Whether you're exploring AI, cybersecurity, or software engineering, this project is intended to help you understand both the concepts and the implementation.

---

# 📖 Continue Learning

The documentation included with this repository is organized into four beginner-friendly guides.

| Guide | Description |
|--------|-------------|
| 📘 Part A | Install and Run the Finished Project |
| 📘 Part B | Build the Entire Project from Scratch |
| 📘 Part C | Testing and Validation |
| 📘 Part D | GitHub Deployment, Troubleshooting, and Final Submission |

Each guide builds upon the previous one and is designed to help readers confidently recreate the project step by step.

---

# 📄 License

This repository is provided for educational and portfolio purposes.

You are welcome to study the code, learn from the implementation, and adapt ideas for your own educational projects. If you plan to redistribute or substantially reuse the project, please review the repository's license terms.

---

# 👨‍💻 Author

## Eric Sledge

**AI • Cybersecurity • Python Development**

### Connect with me

- GitHub: https://github.com/ericsledge

---

<div align="center">

# ⭐ Thank You for Visiting!

Thank you for taking the time to explore this project.

I hope this repository helps you better understand Artificial Intelligence, Retrieval-Augmented Generation (RAG), cybersecurity workflows, and modern Python application development.

If you found this project helpful or interesting, consider giving the repository a ⭐ on GitHub.

Your support helps others discover the project and encourages continued learning and development.

---

### 🚀 Keep Learning • Keep Building • Keep Exploring

**Happy Coding!**

</div>
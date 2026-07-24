# 🛡️ AI SOC Analyst Assistant

> **Capstone Project**
>
> **Course:** Capstone Project
>
> **Author:** Eric Sledge
>
> **Institution:** Claflin University
>
> **Project Type:** Retrieval-Augmented Generation (RAG) AI Assistant
>
> **Programming Language:** Python
>
> **Frontend:** Streamlit
>
> **Backend:** Ollama + FAISS + Sentence Transformers
>
> **Version:** 1.0

---

# 📖 Project Overview

The AI SOC Analyst Assistant is an intelligent cybersecurity assistant designed to help Security Operations Center (SOC) analysts retrieve accurate cybersecurity information from a locally stored knowledge base.

Unlike traditional chatbots that rely entirely on information learned during training, this project implements **Retrieval-Augmented Generation (RAG)**. Instead of answering from memory alone, the assistant first searches a cybersecurity knowledge base stored in a FAISS vector database, retrieves the most relevant information, and then uses a local Large Language Model (LLM) through Ollama to generate an informed response.

This design helps reduce hallucinations while allowing the assistant to answer questions using documentation that can be updated over time.

The application runs entirely on a local machine, making it suitable for environments where cloud-based AI services are not permitted due to privacy or security concerns.

---

# 🎯 Project Objectives

The primary objective of this project is to demonstrate how Artificial Intelligence can assist cybersecurity professionals by combining semantic search with modern Large Language Models.

This capstone demonstrates the ability to:

- Build a Retrieval-Augmented Generation (RAG) application
- Process cybersecurity documentation
- Generate vector embeddings
- Store embeddings using FAISS
- Retrieve relevant cybersecurity knowledge
- Generate AI-assisted responses using Ollama
- Display results through a professional web interface
- Log application activity
- Test and validate software functionality

Rather than creating another chatbot, this project focuses on solving a real-world cybersecurity problem by improving information retrieval for SOC analysts.

---

# 🚀 Key Features

The AI SOC Analyst Assistant includes the following features:

✅ Local AI using Ollama

✅ Retrieval-Augmented Generation (RAG)

✅ FAISS Vector Database

✅ Sentence Transformer Embeddings

✅ Cybersecurity Knowledge Base

✅ Streamlit Web Dashboard

✅ Similarity Search

✅ Source Citation Display

✅ Retrieved Context Viewer

✅ Query Response Timing

✅ JSONL Query Logging

✅ Automated Testing

✅ Modular Python Architecture

---

# 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Primary programming language |
| Streamlit | Web application frontend |
| Ollama | Local Large Language Model runtime |
| Llama 3.2 | AI language model |
| FAISS | Vector similarity search |
| Sentence Transformers | Text embeddings |
| Hugging Face | Embedding models |
| PyTorch | Machine learning framework |
| NumPy | Numerical processing |
| JSON | Metadata and logging |
| dotenv | Environment variable management |
| PyTest | Regression testing |

---

# 🏗️ System Architecture

The application follows a modular architecture.

```
                    User

                      │

                      ▼

             Streamlit Dashboard

                      │

                      ▼

               User Question

                      │

                      ▼

                RAG Engine

          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼

    FAISS Vector DB         Ollama LLM

          │                       ▲
          │                       │
          └──── Retrieved Context ┘

                      │

                      ▼

             Generated Response

                      │

                      ▼

              Streamlit Interface

                      │

                      ▼

              Query Logging (JSONL)
```

Each component has a single responsibility, making the project easier to maintain, debug, and expand.

---

# 📂 Project Structure

```
AI-SOC-Assistant/

│
├── backend/
│   ├── chunker.py
│   ├── embeddings.py
│   ├── faiss_store.py
│   ├── rag_engine.py
│   └── ...
│
├── docs/
│   ├── architecture.md
│   ├── installation.md
│   ├── testing.md
│   ├── limitations.md
│   └── user_guide.md
│
├── evaluation/
│   └── soc_questions.json
│
├── frontend/
│   └── streamlit_app.py
│
├── knowledge_base/
│   ├── documents/
│   └── indexes/
│
├── logs/
│   └── rag_queries.jsonl
│
├── tests/
│
├── .env
├── requirements.txt
├── README.md
└── ...
```

---

# 💡 Why Retrieval-Augmented Generation (RAG)?

Large Language Models are extremely powerful but have one major limitation:

They only know what they learned during training.

If cybersecurity guidance changes, a normal chatbot cannot automatically learn those updates.

Retrieval-Augmented Generation solves this problem by allowing the model to retrieve information from external documents before generating an answer.

Instead of relying solely on memory, the workflow becomes:

```
User Question

↓

Search FAISS

↓

Retrieve Relevant Documents

↓

Provide Context to LLM

↓

Generate Accurate Answer
```

This significantly improves factual accuracy while reducing hallucinations.

---

# 🎓 Skills Demonstrated

This project demonstrates practical experience with:

- Artificial Intelligence
- Retrieval-Augmented Generation
- Vector Databases
- Semantic Search
- Python Software Development
- Cybersecurity Knowledge Management
- Local Large Language Models
- Prompt Engineering
- Software Testing
- Logging and Monitoring
- Application Documentation
- Modular Software Design

These are highly transferable skills applicable to cybersecurity, AI engineering, software development, and machine learning roles.

---

# 🖥️ Software Requirements

The project was developed using:

- Windows Server 2025
- Python 3.13+
- Visual Studio Code
- Ollama
- Git (optional until deployment)
- PowerShell
- Streamlit

The project can also run on Windows 11 with minimal modifications.

---

# 💻 Hardware Requirements

Minimum Recommended Hardware

| Component | Recommendation |
|------------|---------------|
| CPU | Quad-Core Processor |
| RAM | 16 GB |
| Storage | 20 GB Free |
| GPU | Optional |
| Internet | Required for initial model downloads |

After all models are downloaded, the assistant operates completely offline.

---

# 📌 Before You Begin

Before attempting to recreate this project, make sure you have:

- Basic Python knowledge
- Administrator access to your computer
- PowerShell
- Visual Studio Code installed
- Python installed
- Ollama installed
- An internet connection for downloading dependencies

Although this README is written for beginners, having a basic understanding of Python will make the setup process easier.

---

# 📈 What You'll Learn

By completing this project, you will gain hands-on experience with:

- Building a real Retrieval-Augmented Generation application
- Creating a semantic search pipeline
- Working with vector databases
- Running local AI models
- Building interactive Python dashboards
- Logging AI activity
- Writing maintainable Python code
- Testing AI applications
- Troubleshooting machine learning software
- Deploying a professional capstone project

This project combines cybersecurity, artificial intelligence, software engineering, and data processing into one complete application.

---

# ⚙️ Installation and Environment Setup

This section walks through the complete installation process required to build and run the AI SOC Analyst Assistant. Every major dependency is explained, along with why it is needed.

---

# 📋 Step 1 – Install Python

Python is the primary programming language used throughout this project. All backend logic, vector processing, AI integration, testing, and the Streamlit dashboard are written in Python.

Download the latest stable version from:

https://www.python.org/downloads/

During installation:

✅ Check **"Add Python to PATH"**

This option allows Python to be executed from PowerShell or the Windows Command Prompt.

Verify the installation by opening PowerShell and running:

```powershell
python --version
```

Example:

```
Python 3.13.5
```

If Python is not recognized, restart your computer or reinstall Python while enabling **Add Python to PATH**.

---

# 📋 Step 2 – Install Visual Studio Code

Visual Studio Code (VS Code) was used as the Integrated Development Environment (IDE) for this project.

Download:

https://code.visualstudio.com/

Recommended Extensions:

- Python
- Pylance
- Black Formatter
- Markdown All in One
- GitLens (optional)

These extensions improve syntax highlighting, IntelliSense, debugging, formatting, and documentation editing.

---

# 📋 Step 3 – Install Ollama

Ollama allows Large Language Models to run completely on your local computer.

Unlike cloud AI providers, Ollama keeps all processing local, making it suitable for environments where sensitive information cannot leave the organization.

Download:

https://ollama.com/

Verify installation:

```powershell
ollama --version
```

---

# 📋 Step 4 – Download the AI Model

This project uses **Llama 3.2** through Ollama.

Download the model:

```powershell
ollama pull llama3.2:3b
```

This downloads the language model to your computer.

Verify:

```powershell
ollama list
```

Example:

```
NAME

llama3.2:3b
```

---

# 📋 Step 5 – Create the Project Folder

Create the project folder.

Example:

```
C:\Capstone\Projects\AI-SOC-Assistant
```

The project structure should resemble:

```
AI-SOC-Assistant
│
├── backend
├── frontend
├── docs
├── tests
├── logs
├── evaluation
├── knowledge_base
│
└── README.md
```

Keeping the project organized from the beginning makes future maintenance significantly easier.

---

# 📋 Step 6 – Create a Python Virtual Environment

A virtual environment isolates project dependencies from the rest of the computer.

Create it:

```powershell
python -m venv venv
```

Activate it:

PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Command Prompt:

```cmd
venv\Scripts\activate
```

Once activated, your terminal should display:

```
(venv)
```

This indicates all Python packages will be installed only for this project.

---

# 📋 Step 7 – Install Project Dependencies

Install all required packages:

```powershell
pip install -r requirements.txt
```

Typical packages include:

- streamlit
- faiss-cpu
- sentence-transformers
- torch
- transformers
- python-dotenv
- numpy
- pytest

Verify:

```powershell
pip list
```

---

# 📋 Step 8 – Configure Environment Variables

Create a file named:

```
.env
```

Example:

```env
OLLAMA_MODEL=llama3.2:3b
OLLAMA_BASE_URL=http://localhost:11434

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

RAG_TOP_K=5
RAG_MINIMUM_SCORE=0.30
RAG_MAX_CONTEXT_CHARACTERS=6000
```

Environment variables separate configuration from application code, making updates easier without modifying Python files.

---

# 📋 Step 9 – Prepare the Knowledge Base

The AI assistant does not answer questions using the internet.

Instead, it searches a local cybersecurity knowledge base.

Example directory:

```
knowledge_base/

    documents/

        phishing.pdf

        nist_ir.pdf

        mitre_attack.pdf

        malware.pdf

        windows_security.pdf
```

These documents are processed into searchable vector embeddings.

---

# 📋 Step 10 – Document Chunking

Large Language Models perform better when documents are divided into smaller sections.

Instead of embedding an entire PDF, the project splits each document into manageable chunks.

Example:

```
Original PDF

↓

100 pages

↓

Chunking

↓

300 text chunks

↓

Embedding

↓

Vector Database
```

Chunking improves retrieval speed and answer quality.

---

# 📋 Step 11 – Generate Embeddings

Each chunk is converted into a numerical representation called an embedding.

The embedding model used is:

```
sentence-transformers/all-MiniLM-L6-v2
```

Embeddings allow semantic searching.

Instead of matching exact words, the system searches based on meaning.

Example:

User asks:

```
How can phishing emails be detected?
```

The system can still retrieve a document discussing:

```
Recognizing malicious emails
```

even if the wording differs.

---

# 📋 Step 12 – Build the FAISS Index

After embeddings are generated, they are stored inside a FAISS vector database.

FAISS provides extremely fast similarity search.

The generated files include:

```
knowledge_base/

    indexes/

        soc_knowledge.faiss

        soc_knowledge_metadata.json
```

The FAISS index stores vectors.

The metadata file stores information about each vector, including document names and chunk locations.

---

# 📋 Step 13 – Understanding the RAG Pipeline

The application follows this workflow:

```
User asks a question

↓

Question converted into an embedding

↓

FAISS searches similar vectors

↓

Relevant chunks returned

↓

Chunks inserted into prompt

↓

Ollama generates response

↓

Answer displayed

↓

Query logged
```

This process happens in only a few seconds.

---

# 📋 Step 14 – Streamlit Dashboard

The frontend was developed using Streamlit.

Launch:

```powershell
streamlit run frontend\streamlit_app.py
```

The dashboard provides:

- Chat interface
- Source document display
- Retrieved context viewer
- Response timing
- Adjustable retrieval settings
- Conversation history
- Error handling

Everything runs locally inside your web browser.

---

# ⚠️ Common Installation Problems

Building AI software involves many dependencies. During development, several common issues were encountered.

### Python not recognized

Cause:

Python was not added to PATH.

Solution:

Reinstall Python with **Add Python to PATH** enabled.

---

### Ollama connection failed

Cause:

The Ollama server was not running.

Solution:

Start Ollama before launching Streamlit.

---

### FAISS index missing

Cause:

The vector database had not been generated.

Solution:

Rebuild the knowledge base and verify the following files exist:

```
soc_knowledge.faiss

soc_knowledge_metadata.json
```

---

### Embedding model download warning

The first execution downloads the embedding model.

This is expected.

Future executions load the cached version.

---

### HF_TOKEN warning

You may see:

```
Warning: unauthenticated requests to Hugging Face
```

This warning does not prevent the application from functioning.

The model will still download successfully.

---

### Streamlit File Watcher Warning

Some versions of Streamlit attempt to inspect deep learning libraries and may produce warnings related to `torchvision`.

If this occurs, disable the file watcher in:

```
.streamlit/config.toml
```

Example:

```toml
[server]
fileWatcherType = "none"
```

---

# 🎉 Installation Complete

If every step above has been completed successfully, you should now have:

- Python installed
- VS Code configured
- Ollama running
- Llama 3.2 downloaded
- Virtual environment configured
- Project dependencies installed
- Knowledge base prepared
- FAISS vector database created
- Streamlit dashboard operational

At this point, the AI SOC Analyst Assistant is ready to answer cybersecurity questions using Retrieval-Augmented Generation (RAG).

---

# 🧠 How the AI SOC Analyst Assistant Works

Understanding how the application works is just as important as knowing how to install it. This section explains the internal workflow of the project from the moment a user enters a question until an answer is displayed.

The application follows a Retrieval-Augmented Generation (RAG) architecture, combining semantic search with a locally hosted Large Language Model (LLM).

---

# 🔄 End-to-End Workflow

Every question follows the same sequence of events:

```
User enters a question

        │

        ▼

Streamlit receives the request

        │

        ▼

Question sent to the RAG Engine

        │

        ▼

Question converted into an embedding

        │

        ▼

FAISS searches the vector database

        │

        ▼

Most relevant document chunks returned

        │

        ▼

Context sent to Ollama

        │

        ▼

Large Language Model generates answer

        │

        ▼

Answer returned to Streamlit

        │

        ▼

Sources displayed

        │

        ▼

Query written to JSONL log
```

Although this looks like a large process, it typically completes within only a few seconds.

---

# 📁 Backend Overview

The backend contains the application's core logic.

```
backend/

    chunker.py

    embeddings.py

    faiss_store.py

    rag_engine.py

    ...
```

Each module has one responsibility.

Following the Single Responsibility Principle makes the project easier to debug, extend, and maintain.

---

# ✂️ chunker.py

Purpose:

Split large cybersecurity documents into smaller pieces before embedding.

Why?

Embedding an entire PDF produces poor search results.

Smaller chunks provide much better retrieval accuracy.

Example:

```
300-page document

↓

Split into

↓

600 chunks

↓

Each chunk embedded separately
```

Advantages:

- Better retrieval accuracy
- Faster searches
- Lower memory usage

---

# 🧠 embeddings.py

Purpose:

Convert text into vector embeddings.

This project uses:

```
sentence-transformers/all-MiniLM-L6-v2
```

Instead of storing words, the embedding model stores numerical representations describing the meaning of the text.

Example:

```
Password Attack

↓

[0.2184,
0.8392,
-0.4118,
...]

384 dimensions
```

Embeddings allow the application to understand semantic meaning rather than relying on exact keyword matching.

---

# 🗄️ faiss_store.py

Purpose:

Store vector embeddings and perform similarity searches.

Responsibilities include:

- Creating the FAISS index
- Loading the index
- Searching the index
- Returning nearest neighbors

FAISS was selected because it provides extremely fast nearest-neighbor searches while remaining lightweight and efficient.

---

# 🤖 rag_engine.py

Purpose:

Coordinate the entire Retrieval-Augmented Generation workflow.

Responsibilities include:

- Receiving user questions
- Embedding questions
- Searching FAISS
- Filtering results
- Building prompts
- Calling Ollama
- Returning responses

The RAG Engine acts as the "brain" of the application.

Without it, the individual components would not communicate with one another.

---

# 🖥️ Frontend Overview

The user interface is implemented using Streamlit.

Main file:

```
frontend/

    streamlit_app.py
```

Responsibilities:

- Display chat interface
- Receive questions
- Display answers
- Show retrieved sources
- Display retrieved chunks
- Measure response time
- Log completed requests
- Handle errors

---

# 💬 Asking a Question

When a user types:

```
What is phishing?
```

the application performs the following steps:

1. The question is sent to the backend.

2. The backend converts the question into an embedding.

3. FAISS searches for similar document chunks.

4. The best matching chunks are returned.

5. Those chunks become context for Ollama.

6. Ollama generates a grounded answer.

7. Streamlit displays:

- Answer
- Sources
- Response time
- Retrieved context (optional)

---

# 📖 Source Display

Every generated response includes the documents that were used.

Example:

```
Sources

• phishing.pdf

• cisa_email_security.pdf

• nist_ir.pdf
```

Displaying sources improves transparency and allows users to verify where the information originated.

---

# 📚 Retrieved Context Viewer

The application can optionally display the exact document chunks retrieved from FAISS.

This feature is useful for:

- Debugging
- Validation
- Demonstrations
- Understanding retrieval quality

Each chunk displays:

- Source document
- Similarity score
- Retrieved text

---

# ⏱️ Response Timing

Each request measures total execution time.

Example:

```
Total Response Time

2.84 seconds
```

This metric includes:

- Retrieval time
- Prompt generation
- Ollama inference
- Total processing time

Performance metrics help identify bottlenecks during development.

---

# 📝 Automatic Query Logging

Every successful and failed request is automatically recorded.

Log file:

```
logs/

    rag_queries.jsonl
```

Each line contains one JSON object.

Example:

```json
{
  "timestamp": "2026-07-24T12:15:33",
  "question": "What is phishing?",
  "model": "llama3.2:3b",
  "top_k": 5,
  "retrieved_chunks": 5,
  "sources": [
      "phishing.pdf"
  ],
  "answer_length": 725,
  "total_seconds": 2.87,
  "status": "success"
}
```

The logging system allows future developers to:

- Measure performance
- Analyze usage
- Detect failures
- Audit AI interactions
- Troubleshoot issues

---

# 📊 Evaluation Dataset

Evaluation questions are stored inside:

```
evaluation/

    soc_questions.json
```

These questions provide a repeatable way to validate retrieval quality.

Example categories include:

- Phishing
- Malware
- Incident Response
- Authentication
- Windows Security
- MITRE ATT&CK
- OWASP

Using a consistent evaluation dataset makes it easier to compare future improvements.

---

# 🧪 Testing

Testing ensures new changes do not break existing functionality.

Run all tests:

```powershell
python -m pytest -v
```

Expected output:

```
3 passed
```

Testing should be performed after:

- Adding new features
- Refactoring code
- Updating dependencies
- Modifying the RAG pipeline

Regression testing improves software reliability.

---

# 📸 Project Screenshots

Document screenshots are valuable for demonstrating project progress.

Recommended screenshots include:

1. Project Folder Structure

2. Streamlit Dashboard

3. Successful AI Response

4. Displayed Sources

5. Retrieved Context

6. FAISS Index Files

7. JSONL Query Log

8. Passing PyTest Results

9. Architecture Diagram

10. Application Running in Browser

These screenshots can be placed inside a `screenshots` directory and referenced throughout the README.

---

# 🔒 Security Considerations

Although this application runs locally, several security considerations should be kept in mind.

### Local AI

Using Ollama ensures that prompts remain on the local machine.

No user questions are sent to external AI providers.

---

### Knowledge Base

Only trusted cybersecurity documents should be added to the knowledge base.

Inaccurate or malicious documents could negatively affect retrieval quality.

---

### Query Logs

The application records user questions.

Production environments should consider:

- Encryption
- Access controls
- Log rotation
- Retention policies

---

### Environment Variables

Configuration values should be stored inside `.env` files.

Avoid hardcoding:

- URLs
- API keys
- Sensitive configuration

---

# 🚀 Performance Considerations

The following factors influence performance:

- CPU speed
- Available RAM
- Embedding model
- Ollama model size
- Number of indexed documents
- Chunk size
- Top-K retrieval value

Reducing `top_k` generally improves response speed, while increasing it may improve answer quality.

Finding the right balance depends on the deployment environment.

---

# 💡 Lessons Learned

Building this project provided experience in several areas beyond Python programming.

Some of the most valuable lessons included:

- AI applications require strong software engineering practices.
- Good document quality produces better AI responses.
- Logging is essential for troubleshooting.
- Testing should be performed after every major change.
- Modular code is easier to maintain than large monolithic scripts.
- Retrieval quality often matters more than model size.
- Clear documentation greatly improves maintainability.

Developing this application required integrating artificial intelligence, cybersecurity, software engineering, and data processing into one cohesive solution.

---

# 📅 Project Development Timeline

This project was developed over a fourteen-week capstone schedule. Each phase introduced new functionality while building upon the previous week's work.

## Week 1 – Project Planning

### Objectives

- Select a capstone topic
- Research Retrieval-Augmented Generation (RAG)
- Define project goals
- Identify required software

### Deliverables

- Project proposal
- Initial architecture planning
- Technology selection

---

## Week 2 – Environment Setup

### Objectives

- Install Python
- Install Visual Studio Code
- Install Ollama
- Create project structure
- Configure virtual environment

### Deliverables

- Working development environment
- Initial project folders

---

## Week 3 – Knowledge Base Processing

### Objectives

- Import cybersecurity documents
- Read PDF and text files
- Clean extracted text
- Prepare documents for chunking

### Deliverables

- Functional document loader

---

## Week 4 – Document Chunking

### Objectives

- Split documents into smaller chunks
- Preserve metadata
- Optimize chunk sizes

### Deliverables

- Reliable chunking pipeline

---

## Week 5 – Embeddings

### Objectives

- Generate vector embeddings
- Evaluate embedding quality
- Integrate Sentence Transformers

### Deliverables

- Semantic document representations

---

## Week 6 – FAISS Vector Database

### Objectives

- Create vector index
- Store metadata
- Implement similarity search

### Deliverables

- Working vector database

---

## Week 7 – Retrieval-Augmented Generation

### Objectives

- Connect FAISS to Ollama
- Build prompt generation
- Retrieve supporting context

### Deliverables

- Fully functioning RAG engine

---

## Week 8 – Streamlit Dashboard

### Objectives

- Design chat interface
- Display AI responses
- Show supporting sources

### Deliverables

- Functional web interface

---

## Week 9 – Feature Enhancements

### Objectives

- Add response timing
- Improve retrieval quality
- Improve error handling

### Deliverables

- Enhanced user experience

---

## Week 10 – Testing

### Objectives

- Develop regression tests
- Validate retrieval pipeline
- Verify AI responses

### Deliverables

- Stable application

---

## Week 11 – Logging

### Objectives

- Implement automatic JSONL logging
- Capture response metrics
- Record application events

### Deliverables

- Persistent query history

---

## Week 12 – Documentation

### Objectives

- Create user guide
- Document installation
- Explain architecture
- Describe limitations

### Deliverables

- Complete technical documentation

---

## Week 13 – Evaluation

### Objectives

- Build evaluation dataset
- Test multiple cybersecurity questions
- Measure retrieval performance

### Deliverables

- Evaluation report

---

## Week 14 – Final Review

### Objectives

- Final testing
- README completion
- Repository preparation
- Presentation readiness

### Deliverables

- Completed capstone project

---

# 🐞 Challenges Encountered

Software development rarely proceeds without obstacles. During development, several technical challenges were encountered and resolved.

---

## Challenge: Python Environment Configuration

### Problem

Python packages were not available across different terminals.

### Resolution

A dedicated virtual environment was created and activated before installing project dependencies.

---

## Challenge: Ollama Connectivity

### Problem

The application could not communicate with the local language model.

### Resolution

Verified that the Ollama service was installed, running, and accessible through the configured local endpoint.

---

## Challenge: Embedding Downloads

### Problem

The embedding model required an initial download before embeddings could be generated.

### Resolution

Allowed the model to download once and reused the locally cached version for subsequent executions.

---

## Challenge: FAISS Index Creation

### Problem

The application could not retrieve document vectors because the FAISS index had not yet been generated.

### Resolution

Successfully generated the vector index and associated metadata before launching the application.

---

## Challenge: Dependency Compatibility

### Problem

Some Python packages produced warnings after installation.

### Resolution

Verified application functionality and ensured all required libraries were installed using compatible versions.

---

## Challenge: Logging

### Problem

Application activity was initially not being recorded.

### Resolution

Implemented automatic JSONL logging for successful and failed requests, including timestamps, response times, retrieved sources, and status information.

---

# 🌱 Future Improvements

Although the project successfully meets its objectives, there are many opportunities for future enhancements.

Potential improvements include:

- User authentication
- Role-based access control
- Multiple knowledge bases
- Database-backed logging
- Dashboard analytics
- GPU acceleration
- Docker deployment
- Continuous Integration (CI)
- Continuous Deployment (CD)
- REST API
- Automatic document ingestion
- Scheduled index rebuilding
- Support for multiple language models
- Conversation memory
- User feedback collection
- Citation confidence scores
- Administrative dashboard
- Cloud deployment options

These enhancements would further improve scalability, usability, and maintainability.

---

# 📚 References

The following resources were consulted throughout development.

## Python

https://www.python.org/

---

## Streamlit

https://streamlit.io/

---

## Ollama

https://ollama.com/

---

## FAISS

https://github.com/facebookresearch/faiss

---

## Sentence Transformers

https://www.sbert.net/

---

## Hugging Face

https://huggingface.co/

---

## PyTorch

https://pytorch.org/

---

## MITRE ATT&CK

https://attack.mitre.org/

---

## NIST Cybersecurity Framework

https://www.nist.gov/cyberframework

---

# 🙏 Acknowledgements

This project was completed as part of a university capstone experience and reflects the integration of software engineering, cybersecurity, artificial intelligence, and modern information retrieval techniques.

Special thanks to the developers and maintainers of the open-source technologies that made this project possible, including the communities behind Python, Streamlit, Ollama, FAISS, Sentence Transformers, Hugging Face, and PyTorch.

---

# 📋 Final Project Checklist

Before presenting or submitting the project, verify the following items:

## Application

- [x] Streamlit dashboard launches successfully
- [x] Ollama is running
- [x] AI responses generate correctly
- [x] Sources are displayed
- [x] Retrieved context is available
- [x] Response timing is shown
- [x] JSONL logging is functioning

---

## Backend

- [x] Knowledge base loads correctly
- [x] Embeddings generate successfully
- [x] FAISS index loads correctly
- [x] Metadata matches vector index
- [x] RAG engine retrieves relevant context

---

## Documentation

- [x] README completed
- [x] Architecture documentation completed
- [x] Installation guide completed
- [x] User guide completed
- [x] Testing documentation completed
- [x] Limitations documented

---

## Testing

- [x] Regression tests pass
- [x] Evaluation dataset created
- [x] Manual testing completed
- [x] Logging verified

---

# 🎓 Skills Demonstrated

Completing this project demonstrates practical experience with:

- Python Programming
- Artificial Intelligence
- Retrieval-Augmented Generation (RAG)
- Local Large Language Models
- Semantic Search
- Vector Databases
- FAISS
- Streamlit
- Prompt Engineering
- Software Architecture
- Software Testing
- Logging and Monitoring
- Technical Documentation
- Problem Solving
- Cybersecurity Knowledge Management

These skills are directly applicable to roles involving cybersecurity, AI development, software engineering, machine learning, and data engineering.

---

# 🏁 Conclusion

The AI SOC Analyst Assistant demonstrates how Retrieval-Augmented Generation (RAG) can improve the accuracy and usefulness of AI-powered cybersecurity assistants by combining semantic search with a locally hosted Large Language Model.

Throughout this capstone project, a complete end-to-end application was designed and implemented using Python, Streamlit, Ollama, FAISS, and Sentence Transformers. The project includes document processing, vector embedding generation, semantic retrieval, AI-assisted response generation, automated logging, testing, and comprehensive documentation.

By operating entirely on local resources, the application provides a privacy-conscious alternative to cloud-based AI services while remaining flexible enough to support future enhancements. The modular architecture allows additional features, new knowledge sources, and alternative language models to be integrated with minimal changes to the existing codebase.

This project represents the successful application of software engineering principles, artificial intelligence techniques, and cybersecurity knowledge to solve a practical information retrieval problem. It also demonstrates proficiency in system design, technical documentation, testing, and iterative development, providing a strong foundation for future work in AI-assisted cybersecurity solutions.

---

# 📬 Contact

Author: Eric Sledge

Course: Cybersecurity Masters Capstone Project

Institution: Claflin University

**GitHub:** *(Add your repository URL after publishing)*

Version: 1.0

---

**Thank you for taking the time to review this project. Feedback and suggestions for future improvements are always welcome.**

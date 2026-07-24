# 📘 Part B – Build the AI SOC Analyst Assistant from Scratch

> **Estimated Time:** 8–15 Hours  
> **Difficulty:** 🟡 Beginner to Intermediate  
> **Prerequisites:** Complete Part A or have Python, Git, VS Code, and Ollama installed.

---

# 👋 Welcome

Congratulations on making it this far!

If you've completed **Part A**, you already have the finished AI SOC Analyst Assistant running on your computer.

Now comes the exciting part.

Instead of simply using the project, you're going to **build it yourself**.

By the end of this guide, you'll have recreated the entire application from an empty folder using the same architecture and development process used to build this repository.

This guide assumes **no previous software development experience**.

Everything is explained one step at a time.

---

# 🎯 What You'll Build

Over the next several chapters, you'll create a complete Retrieval-Augmented Generation (RAG) application capable of:

🤖 Running a local Large Language Model

📚 Searching cybersecurity documentation

🔍 Retrieving relevant knowledge using semantic search

🧠 Generating context-aware responses

🛡️ Assisting Security Operations Center (SOC) analysts

📄 Displaying supporting source citations

💻 Running through a modern Streamlit web interface

When finished, your project will closely resemble the completed application shown in the README.

---

# 🧠 What You'll Learn

This project teaches much more than Python.

You'll gain hands-on experience with:

## 🐍 Python

- Project organization
- Virtual environments
- Package management
- Functions
- Classes
- Modules
- Error handling

---

## 🤖 Artificial Intelligence

- Large Language Models (LLMs)
- Ollama
- Prompt Engineering
- Retrieval-Augmented Generation (RAG)
- Embeddings
- Semantic Search

---

## 📚 Vector Databases

- FAISS
- Document indexing
- Similarity search
- Knowledge retrieval

---

## 🛡️ Cybersecurity

- Incident Response
- Threat Intelligence
- MITRE ATT&CK
- NIST Cybersecurity Framework
- OWASP Guidance
- Phishing Analysis

---

## 💻 Software Engineering

- Git
- GitHub
- Streamlit
- Testing
- Debugging
- Documentation
- Modular architecture

---

# 🏗️ How This Course Is Organized

This guide is divided into small chapters.

Each chapter focuses on one task.

Every chapter includes:

🎯 Objective

📖 Explanation

🛠️ Hands-on steps

💡 Tips

⚠️ Common mistakes

🧪 Verification

✅ Checkpoint

This approach makes the project easier to understand and helps you build confidence as you progress.

---

# 🗺️ Project Roadmap

Here's what we'll build together.

```text
Chapter 1
Welcome

        ↓

Chapter 2
Understanding the Project

        ↓

Chapter 3
Creating the Folder Structure

        ↓

Chapter 4
Creating requirements.txt

        ↓

Chapter 5
Installing Dependencies

        ↓

Chapter 6
Building the Backend

        ↓

Chapter 7
Loading PDF Documents

        ↓

Chapter 8
Text Chunking

        ↓

Chapter 9
Generating Embeddings

        ↓

Chapter 10
Creating the Vector Database

        ↓

Chapter 11
Building the RAG Engine

        ↓

Chapter 12
Connecting Ollama

        ↓

Chapter 13
Building the Streamlit Interface

        ↓

Chapter 14
Testing Everything

        ↓

Chapter 15
Running the Finished Application
```

---

# 🧩 Before We Begin

Software projects can sometimes feel overwhelming because they contain many files working together.

Don't worry.

You are **not expected to understand everything immediately**.

Instead, we'll build one small piece at a time.

Think of this project like assembling a puzzle.

Each chapter adds another piece until the final application comes together.

---

# 📁 What You're Starting With

At this point, your project folder should be completely empty.

There should be:

- ❌ No Python files
- ❌ No folders
- ❌ No requirements.txt
- ❌ No application code

We're going to create everything ourselves.

---

# 🎓 Learning Philosophy

There are two ways to learn programming.

### Method 1

Copy and paste code without understanding it.

You'll finish quickly.

You'll also forget most of it.

---

### Method 2

Understand what every file does.

Understand why every command is used.

Understand how each component communicates with the others.

You'll move more slowly.

But you'll finish with knowledge you can apply to future projects.

This guide follows **Method 2**.

The goal isn't simply to build software.

The goal is to understand how modern AI applications are designed.

---

# ✅ Checkpoint

Before moving to Chapter 2, make sure you understand:

✔️ The goal of this project

✔️ What Retrieval-Augmented Generation (RAG) is

✔️ The technologies you'll be using

✔️ That you'll be building the application one component at a time

If you're ready, continue to **Chapter 2 – Understanding the AI SOC Analyst Assistant Architecture**.

---

## 🎉 Congratulations!

You've officially begun building your own AI-powered cybersecurity assistant from scratch.

Let's get started.

---

# 🏗️ Chapter 2 – Understanding the AI SOC Analyst Assistant Architecture

> **Objective:** Understand how every major component of the application works together before building it.

---

# 🤔 Why Learn the Architecture First?

Imagine someone handed you the engine, doors, wheels, and seats of a car.

Could you build the car without knowing what each part does?

Probably not.

Software development works the same way.

Before creating files and writing code, it's important to understand how the finished application is organized.

Once you understand the "big picture," every file you create later will have a clear purpose.

---

# 🧠 What Is an AI Application?

An Artificial Intelligence application is simply a software program that uses one or more AI models to perform tasks that normally require human intelligence.

Examples include:

- 💬 Chatbots
- 🌎 Language translation
- 📷 Image recognition
- 🎵 Music generation
- 🛡️ Cybersecurity assistants

Your project falls into the final category.

The AI SOC Analyst Assistant combines artificial intelligence with cybersecurity knowledge to answer questions using trusted documentation.

---

# 📚 What Is Retrieval-Augmented Generation (RAG)?

Traditional AI models answer questions using only the knowledge they learned during training.

That works well for general questions, but it has an important limitation:

❌ The model cannot instantly learn new information.

❌ It may provide inaccurate or unsupported answers.

❌ It may "hallucinate" by confidently generating incorrect information.

Retrieval-Augmented Generation (RAG) solves this problem.

Instead of answering immediately, the application first searches a trusted knowledge base.

The retrieved information is then passed to the AI model as context.

The model uses that context to generate a more accurate response.

---

# 🔄 How RAG Works

```text
User asks a question
          │
          ▼
Application searches documents
          │
          ▼
Most relevant information is retrieved
          │
          ▼
Retrieved information is sent to the AI
          │
          ▼
AI generates a grounded response
          │
          ▼
Answer is displayed to the user
```

Instead of relying only on memory, the model answers using real documentation.

---

# 🏛️ High-Level Architecture

The completed project contains several major components.

Each one performs a specific job.

```text
                    User
                      │
                      ▼
          Streamlit Web Interface
                      │
                      ▼
               RAG Processing Engine
             ┌──────────┴──────────┐
             ▼                     ▼
      FAISS Vector Search     Ollama LLM
             │                     │
             ▼                     ▼
 Cybersecurity Documents     AI Response
             └──────────┬──────────┘
                        ▼
               Final Answer + Sources
```

Every question follows this path.

---

# 📂 Component 1 – Frontend

The frontend is the part of the application users interact with.

In this project, the frontend is built with **Streamlit**.

It is responsible for:

- Displaying the user interface
- Accepting questions
- Showing AI responses
- Displaying supporting citations

Think of the frontend as the application's "face."

---

# ⚙️ Component 2 – Backend

The backend performs the actual work.

It:

- Loads documents
- Splits text into chunks
- Creates embeddings
- Searches the vector database
- Communicates with Ollama
- Builds prompts
- Returns responses

Users never interact directly with the backend, but it powers the entire application.

---

# 📄 Component 3 – Knowledge Base

The knowledge base contains trusted cybersecurity documents.

Examples include:

- MITRE ATT&CK
- NIST Cybersecurity Framework
- OWASP guidance
- Incident response playbooks
- Password security recommendations

These documents become the source of truth for the AI assistant.

---

# ✂️ Component 4 – Text Chunking

Large documents cannot be searched efficiently in their original form.

Instead, documents are divided into smaller pieces called **chunks**.

For example:

```text
Original Document

50 pages

↓

Split into

Chunk 1

Chunk 2

Chunk 3

...

Chunk 400
```

Searching hundreds of small chunks is much faster than searching one large document.

---

# 🧠 Component 5 – Embeddings

Computers cannot understand text the way humans do.

Instead, text is converted into numerical representations called **embeddings**.

An embedding captures the meaning of a piece of text.

For example:

```text
"Reset your password"

↓

[0.142, -0.387, 0.901, ...]
```

Although the numbers are difficult for humans to interpret, they allow the computer to compare the meanings of different pieces of text.

---

# 📚 Component 6 – FAISS Vector Database

Once embeddings are created, they are stored in a vector database.

This project uses **FAISS**.

Instead of searching words, FAISS searches meanings.

For example:

User asks:

> "How do I respond to a phishing email?"

FAISS doesn't search only for the word "phishing."

It searches for document chunks with similar meaning.

This makes retrieval faster and more accurate.

---

# 🤖 Component 7 – Ollama

Ollama runs the Large Language Model locally on your computer.

In this project, Ollama is responsible for:

- Reading the retrieved context
- Understanding the user's question
- Generating a natural language response

Because Ollama runs locally:

- 🔒 Your data stays on your machine.
- 💲 No API fees are required.
- 🌐 The project can run offline after setup.

---

# 🧩 Component 8 – The RAG Engine

The RAG Engine is the "brain" that coordinates everything.

It performs the following steps:

1. Receives the user's question.
2. Converts the question into an embedding.
3. Searches FAISS for relevant document chunks.
4. Builds a prompt using the retrieved information.
5. Sends the prompt to Ollama.
6. Receives the AI-generated response.
7. Returns the response to the frontend.

Without the RAG Engine, the individual components would not work together.

---

# 📁 How the Project Is Organized

The project is divided into folders so each part has a clear responsibility.

```text
AI-SOC-Assistant/

backend/
    Core application logic

frontend/
    Streamlit interface

knowledge_base/
    Documents and vector indexes

tests/
    Automated tests

docs/
    Documentation

screenshots/
    Images used in the README

evaluation/
    Project evaluation files

data/
    Supporting project data
```

Organizing projects this way makes them easier to understand, maintain, and expand.

---

# 🎯 Key Takeaways

By now, you should understand that:

- ✅ The frontend is what users interact with.
- ✅ The backend performs the application's work.
- ✅ Documents become the knowledge base.
- ✅ Documents are split into chunks.
- ✅ Chunks are converted into embeddings.
- ✅ Embeddings are stored in FAISS.
- ✅ Ollama generates the final response.
- ✅ The RAG Engine connects every component together.

---

# 🧪 Knowledge Check

Before moving on, ask yourself:

- Can I explain what the frontend does?
- Can I explain what the backend does?
- Do I understand why documents are split into chunks?
- Do I understand why embeddings are needed?
- Can I explain the purpose of FAISS?
- Can I explain why Ollama is used?
- Can I describe the journey of a user's question through the system?

If you answered "yes" to most of these questions, you're ready to begin building the project.

---

# ✅ Checkpoint

Congratulations!

You now understand the overall architecture of the AI SOC Analyst Assistant.

In the next chapter, you'll create the project's folder structure from an empty directory and begin laying the foundation for the application.

---

# 🏗️ Chapter 3 – Creating the Project Structure

> **Objective:** Create the folder structure and starter files that will serve as the foundation of the AI SOC Analyst Assistant.

---

# 🎯 Why Project Structure Matters

Imagine trying to build a house without deciding where the kitchen, bedrooms, or bathroom belong.

The result would be confusing and difficult to maintain.

Software projects work the same way.

A well-organized project:

- 📂 Makes files easy to find.
- 🤝 Helps multiple developers collaborate.
- 🐞 Makes debugging easier.
- 📈 Makes future improvements easier.
- 📖 Makes the project easier for others to understand.

Before writing any code, we'll organize the project into logical folders.

---

# 🛠️ Step 1 – Open Visual Studio Code

1. Open **Visual Studio Code**.
2. Wait for the application to fully load.

If this is your first time using VS Code, don't worry. We'll explain everything as we go.

---

# 📂 Step 2 – Open Your Project Folder

Click:

**File → Open Folder...**

Navigate to your project location.

Example:

```text
C:\Capstone\Projects\
```

Select:

```text
AI-SOC-Assistant
```

Click:

**Select Folder**

Your Explorer panel should now be empty because we're building the project from scratch.

---

# 📁 Step 3 – Create the Main Folders

In the Explorer panel:

1. Right-click **AI-SOC-Assistant**
2. Select **New Folder**

Create the following folders one at a time.

```text
backend
```

```text
frontend
```

```text
knowledge_base
```

```text
tests
```

```text
docs
```

```text
screenshots
```

```text
evaluation
```

```text
data
```

Take your time.

Double-check the spelling of every folder.

Python is case-sensitive on many operating systems, so folder names should match exactly.

---

# 📂 Your Project Should Now Look Like This

```text
AI-SOC-Assistant/
│
├── backend/
├── frontend/
├── knowledge_base/
├── tests/
├── docs/
├── screenshots/
├── evaluation/
└── data/
```

If your folders match the structure above, you're ready to continue.

---

# 📄 Step 4 – Create the Root Files

Now we'll create the files that live in the root of the project.

Right-click **AI-SOC-Assistant**

Select:

**New File**

Create each file below.

---

## README.md

```text
README.md
```

This file introduces the project.

You've already created this during the documentation phase.

---

## requirements.txt

```text
requirements.txt
```

This file will contain every Python package required for the project.

We'll fill it in during a later chapter.

---

## .gitignore

```text
.gitignore
```

This tells Git which files should not be uploaded to GitHub.

Examples include:

- Virtual environments
- Python cache files
- Temporary files
- Large AI model caches

---

## app.py

```text
app.py
```

This will become one of the application's main entry points.

---

## dashboard.py

```text
dashboard.py
```

This file will help launch and organize the user interface.

---

# 📂 Step 5 – Create the Backend Files

Open the **backend** folder.

Right-click.

Choose:

**New File**

Create the following files.

```text
document_loader.py
```

```text
text_chunker.py
```

```text
embedding_generator.py
```

```text
vector_store.py
```

```text
ollama_client.py
```

```text
prompts.py
```

```text
rag_engine.py
```

```text
rag_models.py
```

```text
email_parser.py
```

```text
ioc_extractor.py
```

```text
phishing_analyzer.py
```

```text
phishing_engine.py
```

```text
threat_intelligence.py
```

Don't worry that they're empty.

We'll build each one later.

---

# 🖥️ Step 6 – Create the Frontend Files

Open the **frontend** folder.

Create:

```text
streamlit_app.py
```

This file will contain the Streamlit user interface.

---

# 📚 Step 7 – Create the Knowledge Base Structure

Open:

```text
knowledge_base
```

Create two folders.

```text
documents
```

```text
indexes
```

The completed structure should look like:

```text
knowledge_base/

├── documents/
└── indexes/
```

---

# 🧪 Step 8 – Create the Test Structure

Open:

```text
tests
```

Create the following files.

```text
test_document_loader.py
```

```text
test_text_chunker.py
```

```text
test_vector_store.py
```

```text
test_rag_engine.py
```

```text
test_phishing.py
```

We'll write these tests after the application is complete.

---

# 📸 Step 9 – Prepare the Screenshot Folder

Open:

```text
screenshots
```

You don't need to add anything yet.

Later you'll store screenshots such as:

- Dashboard
- RAG Responses
- Pytest Results
- Ollama
- Source Citations

These will be displayed in the README.

---

# 📁 Final Project Structure

If you've followed every step, your project should now resemble:

```text
AI-SOC-Assistant/

backend/
│
├── document_loader.py
├── text_chunker.py
├── embedding_generator.py
├── vector_store.py
├── ollama_client.py
├── prompts.py
├── rag_engine.py
├── rag_models.py
├── email_parser.py
├── ioc_extractor.py
├── phishing_analyzer.py
├── phishing_engine.py
└── threat_intelligence.py

frontend/
│
└── streamlit_app.py

knowledge_base/
│
├── documents/
└── indexes/

tests/
│
├── test_document_loader.py
├── test_text_chunker.py
├── test_vector_store.py
├── test_rag_engine.py
└── test_phishing.py

docs/

screenshots/

evaluation/

data/

README.md
requirements.txt
.gitignore
app.py
dashboard.py
```

---

# 💡 Why We Created Empty Files

Some beginners wonder why we're creating files before writing code.

There are several reasons:

- It helps visualize the complete application.
- It makes navigation easier.
- It encourages thinking in modules rather than one large script.
- It mirrors how professional software projects are organized.

Later, we'll fill each file with code one at a time.

---

# 🧪 Knowledge Check

Before moving on, ask yourself:

- Can I explain why we separate the frontend and backend?
- Do I understand why we created a `knowledge_base` folder?
- Why are tests stored in their own directory?
- Why is documentation separate from source code?

If you can answer these questions, you're ready for the next chapter.

---

# ✅ Checkpoint

🎉 Congratulations!

You've created the complete project skeleton for the AI SOC Analyst Assistant.

Although every file is currently empty, you've built the same professional structure used by the finished application.

In the next chapter, we'll create the project's `requirements.txt` file and learn how Python dependencies are managed.

---

# 📦 Chapter 4 – Creating the `requirements.txt` File

> **Objective:** Learn what Python dependencies are, why they're important, and create the `requirements.txt` file that will allow anyone to install the software needed for this project.

---

# 🤔 What Is a Dependency?

Imagine you're building a house.

Instead of making every brick, nail, window, and door yourself, you purchase them from companies that specialize in making those materials.

Software development works the same way.

Rather than writing every feature from scratch, developers use **libraries** created by other programmers.

These libraries are called **dependencies** because your project depends on them to function correctly.

---

# 📖 What Is `requirements.txt`?

The `requirements.txt` file is simply a list of every Python package your project requires.

When someone downloads your project, they don't need to manually search for every library.

Instead, Python reads this file and installs everything automatically.

Without this file:

❌ Readers would have to guess which packages are required.

❌ Different computers might install different versions.

❌ The project could fail because of missing libraries.

For these reasons, almost every professional Python project includes a `requirements.txt` file.

---

# 📂 Locate the File

In Visual Studio Code, locate the file you created earlier.

```text
AI-SOC-Assistant/

requirements.txt
```

If you don't see it, create it now by:

1. Right-clicking the project root.
2. Selecting **New File**.
3. Naming the file:

```text
requirements.txt
```

---

# ✏️ Add the Project Dependencies

Open `requirements.txt`.

Replace its contents with the following:

```text
streamlit
ollama
sentence-transformers
faiss-cpu
PyMuPDF
langchain
langchain-community
langchain-core
langchain-text-splitters
numpy
pandas
scikit-learn
pytest
python-dotenv
tqdm
```

Save the file.

---

# 📚 What Does Each Package Do?

Let's briefly examine each dependency.

| Package | Purpose |
|---------|---------|
| streamlit | Builds the web interface |
| ollama | Communicates with the local AI model |
| sentence-transformers | Creates text embeddings |
| faiss-cpu | Stores and searches vectors |
| PyMuPDF | Reads PDF documents |
| langchain | AI workflow utilities |
| langchain-community | Community integrations |
| langchain-core | Core LangChain functionality |
| langchain-text-splitters | Splits documents into chunks |
| numpy | Numerical computing |
| pandas | Data processing |
| scikit-learn | Machine learning utilities |
| pytest | Automated testing |
| python-dotenv | Reads environment variables |
| tqdm | Displays progress bars |

Notice that each library has a specific responsibility.

Professional software is built by combining specialized tools rather than reinventing everything from scratch.

---

# ⚠️ Why Don't We Include Python?

You might notice that Python itself is not listed.

That's because Python is the programming language used to run the project.

The packages listed in `requirements.txt` are installed **inside** Python.

---

# 🧠 Understanding Version Numbers

Sometimes you'll see dependencies written like this:

```text
streamlit==1.44.0
```

or

```text
numpy>=2.0.0
```

These specify exact or minimum versions.

For this educational project, we're using package names only to keep the file simple and readable.

As your projects grow, you may choose to pin specific versions for consistent behavior across different systems.

---

# 💻 How Python Uses This File

Later, you'll install every dependency with a single command:

```bash
pip install -r requirements.txt
```

Here's what happens:

1. Python opens `requirements.txt`.
2. It reads each package name.
3. It downloads the package from the Python Package Index (PyPI).
4. It installs the package into your virtual environment.
5. Your project becomes ready to run.

This is one of the reasons Python projects are easy to share.

---

# 🧪 Verification

Your completed `requirements.txt` should look similar to this:

```text
streamlit
ollama
sentence-transformers
faiss-cpu
PyMuPDF
langchain
langchain-community
langchain-core
langchain-text-splitters
numpy
pandas
scikit-learn
pytest
python-dotenv
tqdm
```

If your file matches the example above, you've completed this chapter successfully.

---

# 💡 Pro Tip

As you continue developing software, you'll likely install additional libraries.

Whenever you add a new dependency to your project, remember to update `requirements.txt`.

Doing so ensures that anyone else working with your project can install the same tools and reproduce your results.

---

# 🧪 Knowledge Check

Before moving on, ask yourself:

- What is a dependency?
- Why is `requirements.txt` important?
- Why don't we list Python itself?
- Which package creates embeddings?
- Which package builds the web interface?
- Which package reads PDF documents?
- Which package performs vector search?

If you can answer these questions, you're ready to continue.

---

# ✅ Checkpoint

🎉 Congratulations!

You've created one of the most important files in the project.

Although it contains only a short list of package names, `requirements.txt` makes your application reproducible and easy to share with other developers.

In the next chapter, you'll create a Python virtual environment and install every dependency needed to begin writing the application's code.

---

# 🐍 Chapter 5 – Creating a Python Virtual Environment

> **Objective:** Learn what a Python virtual environment is, why every professional Python project uses one, create your own virtual environment, and install the project's dependencies.

---

# 🤔 What Is a Virtual Environment?

Imagine you own several different cars.

Each car uses a different key.

The key for one car doesn't work on another.

A Python virtual environment works in a similar way.

Instead of every project sharing the same Python packages, each project gets its own isolated environment.

This prevents one project's packages from interfering with another project's packages.

---

# 🧠 Why Do We Need One?

Without a virtual environment:

❌ Installing a package for one project installs it for every project.

❌ Different projects may require different package versions.

❌ Updating one library can accidentally break another project.

Using a virtual environment keeps each project self-contained and predictable.

---

# 📁 What Will Happen?

By the end of this chapter, your project will contain a new folder called:

```text
.venv
```

This folder contains your isolated Python environment.

> ⚠️ **Important:** Never upload the `.venv` folder to GitHub. It should already be excluded by your `.gitignore` file.

---

# 🛠️ Step 1 – Open the Terminal

Inside Visual Studio Code:

1. Click **Terminal** on the top menu.
2. Select **New Terminal**.

A terminal window should appear near the bottom of the screen.

It should display something similar to:

```powershell
PS C:\Capstone\Projects\AI-SOC-Assistant>
```

---

# 🛠️ Step 2 – Verify Python Is Installed

Type the following command:

```powershell
python --version
```

Press **Enter**.

If Python is installed correctly, you'll see something similar to:

```text
Python 3.13.x
```

> 💡 Your version number may differ slightly.

---

# ⚠️ Troubleshooting

### Problem

```text
'python' is not recognized as an internal or external command...
```

### Solution

Python is either:

- Not installed
- Not added to your system's PATH

Return to **Part A** and reinstall Python, making sure **"Add Python to PATH"** is selected during installation.

---

# 🛠️ Step 3 – Create the Virtual Environment

While still inside the project folder, type:

```powershell
python -m venv .venv
```

Press **Enter**.

Python will create a new folder named:

```text
.venv
```

This may take a few moments.

---

# 📂 Your Project Should Now Look Like This

```text
AI-SOC-Assistant/

.venv/

backend/

frontend/

knowledge_base/

tests/

README.md

requirements.txt
```

Don't worry if you don't see `.venv` immediately.

VS Code may take a moment to refresh.

---

# 🛠️ Step 4 – Activate the Virtual Environment

Because this guide targets Windows, run:

```powershell
.venv\Scripts\activate
```

Press **Enter**.

---

# ✅ Successful Activation

If activation succeeds, your terminal prompt will change.

Example:

```powershell
(.venv) PS C:\Capstone\Projects\AI-SOC-Assistant>
```

The `(.venv)` at the beginning tells you that the virtual environment is active.

---

# ⚠️ Common Error

You may see:

```text
Running scripts is disabled on this system.
```

This is a Windows PowerShell security feature.

Run the following command:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Type:

```text
Y
```

Press **Enter**.

Now activate the virtual environment again:

```powershell
.venv\Scripts\activate
```

---

# 🛠️ Step 5 – Install the Project Dependencies

Now install every package listed in `requirements.txt`.

Type:

```powershell
pip install -r requirements.txt
```

Press **Enter**.

Python will begin downloading and installing each dependency.

This may take several minutes depending on your internet connection.

---

# 📥 What Is Happening?

Python is reading the `requirements.txt` file one line at a time.

For each package, it:

1. Searches the Python Package Index (PyPI).
2. Downloads the package.
3. Installs it into your virtual environment.

Once complete, every required library will be available to your project.

---

# ⏳ Expected Output

You'll see many messages as packages are downloaded.

Toward the end, you should see something similar to:

```text
Successfully installed
```

followed by a list of installed packages.

---

# 🛠️ Step 6 – Verify the Installation

Run:

```powershell
pip list
```

Press **Enter**.

You should see packages such as:

```text
streamlit

faiss-cpu

sentence-transformers

ollama

PyMuPDF

pytest
```

The list will be much longer than this.

---

# 💡 Why We Verify

Professional developers don't assume software installed correctly.

They verify it.

Checking installed packages now helps catch problems before writing any code.

---

# 🧪 Knowledge Check

Before moving on, ask yourself:

- What is a virtual environment?
- Why should every Python project have one?
- How do you activate the virtual environment?
- Why do we use `requirements.txt`?
- What command installs every dependency?
- How do you verify the installation?

If you can answer these questions, you're ready to continue.

---

# ✅ Checkpoint

🎉 Congratulations!

You've completed one of the most important setup tasks in the entire project.

Your development environment is now isolated, organized, and ready for coding.

Every Python file you create from this point forward will use the packages installed inside your virtual environment.

---

# ⏭️ Coming Up Next

In **Chapter 6**, you'll begin writing your first real Python module:

📄 `backend/document_loader.py`

You'll learn:

- What PDF parsing is
- How cybersecurity documents are loaded into memory
- Why document loading is the first stage of a RAG pipeline
- How to write and understand the complete `document_loader.py` module
- How to test it independently before connecting it to the rest of the application

This is where the AI SOC Analyst Assistant truly begins to come to life.

---

# 📄 Chapter 6 – Building the Document Loader

> **Objective:** Learn how Retrieval-Augmented Generation (RAG) systems read documents and build the first Python module of the AI SOC Analyst Assistant.

---

# 🤔 Why Do We Need a Document Loader?

Think about how a human studies for an exam.

Before answering questions, you first:

📚 Read the textbook

📖 Highlight important sections

🧠 Remember what you learned

Artificial Intelligence works similarly.

Before our AI can answer cybersecurity questions, it needs access to trusted documentation.

That means our application must first load those documents into memory.

This is the job of the **Document Loader**.

---

# 🧠 Where Does the Document Loader Fit?

Our RAG pipeline currently looks like this:

```text
Cybersecurity PDFs

        │

        ▼

Document Loader

        │

        ▼

Text Chunker

        │

        ▼

Embedding Generator

        │

        ▼

FAISS Vector Database

        │

        ▼

User Questions
```

Without the Document Loader, the AI has nothing to search.

---

# 📚 What Documents Will We Load?

Inside:

```text
knowledge_base/
```

Create another folder if it doesn't already exist:

```text
documents
```

Your folder should now look like:

```text
knowledge_base/

documents/

indexes/
```

This folder will contain PDFs such as:

- MITRE ATT&CK
- NIST Cybersecurity Framework
- OWASP Cheat Sheets
- Incident Response Playbooks
- Password Guidelines

These become the application's knowledge base.

---

# 📄 What Is a PDF Parser?

A PDF is designed for humans to read.

Unfortunately, computers cannot directly understand PDF pages.

A **PDF parser** extracts the text from every page.

For example:

```text
Page 1

↓

"This document explains phishing attacks..."

↓

Plain Text
```

Once the text has been extracted, Python can process it.

Our project uses:

**PyMuPDF**

to perform this task.

---

# 🛠️ Create the Module

Inside:

```text
backend/
```

Open:

```text
document_loader.py
```

If the file is empty, that's expected.

We're about to write our first Python module.

---

# ✍️ Add the Following Code

```python
from pathlib import Path
import fitz


class DocumentLoader:
    """
    Loads PDF documents from the knowledge base.
    """

    def __init__(self, documents_directory):
        self.documents_directory = Path(documents_directory)

    def load_documents(self):
        documents = []

        pdf_files = self.documents_directory.glob("*.pdf")

        for pdf in pdf_files:

            document = fitz.open(pdf)

            text = ""

            for page in document:
                text += page.get_text()

            documents.append(
                {
                    "filename": pdf.name,
                    "text": text
                }
            )

        return documents
```

Save the file.

---

# 🧩 Understanding the Code

Let's examine the module piece by piece.

---

## Import Statements

```python
from pathlib import Path
```

`Path` makes it easier to work with folders and files.

Instead of manually writing file paths, Python can build them automatically.

---

```python
import fitz
```

`fitz` is PyMuPDF.

It allows Python to:

- Open PDFs
- Read pages
- Extract text

---

## The Class

```python
class DocumentLoader:
```

Instead of writing one large script, we organize our code into classes.

This makes the project:

- Easier to reuse
- Easier to test
- Easier to maintain

---

## The Constructor

```python
def __init__(...)
```

Whenever we create a DocumentLoader, Python remembers where our PDFs are stored.

---

## Finding PDFs

```python
glob("*.pdf")
```

This searches the folder for every file ending with:

```text
.pdf
```

If there are five PDFs, Python finds all five automatically.

---

## Opening the PDF

```python
fitz.open(pdf)
```

This opens one PDF at a time.

---

## Reading Pages

```python
for page in document:
```

Every PDF contains multiple pages.

Python loops through each page and extracts the text.

---

## Saving the Results

Each document becomes a dictionary.

Example:

```python
{
    "filename": "MITRE.pdf",
    "text": "Attack techniques..."
}
```

The list returned by our loader might look like:

```python
[
    {
        "filename": "MITRE.pdf",
        "text": "..."
    },
    {
        "filename": "OWASP.pdf",
        "text": "..."
    }
]
```

Later chapters will split this text into chunks.

---

# 🧪 Testing the Module

Create a temporary file in the project root named:

```text
test_loader.py
```

Add:

```python
from backend.document_loader import DocumentLoader

loader = DocumentLoader("knowledge_base/documents")

documents = loader.load_documents()

print(f"Loaded {len(documents)} documents")

for document in documents:
    print(document["filename"])
```

Save the file.

---

# ▶️ Run the Test

Open your terminal.

Run:

```powershell
python test_loader.py
```

---

# ✅ Expected Output

If your folder contains three PDFs, you should see something similar to:

```text
Loaded 3 documents

MITRE.pdf

OWASP.pdf

Incident_Response_Playbook.pdf
```

Your filenames will depend on the PDFs you've added.

---

# ⚠️ Common Errors

## Error

```text
ModuleNotFoundError: No module named 'fitz'
```

### Cause

PyMuPDF is not installed.

### Fix

Run:

```powershell
pip install PyMuPDF
```

---

## Error

```text
Loaded 0 documents
```

### Cause

The `knowledge_base/documents` folder is empty.

### Fix

Add one or more PDF files to the folder and run the test again.

---

## Error

```text
FileNotFoundError
```

### Cause

The folder path is incorrect.

Double-check that your PDFs are stored inside:

```text
knowledge_base/documents
```

---

# 🎓 What You Learned

Congratulations!

You've just written the first real module of the AI SOC Analyst Assistant.

You now understand:

✅ What a document loader does

✅ How PDFs are read into Python

✅ How text is extracted

✅ How documents are stored in memory

✅ Why document loading is the first stage of every RAG pipeline

---

# 🧪 Knowledge Check

Can you answer these questions?

- Why do RAG systems need a document loader?
- What library did we use to read PDFs?
- What does `glob("*.pdf")` do?
- What kind of object does `load_documents()` return?
- Why do we store both the filename and the extracted text?

If you can answer these questions, you're ready for the next chapter.

---

# ✅ Checkpoint

🎉 Excellent work!

The AI SOC Analyst Assistant can now read cybersecurity PDF documents into memory.

In the next chapter, you'll build the **Text Chunker**, which transforms large documents into smaller pieces that can later be converted into embeddings and searched efficiently.

---

# ✂️ Chapter 7 – Building the Text Chunker

> **Objective:** Learn why RAG systems split documents into smaller pieces and build the module responsible for chunking cybersecurity documents.

---

# 🤔 Why Can't We Search Entire Documents?

Imagine someone asks:

> "What is spear phishing?"

Now imagine your knowledge base contains:

- 📄 MITRE ATT&CK (350 pages)
- 📄 NIST Cybersecurity Framework (200 pages)
- 📄 OWASP Top 10 (150 pages)
- 📄 Incident Response Guide (75 pages)

Would it make sense to send **all 775 pages** to the AI every time someone asks a question?

❌ No.

Large Language Models have limits on how much text they can process at once.

Even if they didn't, sending hundreds of pages would:

- Be slower
- Cost more memory
- Reduce answer quality
- Introduce irrelevant information

Instead, we divide documents into smaller sections called **chunks**.

---

# 📚 What Is a Chunk?

A chunk is simply a small section of a larger document.

For example:

```text
Original PDF

Page 1
Page 2
Page 3
Page 4
Page 5

↓

Chunk 1

Chunk 2

Chunk 3

Chunk 4

Chunk 5
```

Instead of searching five pages together, we search many smaller pieces.

---

# 🧠 Why Does Chunking Improve AI?

Suppose a user asks:

> "How do I respond to a phishing email?"

The answer may only exist in one small paragraph.

Instead of sending the AI:

📚 Entire Book

We send:

📄 One relevant chunk

This keeps the response focused and accurate.

---

# 🔄 Where Does Chunking Fit?

Our pipeline now looks like this:

```text
PDF Documents

↓

Document Loader

↓

Text Chunker

↓

Embedding Generator

↓

FAISS Vector Database

↓

User Question

↓

AI Response
```

The Text Chunker is the second stage of the RAG pipeline.

---

# 📄 Open the Module

Inside:

```text
backend/
```

Open:

```text
text_chunker.py
```

---

# ✍️ Replace the File with the Following Code

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextChunker:
    """
    Splits documents into smaller chunks for retrieval.
    """

    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

    def chunk_documents(self, documents):
        chunks = []

        for document in documents:

            split_text = self.splitter.split_text(document["text"])

            for chunk in split_text:

                chunks.append(
                    {
                        "filename": document["filename"],
                        "text": chunk
                    }
                )

        return chunks
```

Save the file.

---

# 🔍 Understanding the Code

Let's break it down.

---

## Import Statement

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
```

LangChain already provides an excellent text splitter.

Instead of writing our own algorithm, we reuse a well-tested library.

---

## Creating the Class

```python
class TextChunker:
```

This class has one responsibility:

Split documents into smaller pieces.

Following the **Single Responsibility Principle** makes the code easier to understand and maintain.

---

## The Constructor

```python
chunk_size=1000
```

Each chunk can contain approximately **1,000 characters**.

---

```python
chunk_overlap=200
```

Notice we don't simply split documents into separate blocks.

Instead, chunks overlap slightly.

Example:

```text
Chunk 1

AAAAAAAAAA
BBBBBBBBBB
CCCCCCCCCC

Chunk 2

CCCCCCCCCC
DDDDDDDDDD
EEEEEEEEEE
```

The repeated section helps preserve context.

Without overlap, important ideas could be split between two chunks and lose meaning.

---

## Splitting Documents

```python
split_text(document["text"])
```

LangChain automatically divides the text into appropriately sized chunks.

This saves us from writing our own splitting logic.

---

## Creating Chunk Objects

Every chunk becomes a dictionary.

Example:

```python
{
    "filename": "MITRE.pdf",
    "text": "Spear phishing is..."
}
```

Notice we preserve the filename.

Later, this allows us to cite the original document that contained the answer.

---

# 🧪 Testing the Chunker

Create a temporary file named:

```text
test_chunker.py
```

Add:

```python
from backend.document_loader import DocumentLoader
from backend.text_chunker import TextChunker

loader = DocumentLoader("knowledge_base/documents")
documents = loader.load_documents()

chunker = TextChunker()

chunks = chunker.chunk_documents(documents)

print(f"Loaded {len(documents)} documents")

print(f"Created {len(chunks)} chunks")
```

Save the file.

---

# ▶️ Run the Test

Open your terminal.

Run:

```powershell
python test_chunker.py
```

---

# ✅ Expected Output

You should see something similar to:

```text
Loaded 4 documents

Created 217 chunks
```

The exact number will depend on:

- Number of PDFs
- Size of the PDFs
- Chunk size
- Chunk overlap

Don't worry if your numbers differ.

---

# 💡 Why We Preserve the Filename

Every chunk stores:

```python
filename

text
```

Later, when the AI answers a question, it can tell the user:

> "This answer came from the NIST Cybersecurity Framework."

Without storing the filename, source citations would be impossible.

---

# ⚠️ Common Errors

## Error

```text
ModuleNotFoundError
```

### Fix

Verify that LangChain was installed correctly.

Run:

```powershell
pip install langchain-text-splitters
```

---

## Error

```text
Created 0 chunks
```

### Cause

No documents were loaded.

Verify:

```text
knowledge_base/documents
```

contains one or more PDF files.

---

## Error

```text
KeyError: text
```

### Cause

The Document Loader isn't returning dictionaries with a `"text"` key.

Double-check the previous chapter before continuing.

---

# 📚 Real-World Example

Imagine a cybersecurity document contains this paragraph:

```text
Phishing attacks attempt to trick users into revealing sensitive information through deceptive emails.
```

Instead of storing the entire document, we store only this section as one searchable chunk.

When a user later asks:

> "What is phishing?"

FAISS can retrieve this chunk almost instantly.

---

# 🎓 What You Learned

Congratulations!

You've now built the second stage of the RAG pipeline.

You understand:

- ✅ Why chunking is necessary
- ✅ Why chunk overlap improves retrieval
- ✅ How LangChain splits text
- ✅ Why chunks retain filenames
- ✅ How chunks prepare documents for embeddings

---

# 🧪 Knowledge Check

Can you answer these questions?

- Why don't RAG systems search entire books?
- What is a chunk?
- Why do chunks overlap?
- Why do we store the filename?
- What package performs the chunking?
- What does `chunk_size` control?

If you answered yes to these questions, you're ready to continue.

---

# ✅ Checkpoint

🎉 Excellent work!

The AI SOC Analyst Assistant can now:

- Read PDF documents
- Extract their text
- Split the text into searchable chunks

In the next chapter, you'll build the **Embedding Generator**, where these chunks will be converted into numerical vectors that computers can understand and compare.

---

# 🧠 Chapter 8 – Building the Embedding Generator

> **Objective:** Learn what embeddings are, why they are essential to Retrieval-Augmented Generation (RAG), and build the module that converts document chunks into searchable vectors.

---

# 🤔 What Is an Embedding?

Humans understand words by their meaning.

For example:

> Password

and

> Credentials

are different words, but they are closely related.

A computer doesn't naturally understand this relationship.

To a computer, words are simply characters.

```
P a s s w o r d
```

or

```
C r e d e n t i a l s
```

To allow computers to compare meanings, we convert text into numbers.

These numerical representations are called **embeddings**.

---

# 📚 Think of an Embedding Like GPS Coordinates

Imagine two cities.

```
New York

↓

40.7128° N
74.0060° W
```

Those coordinates tell us exactly where New York is.

Embeddings work similarly.

Instead of representing a location on Earth, they represent the meaning of text in a mathematical space.

Example:

```
"Reset your password"

↓

[-0.217, 0.894, 0.153, ...]
```

Those numbers may look meaningless to us, but they allow the computer to compare ideas.

---

# 🧠 Why Are Embeddings Important?

Imagine the user asks:

> "How do I protect my login credentials?"

Your cybersecurity documentation might contain:

> "Users should create strong passwords."

Notice something?

The words are different.

```
login credentials

≠

password
```

A normal keyword search might miss this.

Embeddings allow the computer to recognize that the two ideas are closely related.

Instead of searching words...

...we search **meaning**.

---

# 🔄 Where Does This Fit in the RAG Pipeline?

Our pipeline now looks like this:

```
PDF Documents

↓

Document Loader

↓

Text Chunker

↓

Embedding Generator

↓

FAISS Vector Database

↓

User Question

↓

AI Response
```

The Embedding Generator transforms every chunk into a vector that FAISS can search.

---

# 🤖 Which Embedding Model Are We Using?

This project uses the following model from Sentence Transformers:

```
all-MiniLM-L6-v2
```

This model is:

- ✅ Fast
- ✅ Lightweight
- ✅ Accurate
- ✅ Popular for semantic search
- ✅ Excellent for educational RAG applications

---

# 📄 Open the Module

Inside:

```
backend/
```

Open:

```
embedding_generator.py
```

---

# ✍️ Replace the File with the Following Code

```python
from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:
    """
    Generates vector embeddings for document chunks.
    """

    def __init__(self):
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def generate_embeddings(self, chunks):
        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        embeddings = self.model.encode(
            texts,
            show_progress_bar=True
        )

        return embeddings
```

Save the file.

---

# 🔍 Understanding the Code

Let's examine each part.

---

## Import Statement

```python
from sentence_transformers import SentenceTransformer
```

This imports the Sentence Transformers library.

Its job is to convert human language into embeddings.

---

## Loading the Model

```python
SentenceTransformer(
    "all-MiniLM-L6-v2"
)
```

The first time this runs, Python downloads the model.

After that, it loads from your computer.

---

## Preparing the Text

```python
texts = [
    chunk["text"]
    for chunk in chunks
]
```

Our chunk objects contain:

```python
{
    "filename": "...",
    "text": "..."
}
```

The embedding model only needs the text.

So we extract every chunk's text into a list.

---

## Generating Embeddings

```python
self.model.encode(...)
```

This converts every chunk into a numerical vector.

For example:

```
Chunk 1

↓

Vector 1

Chunk 2

↓

Vector 2

Chunk 3

↓

Vector 3
```

---

# 📊 What Does an Embedding Look Like?

One embedding might begin like this:

```
[
0.143,
-0.552,
0.816,
...
]
```

The actual vector contains hundreds of numbers.

Humans cannot interpret them directly.

Computers use them to calculate similarity.

---

# 🧪 Testing the Module

Create a temporary file:

```
test_embeddings.py
```

Add:

```python
from backend.document_loader import DocumentLoader
from backend.text_chunker import TextChunker
from backend.embedding_generator import EmbeddingGenerator

loader = DocumentLoader(
    "knowledge_base/documents"
)

documents = loader.load_documents()

chunker = TextChunker()

chunks = chunker.chunk_documents(documents)

generator = EmbeddingGenerator()

embeddings = generator.generate_embeddings(
    chunks
)

print(f"Chunks: {len(chunks)}")

print(f"Embeddings: {len(embeddings)}")

print(embeddings[0])
```

Save the file.

---

# ▶️ Run the Test

Open the terminal.

Run:

```powershell
python test_embeddings.py
```

---

# ✅ Expected Output

```
Chunks: 217

Embeddings: 217

[0.1823, -0.5172, ...]
```

Your numbers will be different.

That's perfectly normal.

---

# 💡 Why Is There One Embedding Per Chunk?

Every chunk represents one idea.

Every idea gets one embedding.

Example:

```
Chunk

↓

Embedding

↓

Stored in FAISS
```

Later, when someone asks a question...

The user's question also becomes an embedding.

FAISS compares the vectors.

The closest vectors are returned.

---

# ⚠️ Common Errors

## Error

```
ModuleNotFoundError:
sentence_transformers
```

### Solution

Run:

```powershell
pip install sentence-transformers
```

---

## Error

```
No module named torch
```

PyTorch was not installed correctly.

Run:

```powershell
pip install torch
```

---

## Error

```
Downloading model...
```

This is normal.

The model downloads only the first time.

Later runs load it locally.

---

# 🧠 Fun Fact

The embedding model doesn't understand cybersecurity.

It understands language.

That's why we combine it with:

- MITRE ATT&CK
- OWASP
- NIST
- Incident Response documents

Together they create a cybersecurity-specific RAG system.

---

# 🎓 What You Learned

Congratulations!

You've now built the third stage of the RAG pipeline.

You understand:

- ✅ What embeddings are
- ✅ Why embeddings are numerical vectors
- ✅ Why semantic search is better than keyword search
- ✅ How Sentence Transformers generates embeddings
- ✅ Why every chunk becomes one embedding

---

# 🧪 Knowledge Check

Can you answer these questions?

- What is an embedding?
- Why can't computers search meaning without embeddings?
- Why is semantic search better than keyword search?
- Which model are we using?
- Why does every chunk receive its own embedding?

If you answered yes, you're ready to continue.

---

# ✅ Checkpoint

🎉 Outstanding!

Your AI SOC Analyst Assistant can now:

✅ Read PDF documents

✅ Split them into chunks

✅ Convert every chunk into a searchable vector representation

In the next chapter, you'll build the **FAISS Vector Store**, where these embeddings will be indexed for lightning-fast semantic search.

---

# ⚡ Chapter 9 – Building the FAISS Vector Store

> **Objective:** Learn what a vector database is, why it is needed, and build the FAISS Vector Store that powers semantic search in the AI SOC Analyst Assistant.

---

# 🤔 What Is a Vector Database?

Imagine you have a library with **100,000 books**.

Someone walks in and asks:

> "Where can I learn about ransomware recovery?"

Would you read every book from beginning to end?

Of course not.

Instead, you'd use the library's catalog to quickly locate the most relevant books.

A **vector database** works the same way.

Instead of searching through every document manually, it quickly finds the document chunks whose meanings are most similar to the user's question.

---

# 📚 Why Can't We Just Use a Python List?

Suppose our project has:

- 50 PDFs
- 15,000 text chunks
- 15,000 embeddings

Every time someone asks a question, Python would need to compare that question against all 15,000 embeddings.

That approach works for tiny projects but becomes painfully slow as the knowledge base grows.

FAISS is optimized to perform these comparisons much faster.

---

# 🧠 What Is FAISS?

**FAISS** stands for:

> **Facebook AI Similarity Search**

It was developed by Meta AI to efficiently search large collections of vector embeddings.

Instead of comparing every vector one at a time, FAISS uses specialized indexing techniques to retrieve the closest matches in milliseconds.

---

# 🔄 Where Does FAISS Fit?

Our pipeline now looks like this:

```text
PDF Documents

↓

Document Loader

↓

Text Chunker

↓

Embedding Generator

↓

FAISS Vector Store

↓

Relevant Chunks

↓

Ollama

↓

Final AI Response
```

---

# 📁 Open the Module

Inside the **backend** folder, open:

```text
vector_store.py
```

Replace the contents with the following code.

---

# ✍️ Add the Following Code

```python
import faiss
import numpy as np
import pickle
from pathlib import Path


class VectorStore:
    """
    Stores and searches document embeddings using FAISS.
    """

    def __init__(self):

        self.index = None
        self.chunks = []

    def build_index(self, embeddings, chunks):

        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)

        self.index.add(
            np.array(
                embeddings,
                dtype="float32"
            )
        )

        self.chunks = chunks

    def search(self, query_embedding, top_k=5):

        distances, indices = self.index.search(
            np.array(
                [query_embedding],
                dtype="float32"
            ),
            top_k
        )

        results = []

        for index in indices[0]:
            results.append(
                self.chunks[index]
            )

        return results

    def save(self, directory):

        directory = Path(directory)

        directory.mkdir(
            parents=True,
            exist_ok=True
        )

        faiss.write_index(
            self.index,
            str(directory / "faiss.index")
        )

        with open(
            directory / "chunks.pkl",
            "wb"
        ) as file:

            pickle.dump(
                self.chunks,
                file
            )

    def load(self, directory):

        directory = Path(directory)

        self.index = faiss.read_index(
            str(directory / "faiss.index")
        )

        with open(
            directory / "chunks.pkl",
            "rb"
        ) as file:

            self.chunks = pickle.load(file)
```

Save the file.

---

# 🔍 Understanding the Code

Let's break this module into smaller pieces.

---

## Import Statements

```python
import faiss
```

Imports the FAISS library.

---

```python
import numpy as np
```

FAISS expects vectors as NumPy arrays.

---

```python
import pickle
```

Pickle allows Python objects to be saved to disk.

We'll use it to save our document chunks.

---

# The Constructor

```python
self.index = None
```

Initially, no vector database exists.

We'll create it after generating embeddings.

---

```python
self.chunks = []
```

The chunks are stored separately from the vectors.

This allows us to recover the original document text after a search.

---

# Building the Index

```python
dimension = embeddings.shape[1]
```

Every embedding has the same number of dimensions.

For the model we're using:

```
384 dimensions
```

FAISS needs to know this before building the index.

---

```python
faiss.IndexFlatL2(...)
```

This creates one of FAISS's simplest index types.

It compares vectors using Euclidean distance.

For educational projects, this is an excellent choice because it is simple and accurate.

---

# Adding Embeddings

```python
self.index.add(...)
```

Every embedding is inserted into the vector database.

Once complete, FAISS can search them.

---

# Searching

```python
self.index.search(...)
```

Instead of searching words...

FAISS searches vectors.

It returns:

- distances
- indices

The indices tell us which document chunks are most similar.

---

# Saving the Database

```python
faiss.write_index(...)
```

The vector database is saved to disk.

Without this step, we'd have to regenerate embeddings every time the application starts.

---

# Saving the Chunks

Notice we also save:

```python
chunks.pkl
```

The FAISS index stores vectors.

It does **not** store the original text.

The pickle file preserves the chunks so we can display them later.

---

# Loading the Database

The `load()` method reloads both:

- the FAISS index
- the chunk data

This makes future application startups much faster.

---

# 🧪 Testing the Vector Store

Create a temporary file:

```text
test_vector_store.py
```

Add:

```python
from backend.document_loader import DocumentLoader
from backend.text_chunker import TextChunker
from backend.embedding_generator import EmbeddingGenerator
from backend.vector_store import VectorStore

loader = DocumentLoader(
    "knowledge_base/documents"
)

documents = loader.load_documents()

chunker = TextChunker()

chunks = chunker.chunk_documents(documents)

generator = EmbeddingGenerator()

embeddings = generator.generate_embeddings(chunks)

store = VectorStore()

store.build_index(
    embeddings,
    chunks
)

store.save(
    "knowledge_base/indexes"
)

print("Vector database created successfully!")
```

Save the file.

---

# ▶️ Run the Test

Open the terminal.

Run:

```powershell
python test_vector_store.py
```

---

# ✅ Expected Output

```text
Vector database created successfully!
```

Inside:

```text
knowledge_base/indexes/
```

You should now see:

```text
faiss.index

chunks.pkl
```

Congratulations!

You have built your first searchable vector database.

---

# ⚠️ Common Errors

## Error

```text
ModuleNotFoundError:
faiss
```

Run:

```powershell
pip install faiss-cpu
```

---

## Error

```text
AttributeError:
shape
```

This usually means your embeddings are not a NumPy array.

Verify that the Embedding Generator returned embeddings correctly before calling `build_index()`.

---

## Error

```text
FileNotFoundError
```

Check that the `knowledge_base/indexes` folder exists or let the `save()` method create it automatically.

---

# 📊 How the Search Works

Imagine your knowledge base contains 5,000 chunks.

A user asks:

> "What is privilege escalation?"

The question is converted into an embedding.

FAISS compares that embedding against all stored vectors and quickly returns the closest matches.

Only those relevant chunks are sent to Ollama.

This makes the AI faster and more accurate.

---

# 🎓 What You Learned

Congratulations!

You've now built the fourth stage of the RAG pipeline.

You understand:

- ✅ What a vector database is
- ✅ Why FAISS is used
- ✅ How embeddings are indexed
- ✅ Why chunks are saved separately
- ✅ How semantic search works

---

# 🧪 Knowledge Check

Can you answer these questions?

- What problem does FAISS solve?
- Why don't we search every embedding manually?
- What does `IndexFlatL2` do?
- Why do we save both the FAISS index and the chunk data?
- What happens when a user asks a question?

If you answered yes, you're ready for the next chapter.

---

# ✅ Checkpoint

🎉 Outstanding!

Your AI SOC Analyst Assistant can now:

- 📄 Load PDF documents
- ✂️ Split them into chunks
- 🧠 Generate embeddings
- ⚡ Build a searchable FAISS vector database

In the next chapter, you'll build the **Retriever**, the component responsible for converting a user's question into an embedding and retrieving the most relevant document chunks before the AI generates a response.

---

# 🔍 Chapter 10 – Building the Retriever

> **Objective:** Learn how Retrieval-Augmented Generation (RAG) finds relevant information by converting a user's question into an embedding and retrieving the most similar document chunks from the FAISS vector database.

---

# 🤔 What Is a Retriever?

Imagine you walk into a large library and ask:

> "How can I detect phishing emails?"

You wouldn't expect the librarian to hand you every cybersecurity book.

Instead, they would locate the few books or pages most likely to answer your question.

A **Retriever** performs the same task.

Instead of searching books, it searches embeddings.

Instead of returning entire documents, it returns only the most relevant chunks.

---

# 🧠 Why Is This Important?

Large Language Models should not receive your entire knowledge base.

Instead, they should receive only the information related to the user's question.

This makes responses:

- ✅ Faster
- ✅ More accurate
- ✅ Less expensive
- ✅ More focused

The Retriever is responsible for finding that information.

---

# 🔄 Where Does the Retriever Fit?

Our RAG pipeline now looks like this:

```text
PDF Documents

↓

Document Loader

↓

Text Chunker

↓

Embedding Generator

↓

FAISS Vector Store

↓

Retriever

↓

Relevant Chunks

↓

Ollama

↓

Final AI Response
```

---

# 📁 Open the Module

Inside:

```text
backend/
```

Open:

```text
rag_engine.py
```

We'll use this module to build our retrieval engine.

---

# ✍️ Replace the File with the Following Code

```python
from backend.embedding_generator import EmbeddingGenerator


class RAGEngine:
    """
    Retrieves the most relevant document chunks
    for a user's question.
    """

    def __init__(self, vector_store):

        self.vector_store = vector_store

        self.embedding_generator = EmbeddingGenerator()

    def retrieve(self, question, top_k=5):

        query_embedding = self.embedding_generator.model.encode(
            question
        )

        results = self.vector_store.search(
            query_embedding,
            top_k=top_k
        )

        return results
```

Save the file.

---

# 🔍 Understanding the Code

Let's examine each section.

---

## Import Statement

```python
from backend.embedding_generator import EmbeddingGenerator
```

We're reusing the same embedding model that processed our documents.

This is extremely important.

If the documents and the user's question were embedded using different models, their vectors would not exist in the same semantic space.

Always use the same embedding model for both.

---

## Constructor

```python
def __init__(self, vector_store):
```

Instead of creating a new vector database, the Retriever receives one that already exists.

This allows multiple components of the application to share the same index.

---

## Creating the Query Embedding

```python
query_embedding = self.embedding_generator.model.encode(
    question
)
```

Remember:

Our documents were converted into embeddings.

Now we do exactly the same thing with the user's question.

Example:

```
User Question

↓

Embedding

↓

Search FAISS
```

---

## Searching the Vector Database

```python
self.vector_store.search(...)
```

FAISS compares the question's embedding against every stored document embedding.

It returns the chunks whose meanings are most similar.

---

## Returning the Results

The Retriever simply returns a list of document chunks.

Those chunks will later become context for Ollama.

At this stage, we are not generating an AI response yet.

We're only retrieving information.

---

# 🧪 Testing the Retriever

Create a temporary file named:

```text
test_retriever.py
```

Add the following code:

```python
from backend.document_loader import DocumentLoader
from backend.text_chunker import TextChunker
from backend.embedding_generator import EmbeddingGenerator
from backend.vector_store import VectorStore
from backend.rag_engine import RAGEngine

loader = DocumentLoader(
    "knowledge_base/documents"
)

documents = loader.load_documents()

chunker = TextChunker()

chunks = chunker.chunk_documents(documents)

generator = EmbeddingGenerator()

embeddings = generator.generate_embeddings(chunks)

store = VectorStore()

store.build_index(
    embeddings,
    chunks
)

retriever = RAGEngine(store)

results = retriever.retrieve(
    "How do phishing attacks work?"
)

print("Top Results")

for index, result in enumerate(results, start=1):

    print(f"\nResult {index}")

    print(result["filename"])

    print(result["text"][:250])
```

Save the file.

---

# ▶️ Run the Test

Open the terminal.

Run:

```powershell
python test_retriever.py
```

---

# ✅ Expected Output

Your output will vary depending on the PDFs you've added, but it should resemble:

```text
Top Results

Result 1

OWASP.pdf

Phishing attacks attempt to deceive users...

Result 2

MITRE.pdf

Spear phishing is a targeted attack...

Result 3

Incident_Response.pdf

Employees should immediately report...
```

The Retriever has successfully identified the most relevant sections of your cybersecurity documentation.

---

# 💡 Why Don't We Return Entire Documents?

Imagine a 200-page NIST guide.

If only one paragraph discusses phishing, sending all 200 pages would waste time and reduce the quality of the AI's response.

Returning only the most relevant chunks keeps the context focused and efficient.

---

# ⚙️ Understanding `top_k`

Notice this parameter:

```python
top_k=5
```

This tells FAISS:

> "Return the five most relevant chunks."

You can experiment with different values.

For example:

```python
top_k=3
```

or

```python
top_k=10
```

Larger values provide more context but also increase the amount of information sent to the language model.

---

# ⚠️ Common Errors

## Error

```text
AttributeError:
'NoneType' object has no attribute 'search'
```

### Cause

The vector store was never built or loaded.

Make sure you call:

```python
store.build_index(...)
```

before creating the Retriever.

---

## Error

```text
IndexError
```

### Cause

The vector database is empty.

Verify that:

- PDFs were loaded
- Chunks were created
- Embeddings were generated
- The FAISS index was built

---

## Error

No relevant results are returned.

### Possible Causes

- Your knowledge base doesn't contain information related to the question.
- The document loading process failed.
- The FAISS index wasn't rebuilt after adding new documents.

---

# 📊 Visualizing the Retrieval Process

```text
User Question

↓

Embedding

↓

FAISS Search

↓

Top 5 Chunks

↓

Returned to Application
```

Notice that the AI model hasn't been called yet.

The Retriever's only responsibility is to locate information.

---

# 🎓 What You Learned

Congratulations!

You've now built the fifth stage of the RAG pipeline.

You understand:

- ✅ What a Retriever does
- ✅ Why the user's question becomes an embedding
- ✅ Why the same embedding model must be used
- ✅ How FAISS identifies similar meanings
- ✅ Why only relevant chunks are returned

---

# 🧪 Knowledge Check

Can you answer these questions?

- Why does the user's question become an embedding?
- Why must documents and questions use the same embedding model?
- What does the Retriever return?
- What does `top_k` control?
- Why don't we send the entire knowledge base to the language model?

If you can answer these questions, you're ready to continue.

---

# ✅ Checkpoint

🎉 Congratulations!

Your AI SOC Analyst Assistant can now:

- 📄 Load cybersecurity documents
- ✂️ Split them into chunks
- 🧠 Generate embeddings
- ⚡ Build a FAISS vector database
- 🔍 Retrieve the most relevant document chunks for any user question

In the next chapter, you'll build the **Ollama Client**, which sends the retrieved context and the user's question to a local Large Language Model so it can generate a cybersecurity-focused response.

---

# 🤖 Chapter 11 – Building the Ollama Client

> **Objective:** Learn how your application communicates with a locally running Large Language Model (LLM) using Ollama and build the module responsible for sending prompts and receiving AI-generated responses.

---

# 🤔 What Is Ollama?

Earlier in this guide, you installed Ollama.

But what exactly is it?

Ollama is an application that allows you to run Large Language Models (LLMs) directly on your own computer.

Instead of sending your questions to cloud services like ChatGPT or Gemini, Ollama keeps everything on your local machine.

This provides several benefits:

- ✅ Better privacy
- ✅ No internet required after downloading the model
- ✅ No API costs
- ✅ Faster development and testing
- ✅ Complete control over the model

For cybersecurity projects, this is especially valuable because sensitive information never has to leave your computer.

---

# 🧠 What Is an LLM?

A Large Language Model is an AI system trained to understand and generate human language.

Examples include:

- Llama
- Mistral
- Gemma
- DeepSeek
- Phi

In this project, Ollama manages the model while our Python application communicates with it.

---

# 🔄 Where Does the Ollama Client Fit?

Our RAG pipeline now looks like this:

```text
User Question

↓

Retriever

↓

Relevant Chunks

↓

Prompt Builder

↓

Ollama Client

↓

Large Language Model

↓

AI Response
```

The Retriever finds information.

The Ollama Client asks the AI to use that information to answer the user's question.

---

# 📁 Open the Module

Inside the **backend** folder, open:

```text
ollama_client.py
```

---

# ✍️ Replace the File with the Following Code

```python
import ollama


class OllamaClient:
    """
    Sends prompts to a local Ollama model.
    """

    def __init__(self, model="llama3.2"):
        self.model = model

    def generate(self, prompt):

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]
```

Save the file.

---

# 🔍 Understanding the Code

Let's examine each section.

---

## Import Statement

```python
import ollama
```

This imports the official Ollama Python library.

It allows Python to communicate with the Ollama application running on your computer.

---

## Constructor

```python
def __init__(...)
```

When we create an `OllamaClient`, we specify which model we want to use.

By default:

```python
llama3.2
```

If you downloaded another model, you can simply change this value.

For example:

```python
model="mistral"
```

or

```python
model="gemma3"
```

---

## Sending a Prompt

```python
ollama.chat(...)
```

This sends a request to the local Ollama server.

Unlike cloud AI services, the request never leaves your computer.

---

## Messages

```python
messages=[
    {
        "role": "user",
        "content": prompt
    }
]
```

Most modern language models use a conversation format.

Each message has:

- a role
- content

For this chapter, we're sending a single user message.

Later, we'll improve this by including system instructions and retrieved context.

---

## Returning the Response

```python
return response["message"]["content"]
```

Ollama returns a large response object.

We're interested only in the AI's generated text.

---

# 🧪 Testing the Ollama Client

Create a temporary file named:

```text
test_ollama.py
```

Add:

```python
from backend.ollama_client import OllamaClient

client = OllamaClient()

response = client.generate(
    "Explain phishing attacks in two sentences."
)

print(response)
```

Save the file.

---

# ▶️ Before Running the Test

Make sure Ollama is running.

Open a terminal and verify your installed models:

```powershell
ollama list
```

You should see something similar to:

```text
NAME

llama3.2
```

If the model is not listed, download it:

```powershell
ollama pull llama3.2
```

---

# ▶️ Run the Test

Run:

```powershell
python test_ollama.py
```

---

# ✅ Expected Output

Your wording will differ, but you should receive something similar to:

```text
Phishing is a cyberattack in which attackers attempt to trick users into revealing sensitive information through deceptive emails, websites, or messages.

Organizations can reduce phishing risk through user awareness training, email filtering, and multi-factor authentication.
```

Congratulations!

Your Python application has successfully communicated with a local AI model.

---

# 💡 Why Don't We Send the User's Question Directly?

At the moment, we are only sending:

```
User Question
```

Soon we'll improve this by sending:

```
Retrieved Documents

+

User Question

↓

LLM
```

This is what makes RAG so powerful.

Instead of relying only on what the model remembers from training, it can answer using your own cybersecurity documentation.

---

# ⚠️ Common Errors

## Error

```text
ConnectionError
```

### Cause

Ollama is not running.

### Solution

Start Ollama and try again.

---

## Error

```text
Model not found
```

### Cause

The requested model has not been downloaded.

### Solution

Run:

```powershell
ollama pull llama3.2
```

---

## Error

```text
ModuleNotFoundError:
ollama
```

### Solution

Install the Python package:

```powershell
pip install ollama
```

---

# 🧠 Real-World Workflow

Here's what just happened behind the scenes:

```text
Python

↓

Ollama Python Library

↓

Local Ollama Server

↓

Llama 3.2

↓

Generated Response

↓

Python
```

Everything happened locally on your computer.

No external API was required.

---

# 🎓 What You Learned

Congratulations!

You've now built the component responsible for AI text generation.

You understand:

- ✅ What Ollama is
- ✅ Why local LLMs are useful
- ✅ How Python communicates with Ollama
- ✅ How prompts are sent
- ✅ How responses are received

---

# 🧪 Knowledge Check

Can you answer these questions?

- What is Ollama?
- Why run an LLM locally?
- What does `ollama.chat()` do?
- What information does the `messages` parameter contain?
- Why do we return `response["message"]["content"]` instead of the full response?

If you can answer these questions, you're ready to continue.

---

# ✅ Checkpoint

🎉 Outstanding!

Your AI SOC Analyst Assistant can now:

- 📄 Load cybersecurity documents
- ✂️ Split them into chunks
- 🧠 Generate embeddings
- ⚡ Search a FAISS vector database
- 🔍 Retrieve relevant document chunks
- 🤖 Generate AI responses using a local LLM

In the next chapter, you'll build the **Prompt Builder**, where you'll combine the retrieved cybersecurity documentation with the user's question to create the high-quality prompts that drive accurate Retrieval-Augmented Generation (RAG).

---

# 📝 Chapter 12 – Building the Prompt Builder

> **Objective:** Learn why prompt engineering is critical for Retrieval-Augmented Generation (RAG) systems and build the module responsible for combining retrieved cybersecurity documentation with the user's question before sending it to the AI model.

---

# 🤔 What Is a Prompt?

A prompt is the instruction you send to a Large Language Model.

Think of it like giving directions to a new employee.

Consider these two instructions:

❌

> Explain phishing.

Now compare it to:

✅

> You are an experienced SOC Analyst. Using only the documentation below, explain phishing in simple language. If the answer cannot be found, clearly state that the documentation does not contain enough information.

Which instruction is more likely to produce a useful answer?

The second.

The AI performs better when it receives clear guidance.

---

# 🧠 Why Does RAG Need Prompt Engineering?

Remember...

Our Retriever already found the most relevant document chunks.

Now we need to combine:

- the retrieved documents
- the user's question
- instructions for the AI

into one prompt.

Without this step, the model has no idea:

- what its role is
- which information to trust
- how to answer
- what to do if information is missing

---

# 🔄 Where Does the Prompt Builder Fit?

Our pipeline now looks like this:

```text
User Question

↓

Retriever

↓

Relevant Chunks

↓

Prompt Builder

↓

Ollama

↓

AI Response
```

The Prompt Builder prepares everything before the AI begins generating a response.

---

# 📁 Open the Module

Inside:

```text
backend/
```

Open:

```text
prompts.py
```

---

# ✍️ Replace the File with the Following Code

```python
class PromptBuilder:
    """
    Builds prompts for the Large Language Model.
    """

    @staticmethod
    def build(question, retrieved_chunks):

        context = "\n\n".join(
            chunk["text"]
            for chunk in retrieved_chunks
        )

        prompt = f"""
You are an experienced SOC Analyst.

Answer the user's question using ONLY the cybersecurity documentation below.

If the answer cannot be found in the documentation, clearly state that the information is unavailable.

========================
Cybersecurity Documentation
========================

{context}

========================
User Question
========================

{question}

========================
Answer
========================
"""

        return prompt.strip()
```

Save the file.

---

# 🔍 Understanding the Code

Let's examine the module one section at a time.

---

## Why Use a Class?

```python
class PromptBuilder:
```

Rather than scattering prompt text throughout the application, we keep it in one location.

This makes prompts easier to:

- modify
- improve
- test
- reuse

Professional AI projects almost always separate prompt construction from business logic.

---

## The Static Method

```python
@staticmethod
```

Notice this method doesn't depend on any stored class data.

We simply call:

```python
PromptBuilder.build(...)
```

without creating an object first.

---

## Combining the Retrieved Chunks

```python
context = "\n\n".join(...)
```

Suppose the Retriever returned five chunks.

Instead of sending five separate messages, we combine them into one block of text.

Example:

```text
Chunk 1

Chunk 2

Chunk 3

Chunk 4

Chunk 5
```

This becomes the context the AI will use when answering.

---

## Giving the AI a Role

```text
You are an experienced SOC Analyst.
```

This tells the model how it should behave.

Role instructions help guide tone, vocabulary, and reasoning.

---

## Restricting the AI

Notice this instruction:

```text
Answer the user's question using ONLY the cybersecurity documentation below.
```

This is extremely important.

Without it, the model might answer from its own training data instead of your documentation.

RAG systems are designed to ground answers in trusted sources.

---

## Handling Missing Information

Our prompt also says:

```text
If the answer cannot be found...
```

This teaches the AI to admit uncertainty.

That is often better than generating an incorrect answer.

---

## Separating Sections

Notice the divider lines:

```text
========================
```

These clearly separate:

- instructions
- documentation
- user question

This structure makes the prompt easier for both humans and language models to understand.

---

# 🧪 Testing the Prompt Builder

Create a temporary file named:

```text
test_prompt.py
```

Add:

```python
from backend.prompts import PromptBuilder

chunks = [
    {
        "filename": "OWASP.pdf",
        "text": "Phishing attacks attempt to trick users into revealing sensitive information."
    },
    {
        "filename": "MITRE.pdf",
        "text": "Spear phishing targets specific individuals or organizations."
    }
]

prompt = PromptBuilder.build(
    "What is phishing?",
    chunks
)

print(prompt)
```

Save the file.

---

# ▶️ Run the Test

Open your terminal.

Run:

```powershell
python test_prompt.py
```

---

# ✅ Expected Output

You should see something similar to:

```text
You are an experienced SOC Analyst.

Answer the user's question using ONLY the cybersecurity documentation below.

...

Cybersecurity Documentation

Phishing attacks...

Spear phishing...

User Question

What is phishing?
```

Notice how everything is organized into a single prompt.

That prompt will soon be sent directly to Ollama.

---

# 💡 Why Don't We Send Multiple Prompts?

Instead of sending:

```
Chunk 1

↓

Chunk 2

↓

Chunk 3
```

we combine everything into one structured prompt.

This allows the model to consider all relevant information at the same time.

---

# ⚠️ Common Errors

## Error

```text
KeyError: text
```

### Cause

One or more retrieved chunks do not contain a `"text"` field.

Verify that your Retriever returns dictionaries with both:

- `"filename"`
- `"text"`

---

## Error

Prompt is empty.

### Cause

The Retriever returned no document chunks.

Check that:

- PDFs were loaded
- Chunks were generated
- Embeddings were indexed
- Retrieval returned results

---

# 📊 Visualizing Prompt Construction

```text
Retrieved Chunk 1

+

Retrieved Chunk 2

+

Retrieved Chunk 3

+

User Question

↓

Prompt Builder

↓

One Complete Prompt

↓

Ollama
```

---

# 🎓 What You Learned

Congratulations!

You've built the Prompt Builder—the component that transforms retrieved knowledge into instructions the AI can understand.

You now understand:

- ✅ What prompt engineering is
- ✅ Why RAG systems require structured prompts
- ✅ How retrieved chunks become context
- ✅ Why role instructions improve responses
- ✅ Why grounding the AI in documentation reduces hallucinations

---

# 🧪 Knowledge Check

Can you answer these questions?

- What is a prompt?
- Why does the Prompt Builder exist?
- Why do we combine retrieved chunks into one context block?
- Why tell the AI to answer only from the documentation?
- Why is it important for the AI to admit when information is unavailable?

If you can answer these questions, you're ready to continue.

---

# ✅ Checkpoint

🎉 Outstanding!

Your AI SOC Analyst Assistant can now:

- 📄 Load cybersecurity documents
- ✂️ Split them into chunks
- 🧠 Generate embeddings
- ⚡ Build a FAISS vector database
- 🔍 Retrieve relevant document chunks
- 📝 Build structured prompts
- 🤖 Prepare high-quality instructions for the local AI model

In the next chapter, you'll connect every component together inside the **RAG Engine**, creating the complete Retrieval-Augmented Generation workflow from user question to AI-generated answer.

---

# 🔗 Chapter 13 – Building the Complete RAG Engine

> **Objective:** Connect every backend component into a complete Retrieval-Augmented Generation (RAG) workflow that can answer cybersecurity questions using your local knowledge base.

---

# 🎯 What Is the RAG Engine?

So far, we've built several individual components:

- 📄 Document Loader
- ✂️ Text Chunker
- 🧠 Embedding Generator
- ⚡ FAISS Vector Store
- 🔍 Retriever
- 📝 Prompt Builder
- 🤖 Ollama Client

Each one performs a specific task.

The **RAG Engine** is responsible for coordinating all of them.

Think of it as the conductor of an orchestra.

Each musician knows how to play an instrument, but the conductor ensures they perform together as one cohesive piece.

---

# 🧠 The Complete Workflow

When a user asks a question, the application performs these steps:

1. Receive the user's question.
2. Convert the question into an embedding.
3. Search the FAISS vector database.
4. Retrieve the most relevant document chunks.
5. Build a structured prompt.
6. Send the prompt to Ollama.
7. Receive the AI-generated response.
8. Display the answer to the user.

This entire sequence happens in just a few seconds.

---

# 🔄 Visualizing the Pipeline

```text
User Question
        │
        ▼
Retriever
        │
        ▼
Relevant Chunks
        │
        ▼
Prompt Builder
        │
        ▼
Ollama Client
        │
        ▼
AI Response
```

---

# 📁 Open the Module

Inside:

```text
backend/
```

Open:

```text
rag_engine.py
```

Replace the contents with the following code.

---

# ✍️ Add the Following Code

```python
from backend.embedding_generator import EmbeddingGenerator
from backend.prompts import PromptBuilder
from backend.ollama_client import OllamaClient


class RAGEngine:
    """
    Coordinates the Retrieval-Augmented Generation workflow.
    """

    def __init__(self, vector_store):

        self.vector_store = vector_store

        self.embedding_generator = EmbeddingGenerator()

        self.ollama_client = OllamaClient()

    def retrieve(self, question, top_k=5):

        query_embedding = self.embedding_generator.model.encode(
            question
        )

        return self.vector_store.search(
            query_embedding,
            top_k=top_k
        )

    def answer(self, question):

        retrieved_chunks = self.retrieve(question)

        prompt = PromptBuilder.build(
            question,
            retrieved_chunks
        )

        response = self.ollama_client.generate(
            prompt
        )

        return {
            "question": question,
            "response": response,
            "sources": [
                chunk["filename"]
                for chunk in retrieved_chunks
            ]
        }
```

Save the file.

---

# 🔍 Understanding the Code

Let's examine the workflow one step at a time.

---

## Import Statements

```python
from backend.prompts import PromptBuilder
```

Imports the component responsible for constructing prompts.

---

```python
from backend.ollama_client import OllamaClient
```

Imports the component that communicates with the local AI model.

---

```python
from backend.embedding_generator import EmbeddingGenerator
```

Imports the embedding model used to encode the user's question.

---

# Constructor

```python
def __init__(...)
```

When the RAG Engine starts, it receives a vector store and creates the components it needs to retrieve information and generate responses.

Notice that the Document Loader and Text Chunker are **not** created here.

Those components are used during the indexing process, not while answering questions.

---

# Step 1 – Retrieve Relevant Information

```python
retrieved_chunks = self.retrieve(question)
```

The user's question is converted into an embedding.

FAISS searches the vector database.

The most relevant chunks are returned.

---

# Step 2 – Build the Prompt

```python
PromptBuilder.build(...)
```

The retrieved chunks and the user's question are combined into one structured prompt.

---

# Step 3 – Generate the Answer

```python
self.ollama_client.generate(...)
```

The prompt is sent to Ollama.

The language model generates a response using the retrieved documentation.

---

# Step 4 – Return the Results

Instead of returning only the answer, we return a dictionary containing:

- the original question
- the AI response
- the source documents

This makes the application easier to expand later.

For example, a future version could display clickable source references in the interface.

---

# 🧪 Testing the Complete RAG Engine

Create a temporary file named:

```text
test_rag.py
```

Add the following code:

```python
from backend.vector_store import VectorStore
from backend.rag_engine import RAGEngine

store = VectorStore()

store.load(
    "knowledge_base/indexes"
)

engine = RAGEngine(store)

result = engine.answer(
    "What is phishing?"
)

print("Question:")
print(result["question"])

print("\nResponse:")
print(result["response"])

print("\nSources:")

for source in result["sources"]:
    print(f"- {source}")
```

Save the file.

---

# ▶️ Run the Test

Open your terminal.

Run:

```powershell
python test_rag.py
```

---

# ✅ Expected Output

Your output will vary depending on your documents and model, but it should resemble:

```text
Question:

What is phishing?

Response:

Phishing is a social engineering attack in which attackers attempt to deceive users into revealing sensitive information such as usernames, passwords, or financial data...

Sources:

- OWASP.pdf
- MITRE.pdf
- Incident_Response.pdf
```

Congratulations!

You have successfully built a complete Retrieval-Augmented Generation backend.

---

# 💡 Why Return the Sources?

Returning the source filenames provides transparency.

Users can see which documents influenced the AI's response.

This is especially valuable in cybersecurity, where analysts often need to verify information against trusted references.

In future improvements, you could display:

- filenames
- page numbers
- confidence scores
- direct links to the original documents

---

# ⚠️ Common Errors

## Error

```text
FileNotFoundError:
faiss.index
```

### Cause

The vector database has not been created yet.

### Solution

Run the indexing process from the previous chapters before testing the RAG Engine.

---

## Error

```text
ConnectionError
```

### Cause

Ollama is not running.

### Solution

Start Ollama and verify the model is available using:

```powershell
ollama list
```

---

## Error

The response says no information is available.

### Possible Causes

- The knowledge base doesn't contain relevant information.
- The vector database wasn't rebuilt after adding new PDFs.
- The Retriever returned unrelated chunks.

Verify your indexing pipeline and rebuild the FAISS index if necessary.

---

# 📊 End-to-End Workflow

```text
User Question
        │
        ▼
Generate Question Embedding
        │
        ▼
Search FAISS
        │
        ▼
Retrieve Top Chunks
        │
        ▼
Build Prompt
        │
        ▼
Send to Ollama
        │
        ▼
Generate Response
        │
        ▼
Return Answer + Sources
```

---

# 🎓 What You Learned

Congratulations!

You've built the complete backend workflow for your AI SOC Analyst Assistant.

You now understand:

- ✅ How every backend component works together
- ✅ How Retrieval-Augmented Generation operates from beginning to end
- ✅ How user questions are processed
- ✅ How AI responses are grounded in trusted documentation
- ✅ Why modular architecture makes applications easier to maintain and extend

---

# 🧪 Knowledge Check

Can you answer these questions?

- What is the role of the RAG Engine?
- Why doesn't the RAG Engine directly load PDFs?
- Why do we return both the response and the source documents?
- What happens immediately after the Retriever finds relevant chunks?
- Why is modular design beneficial for AI applications?

If you can answer these questions, you've successfully completed the backend architecture.

---

# ✅ Checkpoint

🎉 Incredible work!

Your AI SOC Analyst Assistant now has a fully functional backend capable of:

- 📄 Reading cybersecurity documents
- ✂️ Splitting them into chunks
- 🧠 Creating semantic embeddings
- ⚡ Building and searching a FAISS vector database
- 🔍 Retrieving relevant knowledge
- 📝 Constructing high-quality prompts
- 🤖 Generating grounded AI responses using Ollama

In the next chapter, you'll begin building the **Streamlit web interface**, allowing users to interact with your AI SOC Analyst Assistant through a clean, professional, browser-based application.

---

# 🏗️ Chapter 14 – Building the Knowledge Base Indexing Pipeline

> **Objective:** Learn why indexing is performed separately from question answering and build the script that transforms your cybersecurity documents into a searchable FAISS knowledge base.

---

# 🤔 Why Do We Need an Indexing Pipeline?

Think about a search engine like Google.

Google doesn't search the internet every time you type a question.

Instead, Google continuously:

- Reads web pages
- Processes them
- Stores searchable information

Then, when you search, it looks through its prepared index.

Our AI SOC Analyst Assistant works the same way.

Instead of processing hundreds of PDFs every time a question is asked, we process them once and save the results.

---

# 🧠 Two Different Workflows

Our application actually has two completely separate workflows.

## Workflow 1 — Indexing

Runs only when documents change.

```text
PDF Documents

↓

Document Loader

↓

Text Chunker

↓

Embedding Generator

↓

FAISS Index

↓

Saved to Disk
```

---

## Workflow 2 — Question Answering

Runs every time a user asks a question.

```text
User Question

↓

Load FAISS

↓

Retriever

↓

Prompt Builder

↓

Ollama

↓

Answer
```

Separating these workflows makes the application much faster.

---

# 📁 Open the File

In the project root, open:

```text
app.py
```

This file will build the knowledge base.

---

# ✍️ Replace the File with the Following Code

```python
from backend.document_loader import DocumentLoader
from backend.text_chunker import TextChunker
from backend.embedding_generator import EmbeddingGenerator
from backend.vector_store import VectorStore


def main():

    print("=" * 60)
    print("AI SOC Assistant")
    print("Knowledge Base Index Builder")
    print("=" * 60)

    loader = DocumentLoader(
        "knowledge_base/documents"
    )

    documents = loader.load_documents()

    print(f"\nLoaded {len(documents)} documents.")

    chunker = TextChunker()

    chunks = chunker.chunk_documents(
        documents
    )

    print(f"Created {len(chunks)} chunks.")

    generator = EmbeddingGenerator()

    embeddings = generator.generate_embeddings(
        chunks
    )

    print("Generated embeddings.")

    store = VectorStore()

    store.build_index(
        embeddings,
        chunks
    )

    store.save(
        "knowledge_base/indexes"
    )

    print("\nKnowledge base built successfully!")

    print("FAISS index saved.")

    print("Chunk metadata saved.")


if __name__ == "__main__":
    main()
```

Save the file.

---

# 🔍 Understanding the Code

Notice that this script doesn't answer questions.

Instead, it prepares the application.

Let's examine each step.

---

## Step 1

```python
DocumentLoader()
```

Reads every PDF from the knowledge base.

---

## Step 2

```python
TextChunker()
```

Splits every document into smaller pieces.

---

## Step 3

```python
EmbeddingGenerator()
```

Converts every chunk into an embedding.

---

## Step 4

```python
VectorStore()
```

Creates the searchable FAISS index.

---

## Step 5

```python
save(...)
```

Stores everything on disk.

Later, the application simply loads this data instead of rebuilding it.

---

# ▶️ Run the Index Builder

Open the terminal.

Run:

```powershell
python app.py
```

---

# ✅ Expected Output

```text
============================================================
AI SOC Assistant
Knowledge Base Index Builder
============================================================

Loaded 8 documents.

Created 347 chunks.

Generating embeddings...

Generated embeddings.

Knowledge base built successfully!

FAISS index saved.

Chunk metadata saved.
```

Your numbers will depend on your knowledge base.

---

# 📂 Verify the Output

Open:

```text
knowledge_base/indexes/
```

You should see:

```text
faiss.index

chunks.pkl
```

These files are your searchable knowledge base.

---

# 💡 When Should You Run This Script?

Run the indexing pipeline whenever:

✅ You add a new PDF

✅ You remove a PDF

✅ You update a PDF

✅ You change the chunk size

✅ You change the embedding model

If none of those things change, you don't need to rebuild the index.

---

# ⚠️ Common Errors

## Error

```text
Loaded 0 documents
```

Verify that:

```text
knowledge_base/documents/
```

contains PDF files.

---

## Error

```text
Permission denied
```

Close any programs that currently have the PDF files open.

---

## Error

```text
ModuleNotFoundError
```

Verify that all dependencies from `requirements.txt` have been installed.

---

# 📊 The Complete Indexing Pipeline

```text
Cybersecurity PDFs
        │
        ▼
Load Documents
        │
        ▼
Split Into Chunks
        │
        ▼
Generate Embeddings
        │
        ▼
Build FAISS Index
        │
        ▼
Save Index to Disk
```

This process happens only when the knowledge base changes.

---

# 🎓 What You Learned

Congratulations!

You've built the indexing pipeline that prepares your AI SOC Analyst Assistant for semantic search.

You now understand:

- ✅ Why indexing and question answering are separate workflows
- ✅ How documents become a searchable knowledge base
- ✅ Why rebuilding the index is only necessary after document changes
- ✅ How the backend prepares data for Retrieval-Augmented Generation

---

# 🧪 Knowledge Check

Can you answer these questions?

- Why don't we rebuild the index every time a user asks a question?
- What are the five major steps in the indexing pipeline?
- Which files are created after indexing?
- When should you rerun the indexing script?
- Why is separating indexing from retrieval considered a best practice?

If you answered yes, you're ready to continue.

---

# ✅ Checkpoint

🎉 Outstanding!

You have now completed the complete backend infrastructure for the AI SOC Analyst Assistant.

Your application can:

- 📄 Read cybersecurity PDFs
- ✂️ Split documents into chunks
- 🧠 Generate semantic embeddings
- ⚡ Build a FAISS vector database
- 💾 Save a reusable knowledge base
- 🔍 Retrieve relevant information
- 📝 Build grounded prompts
- 🤖 Generate AI responses with Ollama

In the next chapter, you'll begin building the **Streamlit web interface**, transforming your backend into a polished, interactive application that cybersecurity analysts can use through their web browser.

---

# 🌐 Chapter 15 – Building the Streamlit User Interface

> **Objective:** Build the first version of the AI SOC Analyst Assistant's web interface using Streamlit and connect it to the completed RAG backend.

---

# 🤔 What Is Streamlit?

Up until now, we've interacted with our application through the terminal.

For example:

```powershell
python test_rag.py
```

While this is useful for development, it's not ideal for everyday users.

Instead, we'd like a professional interface where users can:

- Type questions
- Click a button
- View AI-generated responses
- Review supporting documentation

This is where **Streamlit** comes in.

---

# 🧠 What Is Streamlit?

Streamlit is a Python framework for building web applications.

The best part?

You don't need to know HTML, CSS, or JavaScript to create attractive user interfaces.

Everything is written in Python.

---

# 🎯 What Will We Build?

By the end of this chapter, you'll have a web application that looks something like this:

```text
----------------------------------------------------

🛡️ AI SOC Analyst Assistant

Ask a cybersecurity question:

[_____________________________________]

        [ Ask AI ]

----------------------------------------------------

Answer

The AI response appears here...

----------------------------------------------------
```

In future chapters, we'll continue improving this interface with additional features and styling.

---

# 🔄 How Does the Interface Work?

When a user types a question, the application performs the following steps:

```text
User Types Question

↓

Streamlit

↓

RAG Engine

↓

Retriever

↓

Prompt Builder

↓

Ollama

↓

Answer Returned

↓

Displayed in Browser
```

---

# 📁 Open the File

Inside the **frontend** folder, open:

```text
streamlit_app.py
```

Replace the file contents with the following code.

---

# ✍️ Add the Following Code

```python
import streamlit as st

from backend.vector_store import VectorStore
from backend.rag_engine import RAGEngine


@st.cache_resource
def load_engine():

    store = VectorStore()

    store.load(
        "knowledge_base/indexes"
    )

    return RAGEngine(store)


engine = load_engine()

st.set_page_config(
    page_title="AI SOC Analyst Assistant",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ AI SOC Analyst Assistant")

st.write(
    """
Ask questions about cybersecurity using your local
Retrieval-Augmented Generation knowledge base.
"""
)

question = st.text_input(
    "Enter your cybersecurity question:"
)

if st.button("Ask AI"):

    if question.strip():

        with st.spinner("Analyzing documentation..."):

            result = engine.answer(question)

        st.subheader("Answer")

        st.write(result["response"])

    else:

        st.warning(
            "Please enter a question."
        )
```

Save the file.

---

# 🔍 Understanding the Code

Let's explore each section.

---

## Importing Streamlit

```python
import streamlit as st
```

This imports the Streamlit framework.

Everything displayed in the browser comes from this library.

---

## Loading the Vector Store

```python
VectorStore()
```

Instead of rebuilding the knowledge base every time the application starts, we simply load the saved FAISS index.

This makes startup much faster.

---

## Caching the Engine

```python
@st.cache_resource
```

Without caching, Streamlit would rebuild the RAG Engine every time the page refreshes.

Caching tells Streamlit:

> "Load this resource once and reuse it."

This significantly improves performance.

---

## Configuring the Page

```python
st.set_page_config(...)
```

This controls:

- browser tab title
- page icon
- page layout

These settings improve the application's appearance before any content is displayed.

---

## Creating the Title

```python
st.title(...)
```

Displays the main heading at the top of the page.

---

## Creating the Text Box

```python
st.text_input(...)
```

Allows the user to type a cybersecurity question.

For example:

```
What is ransomware?

How do phishing attacks work?

Explain privilege escalation.
```

---

## Creating the Button

```python
st.button(...)
```

The AI only runs after the user clicks the button.

This prevents unnecessary requests while they're still typing.

---

## Displaying a Spinner

```python
st.spinner(...)
```

While Ollama generates a response, Streamlit displays a loading animation.

This reassures users that the application is working.

---

## Displaying the Answer

```python
st.write(...)
```

Once the AI finishes generating its response, the answer appears in the browser.

---

# ▶️ Running the Application

Open your terminal.

Navigate to the project folder.

Run:

```powershell
streamlit run frontend/streamlit_app.py
```

---

# 🌐 What Happens Next?

After a few moments, Streamlit will display something similar to:

```text
Local URL:

http://localhost:8501
```

Open that URL in your web browser.

The AI SOC Analyst Assistant interface should appear.

---

# 🧪 Testing the Application

Try asking questions such as:

```text
What is phishing?

Explain ransomware.

How does multi-factor authentication work?

What is privilege escalation?
```

If your knowledge base contains information about these topics, the AI should generate grounded responses using your documentation.

---

# ⚠️ Common Errors

## Error

```text
ModuleNotFoundError:
streamlit
```

### Solution

Run:

```powershell
pip install streamlit
```

---

## Error

```text
FileNotFoundError:
faiss.index
```

### Cause

The knowledge base has not been indexed.

### Solution

Run:

```powershell
python app.py
```

to rebuild the FAISS index.

---

## Error

No response appears.

### Possible Causes

- Ollama isn't running.
- The selected model hasn't been downloaded.
- The vector database couldn't be loaded.
- The question is unrelated to your documentation.

Verify each component before testing again.

---

# 📊 Complete Application Flow

```text
Web Browser
        │
        ▼
Streamlit Interface
        │
        ▼
RAG Engine
        │
        ▼
Retriever
        │
        ▼
Prompt Builder
        │
        ▼
Ollama
        │
        ▼
Answer
        │
        ▼
Displayed in Browser
```

---

# 🎓 What You Learned

Congratulations!

You've built the first graphical interface for your AI SOC Analyst Assistant.

You now understand:

- ✅ What Streamlit is
- ✅ How Python creates web interfaces
- ✅ How the frontend communicates with the backend
- ✅ How users interact with the RAG Engine
- ✅ How responses are displayed in the browser

---

# 🧪 Knowledge Check

Can you answer these questions?

- What does Streamlit allow us to build?
- Why do we cache the RAG Engine?
- Why do we load the FAISS index instead of rebuilding it?
- What happens after the user clicks **Ask AI**?
- Why is a web interface more user-friendly than terminal commands?

If you answered yes, you're ready to continue.

---

# ✅ Checkpoint

🎉 Congratulations!

Your AI SOC Analyst Assistant is now accessible through a modern web interface.

Users can:

- 🌐 Open the application in a browser
- 💬 Ask cybersecurity questions
- 🔍 Search the local knowledge base
- 🤖 Receive AI-generated responses powered by Retrieval-Augmented Generation

In the next chapter, you'll enhance the interface by displaying source documents, improving the layout, adding a sidebar, and creating a more polished, professional user experience suitable for a cybersecurity portfolio.

---

# 🎨 Chapter 16 – Enhancing the Streamlit User Interface

> **Objective:** Improve the AI SOC Analyst Assistant's user interface by adding a professional layout, sidebar, source references, response timing, and status indicators that create a polished user experience.

---

# 🤔 Why Improve the Interface?

Imagine you're evaluating two cybersecurity tools.

Tool A:

```
Question:

Answer:
```

Tool B:

```
🛡️ AI SOC Analyst Assistant

✔ Knowledge Base Loaded

✔ AI Model Connected

Response Time: 2.14 seconds

Answer

Sources Used

System Information
```

Both applications may produce identical answers.

Which one appears more professional?

Most people would choose Tool B.

Presentation matters.

---

# 🧠 Good Interfaces Build Trust

Cybersecurity professionals often need confidence that:

- the AI is working
- documentation was actually searched
- answers came from trusted sources
- the application is healthy

A polished interface helps communicate that information.

---

# 🎯 What We'll Add

In this chapter we'll improve the interface by adding:

- 🛡️ Sidebar
- 📚 Source document display
- ⏱ Response timing
- 📄 Expandable source list
- ℹ️ Application information
- ✅ Status indicators

---

# 📁 Open the File

Open:

```text
frontend/streamlit_app.py
```

Replace the existing contents with the following code.

---

# ✍️ Updated Streamlit Interface

```python
import time
import streamlit as st

from backend.vector_store import VectorStore
from backend.rag_engine import RAGEngine


@st.cache_resource
def load_engine():

    store = VectorStore()

    store.load(
        "knowledge_base/indexes"
    )

    return RAGEngine(store)


engine = load_engine()

st.set_page_config(
    page_title="AI SOC Analyst Assistant",
    page_icon="🛡️",
    layout="wide"
)

# ------------------------------
# Sidebar
# ------------------------------

with st.sidebar:

    st.header("🛡️ AI SOC Assistant")

    st.success("Knowledge Base Loaded")

    st.success("FAISS Index Ready")

    st.success("Ollama Connected")

    st.divider()

    st.subheader("About")

    st.write(
        """
This application demonstrates a local
Retrieval-Augmented Generation (RAG)
pipeline for cybersecurity analysis.
"""
    )

    st.divider()

    st.caption("Version 1.0")

# ------------------------------
# Main Page
# ------------------------------

st.title("🛡️ AI SOC Analyst Assistant")

st.write(
    """
Ask cybersecurity questions using your local knowledge base.
"""
)

question = st.text_input(
    "Enter your cybersecurity question:"
)

if st.button("Ask AI"):

    if question.strip():

        start = time.time()

        with st.spinner("Searching documentation..."):

            result = engine.answer(question)

        elapsed = time.time() - start

        st.success(
            f"Completed in {elapsed:.2f} seconds"
        )

        st.subheader("Answer")

        st.write(result["response"])

        st.subheader("Source Documents")

        unique_sources = sorted(
            set(result["sources"])
        )

        with st.expander("View Sources"):

            for source in unique_sources:

                st.write(f"📄 {source}")

    else:

        st.warning(
            "Please enter a question."
        )
```

Save the file.

---

# 🔍 Understanding the Improvements

Let's examine each new feature.

---

## Sidebar

```python
with st.sidebar:
```

Instead of placing everything in one column, Streamlit allows us to create a permanent sidebar.

This is a great place for:

- application information
- settings
- system status
- documentation

Professional dashboards often use sidebars to organize supporting information.

---

## Status Indicators

```python
st.success(...)
```

These green status boxes quickly communicate that important components are available.

For now, they're static messages.

In future improvements, you could automatically check whether:

- the FAISS index exists
- Ollama is running
- the selected model is installed

---

## Response Timing

```python
start = time.time()
```

Before generating an answer, we record the current time.

After the response is generated:

```python
elapsed = time.time() - start
```

This allows us to display how long the request took.

Response timing is useful for:

- measuring performance
- debugging
- comparing optimizations

---

## Source Documents

Instead of only displaying the AI's answer, we also display the documents that contributed to that answer.

Example:

```text
OWASP.pdf

MITRE.pdf

NIST.pdf
```

This increases transparency and helps users verify where information came from.

---

## Removing Duplicate Sources

Notice this line:

```python
set(result["sources"])
```

Multiple retrieved chunks may come from the same document.

Using a `set` removes duplicates before displaying the list.

---

## Expanders

```python
st.expander(...)
```

Rather than showing everything immediately, Streamlit allows us to hide additional information until the user wants to see it.

This keeps the interface clean while still making supporting information available.

---

# ▶️ Run the Updated Application

Run:

```powershell
streamlit run frontend/streamlit_app.py
```

---

# ✅ Expected Layout

Your application should now resemble:

```text
------------------------------------------------

🛡️ AI SOC Analyst Assistant

Ask a cybersecurity question:

[____________________________]

[ Ask AI ]

----------------------------------------------

Completed in 2.18 seconds

Answer

Lorem ipsum...

----------------------------------------------

Source Documents

▶ View Sources

----------------------------------------------

Sidebar

✔ Knowledge Base Loaded

✔ FAISS Ready

✔ Ollama Connected

Version 1.0

------------------------------------------------
```

The exact appearance may vary slightly depending on your browser and Streamlit version.

---

# 💡 Why Show Source Documents?

One of the biggest criticisms of AI systems is that users don't know where answers come from.

Displaying source documents helps users:

- verify information
- identify authoritative references
- build confidence in the system

In future versions, you could also display:

- page numbers
- document excerpts
- relevance scores

---

# ⚠️ Common Errors

## Error

```text
KeyError:
sources
```

### Cause

The RAG Engine isn't returning the `"sources"` key.

Review the previous chapter to ensure your `answer()` method returns:

```python
{
    "question": ...,
    "response": ...,
    "sources": ...
}
```

---

## Error

No sources appear.

### Cause

The Retriever returned no matching chunks.

Verify that your FAISS index has been built and contains your documents.

---

## Error

Response time displays as 0.00 seconds.

This can happen with very small knowledge bases or fast hardware.

As your document collection grows, you'll notice more realistic response times.

---

# 📊 Updated Application Workflow

```text
User Question
        │
        ▼
Search Knowledge Base
        │
        ▼
Retrieve Chunks
        │
        ▼
Generate Prompt
        │
        ▼
Ollama
        │
        ▼
Display Answer
        │
        ├────────► Display Sources
        │
        └────────► Display Response Time
```

---

# 🎓 What You Learned

Congratulations!

You've transformed a basic web application into a polished cybersecurity dashboard.

You now understand:

- ✅ How to organize a professional Streamlit layout
- ✅ Why sidebars improve usability
- ✅ How to measure response time
- ✅ Why source transparency is important
- ✅ How expanders help organize information

---

# 🧪 Knowledge Check

Can you answer these questions?

- Why display source documents?
- What is the purpose of a sidebar?
- Why measure response time?
- Why use an expander instead of showing everything immediately?
- Why remove duplicate source filenames before displaying them?

If you can answer these questions, you're ready to continue.

---

# ✅ Checkpoint

🎉 Excellent work!

Your AI SOC Analyst Assistant now includes:

- 🌐 A polished web interface
- 🛡️ System status sidebar
- 📚 Source document references
- ⏱ Response timing
- 📄 Expandable source lists
- 🤖 AI-generated cybersecurity responses

In the next chapter, you'll improve the user experience even further by adding **conversation history**, **sample questions**, **clear chat functionality**, and **persistent session state**, creating an interface that feels much closer to a modern AI assistant.

---

# 💬 Chapter 17 – Adding Conversation History and Session State

> **Objective:** Learn how Streamlit manages session state, preserve conversation history between interactions, provide sample prompts, and allow users to clear the conversation.

---

# 🤔 Why Conversation History Matters

Imagine asking an AI assistant these questions:

```
What is phishing?

↓

How do attackers perform it?

↓

How can organizations defend against it?
```

If the application forgets every previous interaction, the conversation feels disconnected.

Modern AI assistants maintain context during a session, making interactions more natural.

Although our current RAG engine answers each question independently, we can still improve the user experience by remembering previous questions and answers.

---

# 🧠 What Is Session State?

Normally, every time Streamlit updates the page, it reruns your Python script from top to bottom.

Without additional logic:

- previous questions disappear
- previous answers disappear
- variables reset

Streamlit solves this with **Session State**.

Session State allows your application to remember information while the browser session remains open.

---

# 🎯 What We'll Build

By the end of this chapter, users will be able to:

- 💬 View previous questions
- 🤖 Review previous AI responses
- 🗑️ Clear the conversation
- 💡 Click sample cybersecurity questions
- 🧠 Maintain history during the session

---

# 📁 Open the File

Open:

```text
frontend/streamlit_app.py
```

We'll enhance the interface you created in the previous chapter.

---

# ✍️ Initialize Session State

Near the top of your file, after loading the RAG engine, add:

```python
if "history" not in st.session_state:

    st.session_state.history = []
```

This creates an empty conversation history the first time the application loads.

---

# 🔍 Understanding Session State

Think of `st.session_state` as a small notebook that belongs to the user's browser session.

Instead of forgetting everything after each interaction, Streamlit stores information inside this notebook.

In our case:

```python
history
```

will store previous conversations.

---

# ✍️ Add Sample Questions

Below your page introduction, add:

```python
st.subheader("💡 Sample Questions")

sample_questions = [

    "What is phishing?",

    "Explain ransomware attacks.",

    "What is privilege escalation?",

    "Describe multi-factor authentication.",

    "What are Indicators of Compromise (IOCs)?"

]

selected_question = st.selectbox(

    "Choose a sample question:",

    [""] + sample_questions

)

if selected_question:

    question = selected_question
```

This gives first-time users ideas for interacting with the application.

---

# ✍️ Save Each Conversation

After generating the AI response, append the following:

```python
st.session_state.history.append(

    {

        "question": question,

        "response": result["response"],

        "sources": result["sources"]

    }

)
```

Now every interaction is stored in memory.

---

# ✍️ Display Conversation History

Near the bottom of the page, add:

```python
st.divider()

st.header("💬 Conversation History")

if st.session_state.history:

    for conversation in reversed(
        st.session_state.history
    ):

        with st.expander(
            conversation["question"]
        ):

            st.markdown("### 🤖 Response")

            st.write(
                conversation["response"]
            )

            st.markdown("### 📚 Sources")

            for source in sorted(
                set(conversation["sources"])
            ):

                st.write(f"📄 {source}")

else:

    st.info(
        "No conversation history yet."
    )
```

Notice that the newest conversations appear first.

---

# ✍️ Add a Clear Conversation Button

Inside the sidebar, add:

```python
if st.button("🗑️ Clear Conversation"):

    st.session_state.history = []

    st.rerun()
```

Clicking this button removes every stored interaction.

---

# 🔍 Understanding the New Features

---

## Session State

```python
st.session_state.history
```

Stores every conversation during the current browser session.

---

## Sample Questions

Instead of forcing users to think of a question immediately, we provide examples.

This improves discoverability and makes demonstrations easier.

---

## Expanders

Each conversation is stored inside an expandable panel.

This keeps long conversations organized.

---

## Clear Conversation

Rather than refreshing the browser manually, users can reset the application with one click.

---

# ▶️ Run the Updated Application

Run:

```powershell
streamlit run frontend/streamlit_app.py
```

Ask several different questions.

You should notice:

- Conversation history grows
- Previous answers remain visible
- Sources remain attached
- History persists while the application is open

---

# ✅ Expected Layout

```text
------------------------------------------------------

🛡️ AI SOC Analyst Assistant

Question Box

Ask AI

-----------------------------------

Answer

-----------------------------------

Conversation History

▶ What is phishing?

▶ Explain ransomware.

▶ What is MFA?

-----------------------------------

Sidebar

✔ Knowledge Base Loaded

✔ Ollama Connected

🗑 Clear Conversation

------------------------------------------------------
```

---

# 💡 Why Don't We Store Conversations Permanently?

Session State exists only while the browser session is active.

This keeps the project simple and avoids storing potentially sensitive cybersecurity questions on disk.

If permanent history is desired, future versions could use:

- SQLite
- PostgreSQL
- MongoDB
- Redis

For this educational project, session memory is sufficient.

---

# ⚠️ Common Errors

## Error

```text
AttributeError:
history
```

### Cause

The session state variable was never initialized.

Verify that:

```python
if "history" not in st.session_state:
```

appears near the top of the file.

---

## Error

History disappears after every interaction.

### Cause

Conversations were never appended to `st.session_state.history`.

Double-check the append statement after generating each response.

---

## Error

Duplicate conversations appear.

### Cause

The append statement may be executing multiple times.

Ensure it's only called after a successful AI response.

---

# 📊 Updated User Experience

```text
User Question
        │
        ▼
RAG Engine
        │
        ▼
AI Response
        │
        ▼
Display Answer
        │
        ▼
Save to Session History
        │
        ▼
Conversation Appears in Browser
```

---

# 🎓 What You Learned

Congratulations!

You've significantly improved the usability of your AI SOC Analyst Assistant.

You now understand:

- ✅ What Streamlit Session State is
- ✅ Why modern AI assistants remember conversations
- ✅ How to store information during a browser session
- ✅ How to organize previous conversations
- ✅ How to build a cleaner user experience

---

# 🧪 Knowledge Check

Can you answer these questions?

- What problem does Session State solve?
- Why don't variables normally persist in Streamlit?
- Why use expanders for conversation history?
- Why provide sample questions?
- Why is a "Clear Conversation" button useful?

If you can answer these questions, you're ready to continue.

---

# ✅ Checkpoint

🎉 Outstanding!

Your AI SOC Analyst Assistant now includes:

- 🌐 Professional web interface
- 💬 Conversation history
- 🧠 Session memory
- 💡 Sample cybersecurity questions
- 📚 Source references
- 🗑️ One-click conversation reset
- 🤖 AI-powered responses grounded in your cybersecurity knowledge base

In the next chapter, you'll further enhance the application by adding **document management features**, allowing users to upload new PDFs through the interface, rebuild the knowledge base, and monitor indexing progress without leaving the web application.

---

# 🛠️ Chapter 18 – Building a Knowledge Base Management Panel

> **Objective:** Enhance the AI SOC Analyst Assistant by creating an administrative interface that allows users to manage the cybersecurity knowledge base without leaving the web application.

---

# 🤔 Why Build an Administration Panel?

Imagine you've deployed your AI SOC Analyst Assistant to your security team.

One day, new cybersecurity documentation becomes available.

For example:

- New MITRE ATT&CK techniques
- Updated NIST documentation
- New OWASP guidance
- New incident response playbooks

Should you have to:

- Close the application
- Open a terminal
- Copy files manually
- Rebuild everything from the command line

Probably not.

Professional software includes administrative tools that allow authorized users to manage the system directly from the interface.

In this chapter, we'll begin building those tools.

---

# 🧠 Separating Users from Administrators

Think of your application as having two different types of users.

### 👨‍💻 Security Analyst

Uses the application to:

- Ask cybersecurity questions
- Review AI-generated answers
- Read documentation
- Investigate incidents

---

### 🛠 Administrator

Maintains the application by:

- Uploading new PDFs
- Removing outdated documents
- Monitoring the knowledge base
- Rebuilding the FAISS index

Keeping these responsibilities separate makes the application easier to use and maintain.

---

# 🎯 What We'll Build

By the end of this chapter your application will include an Administration Panel capable of displaying:

- 📄 Number of documents
- 📚 Current knowledge base
- 📤 PDF uploader
- 🔄 Rebuild button (placeholder)
- 📂 Knowledge base status

We'll make the rebuild button functional in the next chapter.

---

# 🏗 Updated Application Layout

Our application will now look like this.

```text
--------------------------------------------------------

Sidebar

🛡 AI SOC Assistant

✔ Knowledge Base Loaded

✔ FAISS Ready

✔ Ollama Connected

--------------------------------

🛠 Administration

Knowledge Base PDFs

15

Upload PDF

[Choose File]

🔄 Rebuild Knowledge Base

--------------------------------

Current Documents

📄 OWASP.pdf

📄 MITRE.pdf

📄 NIST.pdf

--------------------------------------------------------
```

---

# 📁 Open the Streamlit Application

Open:

```text
frontend/streamlit_app.py
```

---

# 📦 Import Additional Libraries

Near the top of the file, add:

```python
from pathlib import Path
import shutil
```

---

# 🔍 Understanding These Imports

## pathlib

```python
from pathlib import Path
```

`Path` provides a clean, object-oriented way to work with files and folders.

Instead of writing long file paths as strings, we can use objects that are easier to read and maintain.

---

## shutil

```python
import shutil
```

The `shutil` module is used for copying files.

We'll use it to save uploaded PDF documents into our knowledge base.

---

# 📁 Create the Knowledge Base Directory

Below your imports, add:

```python
DOCUMENTS_DIR = Path(
    "knowledge_base/documents"
)

DOCUMENTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)
```

Save the file.

---

# 🔍 Understanding the Directory

This creates a variable pointing to:

```text
knowledge_base/documents
```

If the folder doesn't exist, Python automatically creates it.

The two parameters:

```python
parents=True
```

allow Python to create missing parent folders.

---

```python
exist_ok=True
```

prevents an error if the folder already exists.

---

# 🛠 Add an Administration Section

Inside your existing sidebar, scroll to the bottom.

Add:

```python
st.divider()

st.subheader("🛠 Administration")
```

---

# ▶️ What You'll See

Your sidebar now contains a new section.

```text
---------------------

🛠 Administration

---------------------
```

We'll continue adding features below it.

---

# 📊 Display the Number of Documents

Under the Administration heading, add:

```python
pdf_files = list(
    DOCUMENTS_DIR.glob("*.pdf")
)

st.metric(
    label="Knowledge Base PDFs",
    value=len(pdf_files)
)
```

Save the file.

---

# 🔍 Understanding the Code

This line:

```python
DOCUMENTS_DIR.glob("*.pdf")
```

searches the folder for every PDF document.

If your folder contains:

```text
MITRE.pdf

OWASP.pdf

NIST.pdf
```

Python returns all three files.

---

The `metric()` component displays a professional statistic.

Example:

```text
Knowledge Base PDFs

12
```

---

# 📤 Add a PDF Uploader

Below the metric, add:

```python
uploaded_file = st.file_uploader(

    "Upload a PDF",

    type=["pdf"]

)
```

---

# 🔍 Understanding file_uploader()

This creates a button that allows users to browse their computer.

Only PDF files are accepted because we specified:

```python
type=["pdf"]
```

---

# 💾 Save Uploaded Files

Immediately below the uploader, add:

```python
if uploaded_file:

    destination = (

        DOCUMENTS_DIR /

        uploaded_file.name

    )

    with open(destination, "wb") as file:

        shutil.copyfileobj(

            uploaded_file,

            file

        )

    st.success(

        f"{uploaded_file.name} uploaded successfully."

    )
```

Save the file.

---

# 🔍 Understanding the Upload Process

When a user selects a PDF:

```text
Choose File

↓

Python receives the file

↓

Copies the file

↓

Saves it into

knowledge_base/documents

↓

Displays Success Message
```

---

# 🔄 Add a Rebuild Button

Below the uploader, add:

```python
if st.button(

    "🔄 Rebuild Knowledge Base"

):

    st.info(

        "Automatic rebuilding will be added in the next chapter."

    )
```

---

# ❓ Why Isn't It Functional Yet?

We're intentionally building the interface first.

In the next chapter, we'll connect this button to the indexing pipeline you built earlier.

That will allow users to rebuild the FAISS index directly from the browser.

---

# 📚 Display Every Document

Finally, add:

```python
st.subheader(

    "📚 Current Documents"

)

if pdf_files:

    for pdf in sorted(pdf_files):

        st.write(

            f"📄 {pdf.name}"

        )

else:

    st.warning(

        "No PDF documents found."

    )
```

Save the file.

---

# ▶️ Run the Application

Open your terminal.

Run:

```powershell
streamlit run frontend/streamlit_app.py
```

---

# ✅ Expected Sidebar

Your sidebar should now resemble something like:

```text
🛡 AI SOC Assistant

✔ Knowledge Base Loaded

✔ FAISS Ready

✔ Ollama Connected

---------------------------------

🛠 Administration

Knowledge Base PDFs

14

Upload PDF

[Choose File]

🔄 Rebuild Knowledge Base

---------------------------------

📚 Current Documents

📄 OWASP.pdf

📄 MITRE.pdf

📄 NIST.pdf

📄 Incident_Response.pdf
```

Your exact document list will depend on your knowledge base.

---

# 💡 Why Build the Administration Panel First?

Professional software development often begins by building the user interface before implementing all of the underlying functionality.

This allows developers to:

- Verify the layout
- Test navigation
- Gather user feedback
- Incrementally add features

In the next chapter, we'll connect the **Rebuild Knowledge Base** button to the indexing pipeline so administrators can rebuild the FAISS index without leaving the application.

---

# ⚠️ Common Errors

## Error

```text
PermissionError
```

### Cause

The PDF may already be open in another application.

### Solution

Close the document and try uploading it again.

---

## Error

```text
Uploaded file doesn't appear.
```

### Cause

The file wasn't copied successfully.

### Solution

Verify the file now exists inside:

```text
knowledge_base/documents
```

---

## Error

```text
Knowledge Base PDFs

0
```

### Cause

No PDF files exist inside the documents folder.

### Solution

Upload a document using the uploader or manually copy PDF files into:

```text
knowledge_base/documents
```

---

# 📊 Administration Workflow

```text
Administrator

        │

        ▼

Upload PDF

        │

        ▼

Save to

knowledge_base/documents

        │

        ▼

View Updated Document List

        │

        ▼

Ready to Rebuild Index
```

---

# 🎓 What You Learned

Congratulations!

You've added the first administrative tools to your AI SOC Analyst Assistant.

You now understand:

- ✅ Why applications separate administrator features from analyst features
- ✅ How Streamlit uploads files
- ✅ How to save uploaded PDFs
- ✅ How to display application metrics
- ✅ How to list files dynamically from a directory
- ✅ How to prepare an interface for future functionality

---

# 🧪 Knowledge Check

Can you answer these questions?

- Why do we separate analyst tools from administrator tools?
- What does `st.file_uploader()` do?
- Why do we use `shutil.copyfileobj()`?
- Why is `Path` preferred over manually writing file paths?
- Why is the rebuild button only a placeholder for now?

If you can answer these questions, you've successfully completed the first version of the Administration Panel.

---

# ✅ Checkpoint

🎉 Excellent work!

Your AI SOC Analyst Assistant now includes:

- 🛠 A dedicated Administration Panel
- 📊 Live document count
- 📤 PDF upload capability
- 📚 Dynamic document listing
- 🔄 A rebuild workflow ready for implementation

In the next chapter, you'll connect the **Rebuild Knowledge Base** button to the indexing pipeline, allowing administrators to regenerate the FAISS index directly from the browser with a single click.

---

# 🔄 Chapter 19 – Rebuilding the Knowledge Base from the Web Interface

> **Objective:** Connect the Administration Panel to the indexing pipeline so administrators can rebuild the FAISS knowledge base directly from the Streamlit application without opening a terminal.

---

# 🤔 Why Do We Need a Rebuild Button?

In the previous chapter, administrators could upload new PDF documents.

However, uploading a document alone is **not enough**.

Remember how Retrieval-Augmented Generation (RAG) works.

Simply placing a PDF into the folder does **not** make it searchable.

Instead, every new document must go through the indexing pipeline:

1. Load the PDF
2. Extract text
3. Split into chunks
4. Generate embeddings
5. Build the FAISS index
6. Save the updated index

Only after those steps can the AI retrieve information from the new document.

---

# 🧠 The Difference Between Uploading and Indexing

Uploading a document simply copies it into the project.

```text
PDF

↓

knowledge_base/documents
```

Nothing else happens.

---

Indexing is a completely different process.

```text
PDF

↓

Document Loader

↓

Text Chunker

↓

Embedding Generator

↓

FAISS Index

↓

Saved Index
```

The rebuild button will perform this second workflow.

---

# 🎯 What We'll Build

By the end of this chapter, administrators will be able to:

- 📄 Upload PDFs
- 🔄 Rebuild the FAISS knowledge base
- ⏳ View indexing progress
- ✅ Receive a success message
- 📊 Know when the knowledge base is ready

---

# 🏗 Updated Administration Workflow

```text
Administrator

↓

Upload PDF

↓

Click Rebuild

↓

Load Documents

↓

Chunk Documents

↓

Generate Embeddings

↓

Build FAISS

↓

Save Index

↓

Knowledge Base Ready
```

---

# 📁 Open the Streamlit Application

Open:

```text
frontend/streamlit_app.py
```

---

# 📦 Import the Backend Components

Near the top of the file, add:

```python
from backend.document_loader import DocumentLoader
from backend.text_chunker import TextChunker
from backend.embedding_generator import EmbeddingGenerator
from backend.vector_store import VectorStore
```

These are the same backend components used in your indexing pipeline.

---

# ✍️ Create a Rebuild Function

Above your Streamlit interface, add:

```python
def rebuild_knowledge_base():

    loader = DocumentLoader(
        "knowledge_base/documents"
    )

    documents = loader.load_documents()

    chunker = TextChunker()

    chunks = chunker.chunk_documents(
        documents
    )

    embedding_generator = EmbeddingGenerator()

    embeddings = embedding_generator.generate_embeddings(
        chunks
    )

    vector_store = VectorStore()

    vector_store.build_index(
        embeddings,
        chunks
    )

    vector_store.save(
        "knowledge_base/indexes"
    )
```

Save the file.

---

# 🔍 Understanding This Function

Notice something interesting.

We're **not writing new logic**.

Instead, we're reusing components we've already built.

Professional software development encourages code reuse.

Rather than duplicating code, we simply call existing modules in the correct order.

---

# 🔄 Update the Rebuild Button

Locate the placeholder button from the previous chapter.

Replace it with:

```python
if st.button("🔄 Rebuild Knowledge Base"):

    progress = st.progress(0)

    status = st.empty()

    status.write("Loading documents...")

    progress.progress(20)

    status.write("Building knowledge base...")

    rebuild_knowledge_base()

    progress.progress(100)

    status.success(
        "Knowledge base rebuilt successfully!"
    )

    st.cache_resource.clear()

    st.rerun()
```

Save the file.

---

# 🔍 Understanding the New Code

Let's examine each section.

---

## Progress Bar

```python
progress = st.progress(0)
```

Creates an empty progress bar.

---

## Status Message

```python
status = st.empty()
```

Creates an area that can display changing messages.

For example:

```text
Loading documents...

Building knowledge base...

Knowledge base rebuilt successfully!
```

---

## Rebuild Function

```python
rebuild_knowledge_base()
```

Runs the entire indexing pipeline.

---

## Clearing the Cache

```python
st.cache_resource.clear()
```

Remember that Streamlit cached our RAG Engine.

Without clearing the cache, the application would continue using the old FAISS index.

By clearing the cache, we force Streamlit to reload the updated knowledge base.

---

## Refreshing the Application

```python
st.rerun()
```

Reloads the application using the newly created FAISS index.

---

# ▶️ Run the Application

Open your terminal.

Run:

```powershell
streamlit run frontend/streamlit_app.py
```

---

# 🧪 Testing the Rebuild Process

Try the following workflow.

### Step 1

Upload a new cybersecurity PDF.

---

### Step 2

Verify it appears under:

```text
📚 Current Documents
```

---

### Step 3

Click:

```text
🔄 Rebuild Knowledge Base
```

---

### Step 4

Watch the progress messages.

---

### Step 5

Ask a question related to the newly uploaded document.

If the indexing process completed successfully, the AI should now retrieve information from that document.

---

# ✅ Expected Workflow

```text
Upload PDF

↓

Click Rebuild

↓

Loading Documents...

↓

Building Knowledge Base...

↓

Saving FAISS Index...

↓

Knowledge Base Rebuilt

↓

Ask AI

↓

New Document Can Be Retrieved
```

---

# 💡 Why Clear the Cache?

Earlier, we used:

```python
@st.cache_resource
```

to improve performance.

That cache stores the RAG Engine in memory.

If we rebuild the knowledge base but never clear the cache, the application continues using the old FAISS index.

Clearing the cache ensures the updated index is loaded.

---

# ⚠️ Common Errors

## Error

```text
No documents found.
```

### Cause

The documents folder is empty.

### Solution

Upload one or more PDF documents before rebuilding.

---

## Error

```text
PermissionError
```

### Cause

One or more PDF files are currently open.

### Solution

Close the files and rebuild again.

---

## Error

```text
Model loading is slow.
```

### Cause

Generating embeddings may take time for large document collections.

### Solution

This is expected behavior. Larger knowledge bases require additional processing.

---

## Error

```text
Application still returns old answers.
```

### Cause

The cache wasn't refreshed.

### Solution

Verify that:

```python
st.cache_resource.clear()
```

and

```python
st.rerun()
```

are called after rebuilding.

---

# 📊 Complete Administration Pipeline

```text
Administrator

        │

        ▼

Upload PDF

        │

        ▼

Save File

        │

        ▼

Click Rebuild

        │

        ▼

Load Documents

        │

        ▼

Chunk Documents

        │

        ▼

Generate Embeddings

        │

        ▼

Build FAISS Index

        │

        ▼

Save Index

        │

        ▼

Reload Application

        │

        ▼

Updated Knowledge Base Ready
```

---

# 🎓 What You Learned

Congratulations!

You've completed one of the most important administrative features in the application.

You now understand:

- ✅ Why uploading a PDF isn't enough for RAG
- ✅ How to connect the frontend to the indexing pipeline
- ✅ How to reuse backend components
- ✅ Why cached resources must be refreshed
- ✅ How to provide progress feedback to users during long-running operations

---

# 🧪 Knowledge Check

Can you answer these questions?

- Why doesn't uploading a PDF automatically make it searchable?
- What are the major steps of the indexing pipeline?
- Why do we clear the Streamlit cache after rebuilding?
- What does `st.rerun()` accomplish?
- Why is reusing backend components better than rewriting the indexing logic?

If you can answer these questions, you've successfully connected the Administration Panel to the indexing pipeline.

---

# ✅ Checkpoint

🎉 Outstanding!

Your AI SOC Analyst Assistant now supports:

- 📤 Uploading new cybersecurity PDFs
- 🔄 One-click knowledge base rebuilding
- ⏳ Progress indicators during indexing
- 💾 Automatic FAISS regeneration
- ♻️ Automatic cache refresh
- 🤖 Immediate use of newly indexed documents

In the next chapter, you'll polish the application further by improving the overall user experience with a more professional layout, dashboard metrics, responsive organization, and visual enhancements suitable for a portfolio-quality cybersecurity project.

---

# 🎨 Chapter 20 – Creating a Professional Dashboard Experience

> **Objective:** Transform the AI SOC Analyst Assistant from a functional prototype into a polished, portfolio-ready cybersecurity dashboard by improving the layout, organization, and overall user experience.

---

# 🤔 Why Improve the User Interface?

Imagine you're interviewing two cybersecurity engineers.

Both built the exact same AI assistant.

The first application looks like this:

```text
Question

Answer

Sources
```

The second application looks like this:

```text
🛡 AI SOC Analyst Assistant

------------------------------------------------

System Status

Knowledge Base

Model Information

Response Metrics

Recent Documents

Conversation

Answer

Sources

------------------------------------------------
```

Both applications have identical functionality.

Which one appears more professional?

Most hiring managers would choose the second.

Good software isn't just functional.

It's organized, intuitive, and visually appealing.

---

# 🧠 Why User Experience Matters

Professional cybersecurity analysts spend hours inside dashboards.

Poorly organized applications make investigations slower.

Well-designed dashboards allow analysts to quickly understand:

- System health
- Available resources
- AI status
- Response information
- Supporting documentation

A good dashboard reduces cognitive load.

---

# 🎯 What We'll Build

In this chapter, you'll redesign the interface by adding:

- 📊 Dashboard metrics
- 📑 Multiple tabs
- 📋 Information cards
- 🛡 System status section
- 📚 Knowledge base summary
- 📈 Better organization
- 🎨 Cleaner spacing

---

# 🏗 New Dashboard Layout

```text
----------------------------------------------------------

🛡 AI SOC Analyst Assistant

----------------------------------------------------------

Metrics

Knowledge Base

AI Model

Documents

----------------------------------------------------------

Question Box

----------------------------------------------------------

Tabs

Answer

Sources

Conversation

System Information

----------------------------------------------------------
```

---

# 📁 Open the Streamlit Application

Open:

```text
frontend/streamlit_app.py
```

---

# 📊 Create Dashboard Metrics

Below the application title, add:

```python
metric1, metric2, metric3 = st.columns(3)

with metric1:

    st.metric(

        "Knowledge Base",

        len(pdf_files)

    )

with metric2:

    st.metric(

        "AI Model",

        "Llama 3.2"

    )

with metric3:

    st.metric(

        "Status",

        "Ready"

    )
```

Save the file.

---

# 🔍 Understanding Metrics

Metrics display important information at a glance.

Instead of searching through menus, users immediately know:

- How many documents exist
- Which AI model is active
- Whether the system is ready

Professional dashboards often place key metrics near the top of the page.

---

# 📑 Create Tabs

Replace your existing answer section with:

```python
answer_tab, source_tab, history_tab, system_tab = st.tabs(

    [

        "🤖 Answer",

        "📚 Sources",

        "💬 History",

        "⚙ System"

    ]

)
```

---

# 🔍 Why Use Tabs?

Without tabs:

```text
Answer

Sources

History

System

Everything appears on one long page.
```

With tabs:

```text
🤖 Answer

📚 Sources

💬 History

⚙ System
```

Only one section is visible at a time.

This creates a cleaner interface.

---

# 🤖 Display the AI Response

Inside the Answer tab:

```python
with answer_tab:

    if "result" in locals():

        st.subheader("AI Response")

        st.write(

            result["response"]

        )
```

---

# 📚 Display Sources

Inside the Sources tab:

```python
with source_tab:

    if "result" in locals():

        unique_sources = sorted(

            set(result["sources"])

        )

        if unique_sources:

            for source in unique_sources:

                st.write(

                    f"📄 {source}"

                )

        else:

            st.info(

                "No source documents available."

            )
```

---

# 💬 Move Conversation History into a Tab

Instead of displaying conversation history below the answer, place it inside:

```python
with history_tab:

    if st.session_state.history:

        for conversation in reversed(

            st.session_state.history

        ):

            with st.expander(

                conversation["question"]

            ):

                st.write(

                    conversation["response"]

                )

    else:

        st.info(

            "No conversation history yet."

        )
```

---

# ⚙ Create a System Information Tab

Inside the final tab, add:

```python
with system_tab:

    st.subheader(

        "Application Information"

    )

    st.write(

        "**Application:** AI SOC Analyst Assistant"

    )

    st.write(

        "**Vector Database:** FAISS"

    )

    st.write(

        "**Embedding Model:** all-MiniLM-L6-v2"

    )

    st.write(

        "**Language Model:** llama3.2"

    )

    st.write(

        "**Framework:** Streamlit"

    )
```

---

# 🎨 Add Containers

Around the question input, add:

```python
with st.container():

    st.subheader(

        "Ask a Question"

    )

    question = st.text_input(

        "Enter your cybersecurity question"

    )
```

Containers help visually group related components.

---

# ➖ Add Dividers

Use:

```python
st.divider()
```

between major sections.

This improves readability.

Example:

```python
st.title(...)

st.divider()

Metrics

st.divider()

Question Box

st.divider()

Tabs
```

---

# ▶️ Run the Application

Run:

```powershell
streamlit run frontend/streamlit_app.py
```

---

# ✅ Expected Dashboard

```text
-------------------------------------------------------

🛡 AI SOC Analyst Assistant

Knowledge Base

15

AI Model

Llama 3.2

Status

Ready

-------------------------------------------------------

Ask a Question

[____________________________]

Ask AI

-------------------------------------------------------

🤖 Answer

📚 Sources

💬 History

⚙ System

-------------------------------------------------------
```

The interface should now feel much more organized and easier to navigate.

---

# 💡 Why Organize Information into Tabs?

Imagine a conversation containing dozens of responses and source documents.

Without organization:

```text
Answer

Sources

History

Settings

Answer

Sources

History

...
```

The page becomes difficult to navigate.

Tabs keep related information together while reducing visual clutter.

---

# 💡 Why Display Dashboard Metrics?

Metrics provide an immediate summary of important system information.

For example:

- Number of indexed documents
- Active language model
- Application status

Users can quickly confirm the application's health before asking questions.

---

# ⚠️ Common Errors

## Error

```text
NameError:
pdf_files
```

### Cause

The variable wasn't created before the metrics section.

### Solution

Ensure `pdf_files` is initialized before calling `st.metric()`.

---

## Error

```text
NameError:
result
```

### Cause

The user hasn't submitted a question yet.

### Solution

Guard sections with:

```python
if "result" in locals():
```

to avoid referencing an undefined variable.

---

## Error

Tabs appear empty.

### Cause

No question has been submitted yet.

### Solution

Ask a question first to populate the answer and sources.

---

# 📊 Updated Dashboard Architecture

```text
Browser

        │

        ▼

Dashboard

        │

        ├──────── Metrics

        │

        ├──────── Question Input

        │

        ├──────── Answer Tab

        │

        ├──────── Sources Tab

        │

        ├──────── History Tab

        │

        └──────── System Tab
```

---

# 🎓 What You Learned

Congratulations!

You've redesigned your AI SOC Analyst Assistant into a cleaner, more professional dashboard.

You now understand:

- ✅ How dashboard metrics improve usability
- ✅ Why tabs reduce clutter
- ✅ How containers organize related content
- ✅ Why system information is valuable
- ✅ How thoughtful layout enhances the user experience

---

# 🧪 Knowledge Check

Can you answer these questions?

- Why are dashboard metrics useful?
- What advantage do tabs provide over a single long page?
- Why should system information be visible to users?
- How do containers improve readability?
- Why should related information be grouped together?

If you can answer these questions, you've successfully built a portfolio-quality dashboard.

---

# ✅ Checkpoint

🎉 Congratulations!

Your AI SOC Analyst Assistant now includes:

- 📊 Professional dashboard metrics
- 📑 Tabbed navigation
- 🤖 Organized AI responses
- 📚 Dedicated source document view
- 💬 Conversation history tab
- ⚙️ System information panel
- 🎨 Improved spacing and layout

The application now resembles a modern cybersecurity tool rather than a simple demonstration project.

In the next chapter, you'll focus on **performance optimization**, learning how to reduce startup time, minimize redundant processing, improve caching strategies, and make your AI SOC Analyst Assistant faster and more scalable.

---

# ⚡ Chapter 21 – Optimizing Performance and Resource Usage

> **Objective:** Improve the speed, efficiency, and scalability of the AI SOC Analyst Assistant by applying performance optimization techniques that reduce startup time, minimize redundant processing, and improve the overall user experience.

---

# 🤔 Why Does Performance Matter?

Imagine asking your AI assistant a simple question.

Instead of receiving an answer in two seconds, you wait:

- 20 seconds
- 30 seconds
- 45 seconds

Eventually, users begin wondering if the application has frozen.

Even if the AI provides an excellent answer, poor performance creates a frustrating experience.

Professional software focuses not only on accuracy but also on responsiveness.

---

# 🧠 What Causes Slow AI Applications?

Several operations in our application are computationally expensive.

Examples include:

- Loading the embedding model
- Loading the language model
- Reading PDF files
- Creating embeddings
- Building the FAISS index
- Searching large knowledge bases

Fortunately, many of these tasks only need to happen once.

---

# 🎯 Performance Goals

By the end of this chapter, you'll understand how to:

- ⚡ Reduce startup time
- 🧠 Reuse expensive resources
- 💾 Minimize unnecessary processing
- 📈 Improve scalability
- 🔄 Optimize user experience

---

# 🏗 Where Time Is Spent

Let's review the application's workflow.

```text
Application Starts

↓

Load Embedding Model

↓

Load FAISS Index

↓

Load Ollama Client

↓

Wait for User

↓

Question Asked

↓

Retrieve Chunks

↓

Generate Response
```

Notice that some steps happen once, while others happen for every question.

---

# 🧠 Expensive vs. Inexpensive Operations

## Expensive Operations

These require significant processing time.

- Loading Sentence Transformers
- Building embeddings
- Building FAISS
- Reading hundreds of PDFs

---

## Inexpensive Operations

These complete very quickly.

- Displaying text
- Reading cached objects
- Formatting prompts
- Showing metrics

Our goal is to perform expensive operations only when necessary.

---

# 💾 Using Streamlit Resource Caching

Earlier, we introduced:

```python
@st.cache_resource
```

Let's revisit why it's important.

```python
@st.cache_resource
def load_engine():

    store = VectorStore()

    store.load(
        "knowledge_base/indexes"
    )

    return RAGEngine(store)
```

Without caching:

```text
Refresh Page

↓

Reload FAISS

↓

Reload Embedding Model

↓

Recreate Engine

↓

Wait...
```

With caching:

```text
Refresh Page

↓

Reuse Existing Engine

↓

Ready
```

This dramatically improves responsiveness.

---

# 🔍 Why Cache Resources Instead of Variables?

A normal Python variable disappears whenever Streamlit reruns the application.

Cached resources remain available until:

- the cache is cleared
- the application restarts
- the underlying code changes

This makes caching ideal for large objects such as:

- FAISS indexes
- AI models
- Database connections

---

# 📚 Avoid Rebuilding the Knowledge Base

One common mistake is rebuilding the FAISS index every time the application starts.

Avoid code like this:

```python
loader = DocumentLoader(...)
documents = loader.load_documents()

chunker = TextChunker()
chunks = chunker.chunk_documents(documents)

generator = EmbeddingGenerator()
embeddings = generator.generate_embeddings(chunks)

store = VectorStore()
store.build_index(embeddings, chunks)
```

Doing this on every launch wastes time.

Instead:

- Build the index once.
- Save it to disk.
- Load it when needed.

---

# 💡 Reuse Existing Components

Our architecture is modular.

Instead of creating multiple embedding generators:

```python
EmbeddingGenerator()

EmbeddingGenerator()

EmbeddingGenerator()
```

Create one instance and reuse it whenever possible.

The same principle applies to:

- VectorStore
- OllamaClient
- RAGEngine

Reducing duplicate object creation conserves memory and improves performance.

---

# 📊 Measuring Response Time

Earlier, we displayed how long responses take.

```python
start = time.time()

result = engine.answer(question)

elapsed = time.time() - start
```

Measuring performance allows you to:

- Compare optimizations
- Detect bottlenecks
- Identify regressions after code changes

Performance metrics help you make evidence-based improvements instead of guessing.

---

# 🗂 Reduce Disk Access

Reading files from disk is slower than accessing data already loaded into memory.

Instead of repeatedly opening the same file:

```python
open(file)

open(file)

open(file)
```

Load it once when appropriate and reuse the resulting object.

This principle is especially useful for:

- Configuration files
- Index metadata
- Large datasets

---

# 📈 Think About Scalability

Right now your knowledge base might contain:

```text
15 PDFs
```

But imagine it grows to:

```text
1,500 PDFs
```

Or even:

```text
10,000 PDFs
```

Applications that perform well on small datasets may struggle as the dataset grows.

Designing with scalability in mind helps your application remain responsive as it evolves.

---

# 🧠 Optimize the User Experience

Performance isn't only about raw speed.

It's also about keeping users informed.

For example:

```python
with st.spinner(
    "Searching documentation..."
):
```

Even if a process takes several seconds, users understand that the application is working.

Progress indicators improve perceived performance.

---

# ⚠️ Avoid Premature Optimization

A common saying in software engineering is:

> "Premature optimization is the root of many software problems."

Don't optimize everything immediately.

Instead:

1. Build a working application.
2. Measure performance.
3. Identify bottlenecks.
4. Optimize where it matters most.

This prevents unnecessary complexity.

---

# 💡 Performance Best Practices

As your application grows, keep these practices in mind:

- Cache expensive resources.
- Reuse existing objects.
- Avoid rebuilding indexes unnecessarily.
- Measure response times.
- Display progress indicators.
- Separate indexing from question answering.
- Minimize disk reads when possible.

These habits contribute to applications that are both efficient and maintainable.

---

# ⚠️ Common Performance Mistakes

## Mistake

Rebuilding the FAISS index every time the application starts.

### Better Approach

Build once and reload from disk.

---

## Mistake

Creating multiple embedding models.

### Better Approach

Create one model and reuse it.

---

## Mistake

Loading the RAG Engine repeatedly.

### Better Approach

Use:

```python
@st.cache_resource
```

---

## Mistake

Removing loading indicators.

### Better Approach

Provide users with clear progress feedback during long-running operations.

---

# 📊 Optimized Architecture

```text
Application Starts

        │

        ▼

Load Cached RAG Engine

        │

        ▼

Load FAISS Index

        │

        ▼

Wait for User

        │

        ▼

Question Asked

        │

        ▼

Retrieve Chunks

        │

        ▼

Generate Response

        │

        ▼

Display Answer
```

Notice that expensive initialization occurs once, while user interactions remain lightweight.

---

# 🎓 What You Learned

Congratulations!

You've learned how to improve the responsiveness and scalability of your AI SOC Analyst Assistant.

You now understand:

- ✅ Why caching improves performance
- ✅ Why expensive operations should be minimized
- ✅ How to reuse backend resources
- ✅ Why measuring response times is valuable
- ✅ How good user feedback improves perceived performance
- ✅ Why scalability should be considered early in a project's design

---

# 🧪 Knowledge Check

Can you answer these questions?

- Why is loading an embedding model considered expensive?
- What problem does `@st.cache_resource` solve?
- Why shouldn't the FAISS index be rebuilt every time the application starts?
- Why is measuring response time useful?
- What is the difference between optimizing performance and improving user experience?

If you can answer these questions, you've successfully completed the performance optimization phase of the project.

---

# ✅ Checkpoint

🎉 Excellent work!

Your AI SOC Analyst Assistant now demonstrates many performance practices found in professional AI applications.

The application now includes:

- ⚡ Cached backend resources
- 💾 Efficient FAISS loading
- 📊 Response time monitoring
- 🔄 Reusable backend components
- ⏳ User progress indicators
- 📈 A scalable architecture prepared for larger knowledge bases

In the next chapter, you'll focus on **error handling and application logging**, making the AI SOC Analyst Assistant more resilient by handling failures gracefully, providing meaningful feedback to users, and creating logs that simplify troubleshooting and maintenance.

---

# 🛡️ Chapter 22 – Implementing Error Handling and Application Logging

> **Objective:** Improve the reliability of the AI SOC Analyst Assistant by handling unexpected errors gracefully, providing meaningful feedback to users, and creating application logs that simplify debugging and maintenance.

---

# 🤔 Why Is Error Handling Important?

Imagine you're demonstrating your application during a job interview.

The interviewer asks:

> "What happens if the FAISS index is missing?"

Instead of crashing with a long Python traceback, your application displays:

```text
⚠️ Knowledge base not found.

Please rebuild the knowledge base using the Administration Panel.
```

Which application appears more professional?

Applications will eventually encounter problems.

Professional software anticipates those problems and responds gracefully.

---

# 🧠 What Is Error Handling?

Error handling is the process of detecting problems and responding appropriately.

Instead of allowing the application to crash unexpectedly, we can:

- Detect the error
- Explain what happened
- Suggest how to fix it
- Continue running whenever possible

---

# 🎯 Common Errors in Our Application

Our AI SOC Analyst Assistant may encounter situations such as:

- Missing PDF documents
- Missing FAISS index
- Corrupted index files
- Ollama not running
- Missing AI model
- Invalid user input
- Permission issues
- Unexpected Python exceptions

We'll prepare the application for each of these scenarios.

---

# 🧠 Understanding Exceptions

In Python, many errors are represented as **exceptions**.

For example:

```python
FileNotFoundError
```

occurs when a file cannot be found.

Another example:

```python
PermissionError
```

occurs when the application doesn't have permission to access a file.

Instead of allowing these exceptions to terminate the program, we can handle them.

---

# 📁 Open the Streamlit Application

Open:

```text
frontend/streamlit_app.py
```

We'll improve several sections of the application.

---

# 🛡️ Protect the RAG Engine

Locate the function:

```python
load_engine()
```

Update it like this:

```python
@st.cache_resource
def load_engine():

    try:

        store = VectorStore()

        store.load(
            "knowledge_base/indexes"
        )

        return RAGEngine(store)

    except FileNotFoundError:

        st.error(
            "Knowledge base not found. Please rebuild the index."
        )

        return None

    except Exception as error:

        st.error(
            f"Unexpected error: {error}"
        )

        return None
```

Save the file.

---

# 🔍 Understanding the Code

Notice the structure:

```python
try:

    ...

except:

    ...
```

Python first attempts to execute the code inside the `try` block.

If something goes wrong, execution jumps to the matching `except` block instead of crashing the application.

---

# 🚫 Prevent Questions When the Engine Isn't Available

Immediately after loading the engine, add:

```python
if engine is None:

    st.stop()
```

---

# 🔍 Why Use `st.stop()`?

If the RAG Engine couldn't load successfully, the application shouldn't continue.

Stopping early prevents additional errors later in the program.

---

# 📝 Validate User Input

Locate your question handling logic.

Replace:

```python
if question.strip():
```

with:

```python
if not question.strip():

    st.warning(
        "Please enter a cybersecurity question."
    )

else:

    result = engine.answer(question)
```

This makes the validation easier to read and ensures users receive helpful feedback.

---

# 📋 Add Application Logging

Near the top of the file, import:

```python
import logging
```

Then configure logging:

```python
logging.basicConfig(

    filename="application.log",

    level=logging.INFO,

    format="%(asctime)s - %(levelname)s - %(message)s"

)
```

Save the file.

---

# 🔍 What Is Logging?

Logs are records of important application events.

Examples include:

```text
Application started

Knowledge base loaded

User submitted question

Knowledge base rebuilt

Unexpected error occurred
```

Logs help developers understand what happened before a problem occurred.

---

# 📝 Log User Questions

Before generating an answer, add:

```python
logging.info(

    f"Question received: {question}"

)
```

---

# 📝 Log Successful Responses

After generating the response, add:

```python
logging.info(

    "Response generated successfully."

)
```

---

# 📝 Log Knowledge Base Rebuilds

Inside your rebuild function, after saving the index, add:

```python
logging.info(

    "Knowledge base rebuilt successfully."

)
```

---

# 📝 Log Unexpected Errors

Inside your generic exception block, add:

```python
logging.exception(

    "Unexpected application error."

)
```

The `exception()` method automatically records the full traceback, making debugging much easier.

---

# 📄 Viewing the Log File

After running the application for a while, you'll notice a new file:

```text
application.log
```

Opening it might show something like:

```text
2026-07-24 14:10:12

INFO

Knowledge base rebuilt successfully.

2026-07-24 14:12:35

INFO

Question received: What is phishing?

2026-07-24 14:12:37

INFO

Response generated successfully.
```

These logs create a history of important events.

---

# 🛡️ Why Show Friendly Error Messages?

Compare these two experiences.

### Without Error Handling

```text
Traceback (most recent call last):

...

FileNotFoundError
```

---

### With Error Handling

```text
⚠️ Knowledge base not found.

Please rebuild the knowledge base from the Administration Panel.
```

The second message is far more helpful for users who may not understand Python tracebacks.

---

# ⚠️ What Should We Log?

Good candidates for logging include:

- Application startup
- Knowledge base rebuilds
- User questions
- Successful AI responses
- Errors and exceptions

Avoid logging sensitive information such as:

- Passwords
- API keys
- Personal user information

Thoughtful logging improves troubleshooting while respecting user privacy.

---

# ▶️ Run the Application

Run:

```powershell
streamlit run frontend/streamlit_app.py
```

Ask a few questions.

Rebuild the knowledge base.

Then open:

```text
application.log
```

Verify that new entries have been recorded.

---

# ⚠️ Common Errors

## Error

```text
application.log not created
```

### Cause

No log messages have been written yet.

### Solution

Interact with the application so log entries are generated.

---

## Error

```text
PermissionError
```

### Cause

The log file may already be open in another application with exclusive access.

### Solution

Close the file before running the application again.

---

## Error

Repeated error messages appear.

### Cause

The underlying issue hasn't been resolved.

### Solution

Review both the user-facing message and the log file to determine the root cause.

---

# 📊 Updated Application Architecture

```text
User

        │

        ▼

Streamlit Interface

        │

        ▼

Input Validation

        │

        ▼

RAG Engine

        │

        ├──────── Success

        │             │

        │             ▼

        │      Generate Response

        │

        └──────── Error

                      │

                      ▼

          Friendly Error Message

                      │

                      ▼

             Write to Log File
```

---

# 🎓 What You Learned

Congratulations!

You've made your AI SOC Analyst Assistant much more resilient.

You now understand:

- ✅ Why error handling is essential
- ✅ How `try` and `except` work
- ✅ Why friendly error messages improve usability
- ✅ How application logging simplifies debugging
- ✅ What types of events should be logged
- ✅ Why sensitive information should not be written to log files

---

# 🧪 Knowledge Check

Can you answer these questions?

- Why should applications handle exceptions instead of crashing?
- What is the purpose of `st.stop()`?
- Why is logging valuable during troubleshooting?
- What information should generally not be written to log files?
- Why are user-friendly error messages better than Python tracebacks?

If you can answer these questions, you've successfully improved the reliability and maintainability of your AI SOC Analyst Assistant.

---

# ✅ Checkpoint

🎉 Excellent work!

Your AI SOC Analyst Assistant now includes:

- 🛡️ Graceful error handling
- ⚠️ Friendly user-facing error messages
- 📝 Structured application logging
- 🚫 Input validation
- 🔄 Safe startup behavior
- 📋 Debugging information for developers

The application is now significantly more robust and better prepared for real-world use.

In the next chapter, you'll perform a **complete end-to-end system validation**, verifying that every major component—from document ingestion to AI response generation—works together correctly before preparing the project for GitHub deployment and the comprehensive testing phase in Part C.

---

# 🧪 Chapter 23 – Performing End-to-End System Validation

> **Objective:** Verify that every component of the AI SOC Analyst Assistant works correctly by performing a complete end-to-end validation of the application, from document ingestion to AI-generated responses.

---

# 🤔 Why Perform End-to-End Testing?

Throughout this project, we've tested individual components.

For example:

- Document Loader
- Text Chunker
- Embedding Generator
- Vector Store
- Retriever
- RAG Engine

Each module worked independently.

But professional software engineers also ask an important question:

> **"Do all of these components work correctly together?"**

That is the purpose of end-to-end testing.

---

# 🧠 What Is End-to-End Testing?

End-to-end (E2E) testing verifies an entire application from start to finish.

Instead of testing one module, we test the complete workflow exactly as a real user would.

For our AI SOC Analyst Assistant, that means validating every stage of the RAG pipeline.

---

# 🎯 What We'll Validate

By the end of this chapter, you'll verify:

- ✅ PDF documents load correctly
- ✅ Text is extracted successfully
- ✅ Documents are chunked correctly
- ✅ Embeddings are generated
- ✅ FAISS indexes are built
- ✅ The knowledge base loads
- ✅ Questions retrieve relevant chunks
- ✅ Ollama generates responses
- ✅ The Streamlit interface displays results correctly

---

# 🏗 Complete Application Workflow

```text
PDF Documents

↓

Document Loader

↓

Text Chunker

↓

Embedding Generator

↓

FAISS Index

↓

Retriever

↓

Prompt Builder

↓

Ollama

↓

Browser Interface
```

We'll validate every stage.

---

# 📁 Step 1 – Verify the Knowledge Base

Open:

```text
knowledge_base/documents
```

Confirm that your cybersecurity PDF documents are present.

Example:

```text
MITRE.pdf

OWASP.pdf

NIST.pdf

Incident_Response.pdf
```

If this folder is empty, upload documents before continuing.

---

# 📁 Step 2 – Verify the FAISS Index

Open:

```text
knowledge_base/indexes
```

Confirm the following files exist:

```text
faiss.index

chunks.pkl
```

If either file is missing:

Rebuild the knowledge base from the Administration Panel before continuing.

---

# ▶️ Step 3 – Launch the Application

Open your terminal.

Run:

```powershell
streamlit run frontend/streamlit_app.py
```

The application should start without errors.

---

# ✅ Validation Checklist

Confirm that:

- Application launches successfully
- Sidebar appears
- Dashboard metrics appear
- Administration Panel appears
- Conversation History appears

If all are visible, continue.

---

# 💬 Step 4 – Test Question Submission

Enter:

```text
What is phishing?
```

Click:

```text
Ask AI
```

---

# ✅ Expected Result

The application should:

```text
Searching Documentation...

↓

Retrieve Chunks

↓

Generate Prompt

↓

Generate AI Response

↓

Display Answer
```

---

# 📚 Step 5 – Verify Source Documents

Open the:

```text
📚 Sources
```

tab.

Confirm that:

- Source filenames appear
- Duplicate filenames are removed
- At least one document is displayed

Example:

```text
MITRE.pdf

OWASP.pdf
```

---

# 💬 Step 6 – Verify Conversation History

Open:

```text
💬 History
```

Confirm:

- The question appears
- The answer appears
- Sources remain attached

---

# 🗑 Step 7 – Clear the Conversation

Click:

```text
🗑 Clear Conversation
```

Expected result:

```text
Conversation History

↓

Empty
```

No previous conversations should remain.

---

# 📤 Step 8 – Upload a New Document

Open:

```text
Administration Panel
```

Upload a new cybersecurity PDF.

Verify:

- Upload succeeds
- Document count increases
- Document appears in:

```text
Current Documents
```

---

# 🔄 Step 9 – Rebuild the Knowledge Base

Click:

```text
🔄 Rebuild Knowledge Base
```

Observe:

```text
Loading Documents...

↓

Generating Embeddings...

↓

Building FAISS...

↓

Saving Index...

↓

Completed Successfully
```

---

# 💬 Step 10 – Verify the New Document

Ask a question related to the newly uploaded document.

If the AI answers using that document, the rebuild process worked correctly.

---

# 📋 Step 11 – Verify Application Logs

Open:

```text
application.log
```

Confirm entries such as:

```text
Knowledge base rebuilt successfully.

Question received.

Response generated successfully.
```

---

# ⚡ Step 12 – Verify Performance

Ask several questions.

Observe:

- Response time displays
- Spinner appears
- Application remains responsive
- No crashes occur

---

# 📊 End-to-End Validation Checklist

Use the following checklist to confirm your application is functioning correctly.

| Component | Status |
|-----------|--------|
| Application Starts | ☐ |
| PDFs Loaded | ☐ |
| FAISS Loaded | ☐ |
| Question Submission | ☐ |
| Retrieval | ☐ |
| AI Response | ☐ |
| Sources Display | ☐ |
| Conversation History | ☐ |
| PDF Upload | ☐ |
| Knowledge Base Rebuild | ☐ |
| Logging | ☐ |
| Dashboard | ☐ |

Mark each item as you complete it.

---

# 🔍 What If Something Fails?

Professional developers rarely expect everything to work perfectly on the first attempt.

Instead, they isolate the problem.

Ask questions like:

- Did the PDF upload correctly?
- Was the FAISS index rebuilt?
- Is Ollama running?
- Is the embedding model installed?
- Did the Streamlit cache refresh?
- Are logs reporting an error?

Debugging is much easier when you verify one stage at a time.

---

# 💡 Think Like a Software Tester

Software testing isn't about proving your code works.

It's about trying to discover situations where it doesn't.

For example:

Try asking:

```text
What is quantum mechanics?
```

If your knowledge base doesn't contain that topic, the AI should respond appropriately instead of inventing an answer.

Testing unusual or unexpected inputs helps reveal weaknesses before users encounter them.

---

# ⚠️ Common Problems

## Problem

No response generated.

### Possible Causes

- Ollama isn't running
- Model isn't installed
- Question is empty

---

## Problem

No sources appear.

### Possible Causes

- Empty knowledge base
- Retrieval returned no matching chunks

---

## Problem

Uploaded document isn't searchable.

### Possible Cause

Knowledge base wasn't rebuilt after uploading.

---

## Problem

Old answers continue appearing.

### Possible Cause

The cache wasn't refreshed after rebuilding the knowledge base.

---

# 📊 Complete Validation Workflow

```text
Launch Application

        │

        ▼

Verify Dashboard

        │

        ▼

Ask Question

        │

        ▼

Retrieve Documents

        │

        ▼

Generate AI Response

        │

        ▼

Verify Sources

        │

        ▼

Upload PDF

        │

        ▼

Rebuild Knowledge Base

        │

        ▼

Verify New Retrieval

        │

        ▼

Review Logs

        │

        ▼

System Validated
```

---

# 🎓 What You Learned

Congratulations!

You've performed a complete end-to-end validation of your AI SOC Analyst Assistant.

You now understand:

- ✅ How to verify every stage of the application
- ✅ Why integration testing is essential
- ✅ How to isolate failures during troubleshooting
- ✅ Why logs simplify debugging
- ✅ How to validate updates to the knowledge base
- ✅ Why testing realistic user workflows is important

---

# 🧪 Knowledge Check

Can you answer these questions?

- What is the purpose of end-to-end testing?
- Why should you verify each stage individually?
- Why should uploaded PDFs always be followed by a rebuild?
- Why are logs valuable during testing?
- Why should you intentionally test unexpected questions?

If you can answer these questions, you've successfully validated your AI SOC Analyst Assistant.

---

# ✅ Checkpoint

🎉 Outstanding!

Your AI SOC Analyst Assistant has now been thoroughly validated from beginning to end.

You have confirmed:

- 📄 Document ingestion
- ✂️ Text chunking
- 🧠 Embedding generation
- ⚡ FAISS indexing
- 🔍 Semantic retrieval
- 🤖 AI response generation
- 🌐 Streamlit interface
- 📚 Source transparency
- 📝 Application logging
- 🛠 Administration tools

Your project is now ready for the final preparation stage before moving into **Part C – Testing and Validation**, where you'll perform structured testing, troubleshoot common issues, and validate the application under a wider range of real-world scenarios.

---

# 🚀 Chapter 24 – Preparing the Project for GitHub

> **Objective:** Organize, clean, and prepare your AI SOC Analyst Assistant for publication on GitHub by following professional software development practices that make your project easier to understand, easier to maintain, and more impressive to employers.

---

# 🤔 Why Prepare a Project Before Publishing?

Imagine you're a hiring manager reviewing two GitHub repositories.

The first repository contains:

```text
test.py

new.py

old.py

test2.py

final_final.py

random_notes.txt
```

There is no organization.

No documentation.

No screenshots.

No explanation.

---

The second repository contains:

```text
README.md

docs/

backend/

frontend/

tests/

knowledge_base/

screenshots/

requirements.txt

.gitignore
```

Everything is organized.

Documentation is complete.

The project is easy to understand.

Which project leaves a better impression?

The second one.

Professional presentation demonstrates attention to detail.

---

# 🧠 Your GitHub Repository Is Your Portfolio

When employers review your GitHub profile, they're evaluating more than your code.

They're also looking for:

- Organization
- Documentation
- Maintainability
- Professionalism
- Consistency

A clean repository communicates that you care about software quality.

---

# 🎯 Goals for This Chapter

By the end of this chapter, you'll:

- 🧹 Remove unnecessary files
- 📂 Verify your folder structure
- 📄 Review your documentation
- 📸 Capture application screenshots
- 🚫 Configure `.gitignore`
- 📦 Prepare your project for publication

---

# 📁 Review the Project Structure

Your project should now resemble:

```text
AI-SOC-Assistant/

│

├── backend/

├── frontend/

├── knowledge_base/

│   ├── documents/

│   └── indexes/

├── tests/

├── docs/

├── screenshots/

│

├── app.py

├── requirements.txt

├── README.md

├── .gitignore

└── application.log
```

If your structure differs significantly, take a moment to organize the files before continuing.

---

# 🧹 Remove Temporary Files

During development, it's common to create temporary files.

Examples include:

```text
test.py

scratch.py

notes.txt

old_code.py

example.py
```

If these files are no longer needed, remove them before publishing.

Keeping only relevant files helps others navigate your project more easily.

---

# 📄 Review Documentation

Verify that your documentation is complete.

Your `docs` folder should contain:

```text
Part-A-Install-and-Run.md

Part-B-Build-From-Scratch.md

Part-C-Testing-and-Validation.md

Part-D-GitHub-Deployment-and-Troubleshooting.md
```

Open each file and ensure:

- Markdown formatting is correct
- Headings are organized
- Code blocks display properly
- Links work as expected

Documentation is often the first thing visitors read.

---

# 📸 Capture Application Screenshots

Screenshots help readers quickly understand what your application looks like.

Launch your application:

```powershell
streamlit run frontend/streamlit_app.py
```

Capture screenshots of important features.

Suggested screenshots include:

- Main dashboard
- Sidebar
- Conversation history
- Source documents
- Administration panel
- Knowledge base rebuild
- Successful AI response

Save them inside:

```text
screenshots/
```

Example:

```text
dashboard.png

conversation-history.png

sources.png

admin-panel.png

knowledge-base-rebuild.png
```

These images can later be referenced in your `README.md`.

---

# 🚫 Configure `.gitignore`

Open:

```text
.gitignore
```

Review its contents.

A good `.gitignore` prevents unnecessary files from being committed.

Example:

```gitignore
# Python

__pycache__/

*.pyc

# Virtual Environment

.venv/

venv/

# Logs

application.log

# Streamlit

.streamlit/

# Operating System

.DS_Store

Thumbs.db

# IDE

.vscode/

.idea/

# FAISS Index

knowledge_base/indexes/*.index

knowledge_base/indexes/*.pkl
```

---

# 🔍 Why Ignore Certain Files?

Some files should not be stored in Git because they are:

- Automatically generated
- Machine-specific
- Temporary
- Large
- Rebuildable

For example:

```text
application.log
```

is recreated every time the application runs.

There's no need to version control it.

---

# 📦 Verify `requirements.txt`

Open:

```text
requirements.txt
```

Ensure it contains only packages required to run the project.

Remove:

- Unused libraries
- Duplicate entries
- Experimental dependencies

A clean dependency list makes installation easier for others.

---

# 📝 Review Your README

Open:

```text
README.md
```

Confirm it includes:

- Project overview
- Features
- Architecture
- Installation instructions
- Screenshots
- Folder structure
- Technologies used
- Future improvements
- License information (if applicable)

A strong README is often the deciding factor for whether someone explores your project further.

---

# 🧪 Perform One Final Test

Before publishing, complete one final validation.

Verify:

- Application starts successfully
- Knowledge base loads
- AI answers questions
- Source documents appear
- Conversation history works
- Administration Panel works
- Knowledge base rebuild succeeds
- No unexpected errors appear

Publishing a project that you've personally tested demonstrates professionalism.

---

# 📋 Final Repository Checklist

Before uploading to GitHub, confirm the following.

| Item | Complete |
|------|----------|
| Project builds successfully | ☐ |
| Documentation complete | ☐ |
| README reviewed | ☐ |
| Screenshots added | ☐ |
| `.gitignore` reviewed | ☐ |
| Temporary files removed | ☐ |
| Application tested | ☐ |
| Folder structure organized | ☐ |

Complete each item before publishing.

---

# 💡 Think Like an Open Source Maintainer

Imagine someone discovers your project six months from now.

They know nothing about you.

Could they:

- Understand the project?
- Install it?
- Run it?
- Learn from it?
- Contribute improvements?

If the answer is yes, you've created a repository that others can successfully use.

---

# ⚠️ Common Mistakes Before Publishing

## Mistake

Uploading the virtual environment.

### Better Approach

Exclude:

```text
.venv/
```

using `.gitignore`.

---

## Mistake

Including application log files.

### Better Approach

Ignore:

```text
application.log
```

---

## Mistake

Publishing unused experimental files.

### Better Approach

Remove them before committing.

---

## Mistake

Forgetting screenshots.

### Better Approach

Include several screenshots that demonstrate the application's functionality.

---

## Mistake

Skipping a final test.

### Better Approach

Always verify that the project still works immediately before publishing.

---

# 📊 Publishing Workflow

```text
Complete Development

        │

        ▼

Clean Repository

        │

        ▼

Review Documentation

        │

        ▼

Capture Screenshots

        │

        ▼

Verify Dependencies

        │

        ▼

Run Final Tests

        │

        ▼

Commit to Git

        │

        ▼

Publish to GitHub
```

---

# 🎓 What You Learned

Congratulations!

You've learned how to prepare a software project for public release.

You now understand:

- ✅ Why repository organization matters
- ✅ How to clean development artifacts
- ✅ Why screenshots improve documentation
- ✅ What belongs in `.gitignore`
- ✅ Why a polished README is important
- ✅ How to perform a final release review

---

# 🧪 Knowledge Check

Can you answer these questions?

- Why shouldn't virtual environments be committed to Git?
- Why are screenshots valuable in a GitHub repository?
- What types of files belong in `.gitignore`?
- Why should temporary development files be removed?
- Why is a final validation important before publishing?

If you can answer these questions, you're ready to complete Part B.

---

# ✅ Checkpoint

🎉 Congratulations!

You have successfully completed the development phase of your AI SOC Analyst Assistant.

Your project now includes:

- 🛡️ A complete Retrieval-Augmented Generation (RAG) backend
- 🌐 A professional Streamlit dashboard
- 📚 A searchable cybersecurity knowledge base
- 🤖 Local AI-powered question answering with Ollama
- 🛠️ Administration tools for managing documents
- ⚡ Performance optimizations
- 📝 Error handling and logging
- 📖 Comprehensive documentation
- 🚀 A GitHub-ready project structure

In the next and final chapter of Part B, you'll review everything you've built, revisit the major architectural concepts, and prepare to transition into **Part C – Testing and Validation**, where you'll systematically test, troubleshoot, and validate every component of the application under realistic conditions.

---

# 🎓 Chapter 25 – Part B Final Review and Architecture Recap

> **Objective:** Review everything you've built throughout Part B, reinforce the major architectural concepts behind the AI SOC Analyst Assistant, and prepare for Part C by understanding how all of the application's components work together.

---

# 🎉 Congratulations!

If you've reached this chapter, you've accomplished something significant.

You didn't simply build an AI chatbot.

You designed and implemented a complete Retrieval-Augmented Generation (RAG) application capable of:

- Reading cybersecurity documentation
- Creating semantic embeddings
- Building a searchable vector database
- Retrieving relevant information
- Generating grounded AI responses
- Presenting everything through a professional web interface

This is the same architectural pattern used by many modern enterprise AI applications.

Take a moment to appreciate how much you've learned.

---

# 🧠 Looking Back at the Journey

When you began Part B, your project contained little more than an empty folder.

Now it has become a complete software application.

Let's revisit that journey.

---

# 🏗 Step 1 – Project Structure

You learned how to organize a professional Python project.

Your repository now contains clearly separated components.

```text
backend/

frontend/

knowledge_base/

tests/

docs/

screenshots/
```

Good organization makes software easier to understand, maintain, and expand.

---

# 📄 Step 2 – Document Processing

You built a system capable of loading cybersecurity PDFs.

```text
PDF Documents

↓

Extract Text

↓

Store in Memory
```

Without document ingestion, the AI would have no knowledge to retrieve.

---

# ✂️ Step 3 – Text Chunking

Large documents were divided into smaller sections.

```text
Long Document

↓

Smaller Chunks

↓

Semantic Search
```

Chunking improves retrieval accuracy and ensures language models receive manageable amounts of context.

---

# 🧠 Step 4 – Embedding Generation

Every text chunk was converted into a numerical representation.

```text
Text

↓

Embedding

↓

Vector
```

These embeddings allow the application to search based on meaning rather than exact wording.

---

# ⚡ Step 5 – FAISS Vector Database

Instead of searching raw text, your application searches vectors.

```text
Embeddings

↓

FAISS

↓

Fast Similarity Search
```

This enables efficient retrieval even as the knowledge base grows.

---

# 🔍 Step 6 – Retrieval

When a user asks a question:

```text
Question

↓

Embedding

↓

Similarity Search

↓

Relevant Chunks
```

The Retriever identifies the most relevant pieces of documentation.

---

# 📝 Step 7 – Prompt Engineering

Retrieved chunks are combined with the user's question.

```text
Question

+

Retrieved Context

↓

Prompt
```

The prompt instructs the AI to answer using only the supplied documentation.

This helps reduce hallucinations.

---

# 🤖 Step 8 – Ollama

The completed prompt is sent to the local language model.

```text
Prompt

↓

Ollama

↓

Generated Response
```

Because the model runs locally, the application can operate without relying on external AI services.

---

# 🌐 Step 9 – Streamlit

You transformed the backend into a browser-based application.

Users can now:

- Ask questions
- View answers
- Review source documents
- Manage the knowledge base

All through a clean graphical interface.

---

# 🛠 Step 10 – Administration Tools

You built tools that allow administrators to:

- Upload PDFs
- View document counts
- Monitor the knowledge base
- Rebuild the FAISS index

This separated operational tasks from everyday analyst workflows.

---

# ⚡ Step 11 – Performance Improvements

You optimized the application by:

- Caching expensive resources
- Reusing backend components
- Measuring response times
- Avoiding unnecessary rebuilding

These improvements make the application more responsive and scalable.

---

# 🛡 Step 12 – Reliability

Finally, you improved reliability through:

- Error handling
- Logging
- Input validation
- User-friendly messages

Professional software doesn't simply work—it also handles failures gracefully.

---

# 🏗 The Complete Architecture

Your application now follows this complete workflow.

```text
Cybersecurity PDFs

        │

        ▼

Document Loader

        │

        ▼

Text Chunker

        │

        ▼

Embedding Generator

        │

        ▼

FAISS Vector Database

        │

        ▼

Retriever

        │

        ▼

Prompt Builder

        │

        ▼

Ollama

        │

        ▼

RAG Engine

        │

        ▼

Streamlit Dashboard

        │

        ▼

Cybersecurity Analyst
```

Every component has a clearly defined responsibility.

This separation of concerns makes the application easier to test, maintain, and extend.

---

# 📚 Major Concepts You've Learned

Throughout Part B, you've explored several important topics in modern AI application development.

These include:

- Python project organization
- Virtual environments
- PDF processing
- Semantic chunking
- Sentence embeddings
- Vector databases
- Retrieval-Augmented Generation (RAG)
- Prompt engineering
- Local language models
- Streamlit web development
- Application architecture
- Performance optimization
- Error handling
- Logging
- User experience design

These concepts form the foundation of many enterprise AI systems.

---

# 🧠 Think Like a Software Engineer

One of the most valuable lessons from this project isn't a specific library or framework.

It's learning how to think about software as a collection of independent components that work together.

Instead of writing one large script, you built specialized modules with clear responsibilities.

This modular approach makes your application easier to understand, easier to test, and easier to improve over time.

---

# 🧪 Are You Ready for Part C?

Before continuing, ask yourself the following questions.

Can you explain:

- What Retrieval-Augmented Generation (RAG) is?
- Why embeddings are necessary?
- How FAISS performs semantic search?
- Why prompt engineering matters?
- Why indexing and retrieval are separate workflows?
- Why caching improves performance?
- How the Streamlit frontend communicates with the backend?

If you can confidently answer these questions, you're ready to begin Part C.

---

# 📋 Final Part B Checklist

Before moving on, verify the following.

| Task | Complete |
|------|----------|
| Project structure created | ☑ |
| Dependencies installed | ☑ |
| Virtual environment configured | ☑ |
| Document Loader completed | ☑ |
| Text Chunker completed | ☑ |
| Embedding Generator completed | ☑ |
| FAISS Vector Store completed | ☑ |
| Retriever completed | ☑ |
| Prompt Builder completed | ☑ |
| Ollama Client completed | ☑ |
| RAG Engine completed | ☑ |
| Indexing pipeline completed | ☑ |
| Streamlit interface completed | ☑ |
| Administration panel completed | ☑ |
| Performance optimization completed | ☑ |
| Error handling completed | ☑ |
| End-to-end validation completed | ☑ |
| GitHub preparation completed | ☑ |

If every item is complete, you've successfully finished Part B.

---

# 🎓 What You Accomplished

Congratulations!

By completing Part B, you've built a fully functional AI-powered cybersecurity assistant from the ground up.

Your application now demonstrates:

- 📄 Document ingestion
- ✂️ Intelligent text chunking
- 🧠 Semantic embedding generation
- ⚡ High-speed vector search with FAISS
- 🔍 Retrieval-Augmented Generation (RAG)
- 🤖 Local AI inference using Ollama
- 🌐 Interactive Streamlit dashboard
- 📚 Source transparency
- 🛠 Administration tools
- ⚡ Performance optimization
- 🛡 Reliable error handling
- 📝 Application logging
- 🚀 GitHub-ready project organization

This is a substantial software engineering achievement and an excellent addition to your portfolio.

---

# 🚀 Looking Ahead to Part C

Building software is only one part of the software development lifecycle.

Professional engineers also verify that their software behaves correctly under normal conditions, unexpected inputs, and failure scenarios.

In **Part C – Testing and Validation**, you'll learn how to:

- 🧪 Test every backend component
- 🌐 Validate the Streamlit interface
- 📄 Verify document ingestion
- 🔍 Measure retrieval accuracy
- 🤖 Evaluate AI-generated responses
- ⚠️ Reproduce and troubleshoot common failures
- 📊 Perform structured system validation
- ✅ Confirm that every feature works as intended

Rather than adding new functionality, Part C focuses on ensuring that everything you've built is dependable, maintainable, and ready for real-world use.

---

# 🎉 Congratulations on Completing Part B!

You have successfully designed, implemented, and documented a complete AI-powered Retrieval-Augmented Generation application.

Take a moment to celebrate your progress.

Then, when you're ready, continue to **Part C – Testing and Validation**, where you'll validate every component of your AI SOC Analyst Assistant with the same level of detail and professionalism that guided its development.
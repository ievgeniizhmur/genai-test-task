# 🧠 News Assistant

## 📘 Description

**News Assistant** is an intelligent analyzer for news articles scraped from the web.  
Currently, it supports parsing and semantic processing of news articles from **TSN.ua**.

The application uses vector search and OpenAI-powered language models to extract summaries, topics, and context-aware answers from raw news content.

---

## 📋 Prerequisites

Before you install the application, ensure the following are set up:

- **Python** version `3.12.5`  
  ⚠️ Do **not** use version `3.13` or higher — compatibility is not guaranteed.
- **Poetry** — a tool for managing Python dependencies and virtual environments.

---

## 🛠 Installing Prerequisites

### 1. 🐍 Install Python 3.12.5

- Download from the official Python site:  
  https://www.python.org/downloads/release/python-3125/
- During installation:
  - ✅ Check **"Add Python to PATH"**
  - ✅ Use "Customize installation" → Enable **`pip`** and **environment variables**
- Confirm installation:

```bash
python --version
```

> You should see: `Python 3.12.5`

### 2. ⚙️ (Optional) Configure Environment Variables

If the `python` or `pip` commands are not recognized, manually add the following to your system's `PATH`:

```
C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python312\
C:\Users\<YourUsername>\AppData\Local\Programs\Python\Python312\Scripts\
```

### 3. 📦 Install Poetry via pip

Use the following command:

```bash
pip install poetry
```

After installation, verify:

```bash
poetry --version
```

---

## 📦 How to Install the Application

# 0. 📥 Clone the Project

First, clone the repository to your local machine using `git`:

```bash
git clone https://github.com/ievgeniizhmur/genai-test-task.git

1. **Navigate to the project’s root folder** — the one that contains `pyproject.toml`:
<Your repo location>\genai-test-task\news-assistant

2. **Install dependencies** with Poetry:

```bash
poetry install
```

> This command will:
> - Create a virtual environment
> - Install all dependencies specified in `pyproject.toml`
> - Lock versions to ensure reproducibility

3. **Set up your OpenAI API Key**

The project expects an `.env` file in the project root directory with the following environment variable:

```
OPENAI_API_KEY=your_openai_key_here
```
> Replace `your_openai_key_here` with your actual OpenAI key.  
---

## 🚀 How to Run the Application

To run the application, use the following command from the project root:

```bash 
poetry run start
```

## 📖 How to Use

> ⏳ **Note:** On the very first run, the application may take some time to initialize.  
> This is expected, as it needs to:
> - Download and prepare language model components
> - Set up local storage (e.g., initialize the vector database)
> - Resolve and activate dependencies

Once the application is running (via `poetry run start`), you will be prompted to select an operation from the menu:
=====================================
Select operation:
1 - Load news article from tsn.ua URL
2 - Load news from URls file (resources/urls.txt)
3 - AI powered search for news

Developer menu:
5 - Semantic search in DB
6 - Clean DB

0 - Exit
====================================

### 🔹 1 — Load news article from tsn.ua URL

Prompts you to enter a single TSN.ua article URL.  
For example: https://tsn.ua/en/ato/russia-deploys-elite-uav-units-to-donetsk-region-what-threats-this-poses-2853032.html
The application will:

- Download the article
- Generate a summary using an AI model
- Extract relevant topics
- Store the full content, summary, and metadata into the vector database

### 🔹 2 — Load news from URLs file

Loads multiple TSN.ua article URLs from a text file.  
Each URL is processed one by one in sequence:

- Content is downloaded and analyzed
- Data is stored in the vector database

> File location: `resources/urls.txt`  
> You can customize this file if needed

### 🔹 3 — AI powered search for news

> ⚠️ **Note:** Since the vector database is initially empty, it is recommended to first run option **2** and preload data from URLs in the `.txt` file.  
> This ensures that the AI assistant has relevant content to search through.  
>  
> 💬 **Example query:**  
> `What is currently happening in Ukraine?`

Allows you to enter a natural language question (e.g., “What caused the recent protests?”).  
The assistant will:

- Search the semantic database for the most relevant articles
- Use a language model to generate an answer
- Return both the AI-generated answer and the list of articles it used as sources

### 🛠 Developer Menu

#### 🔹 5 — Semantic search in DB

Performs a raw vector-based semantic search.  
Returns documents from the database that are most relevant to your search query, without asking the AI to generate a summary or answer.

#### 🔹 6 — Clean DB

Deletes all entries in the vector database.  
⚠️ This operation is **irreversible** and should be used with caution.

### 🔹 0 — Exit

Closes the application.

## 🔧 Configuration

The application supports configuration via a `config.yaml` file located in the project root directory.

Here is an example of a valid configuration file:

```yaml
llm:
  verbose: False
vectorstore:
  search_docs_number: 5
ai_assistant:
  articles_number: 5
```

### 🧩 Parameter Overview

| Key                          | Description                                                                                       |
|-----------------------------|---------------------------------------------------------------------------------------------------|
| `llm.verbose`               | Enables debug output of the full prompt sent to the language model. Useful for debugging.         |
| `vectorstore.search_docs_number` | Number of documents returned in **semantic search** (Menu option 5).                             |
| `ai_assistant.articles_number`   | Number of articles passed to the AI assistant (Menu option 3). ⚠️ Use carefully to avoid token overflows. |
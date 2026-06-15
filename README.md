<<<<<<< HEAD
# 🔍 Log Analyzer & Incident Report Generator

An AI-powered REST API that analyzes application log files and generates structured incident reports using **RAG (Retrieval Augmented Generation)**, **LangChain**, and **Azure OpenAI**.

---

## 💡 How It Works

```
Upload Log File
      ↓
Split into chunks (LangChain TextSplitter)
      ↓
Create embeddings (Azure OpenAI Embeddings)
      ↓
Store in ChromaDB (Vector Database)
      ↓
Query: Find relevant chunks (Similarity Search)
      ↓
Send context to Azure OpenAI (LLM)
      ↓
Get structured Incident Report
```

---

## 🚀 Tech Stack

| Technology | Purpose |
|---|---|
| **FastAPI** | REST API framework |
| **LangChain** | RAG pipeline orchestration |
| **Azure OpenAI** | LLM for report generation |
| **ChromaDB** | Vector database for embeddings |
| **Pydantic** | Data validation |
| **Docker** | Containerization |

---

## 📌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/analyze/upload` | Upload log file, get session_id |
| POST | `/analyze/ask` | Ask question about the log |
| POST | `/analyze/report` | Generate full incident report |
| GET | `/analyze/sessions` | List active sessions |

---

## ⚡ Quick Start

```bash
# 1. Clone repo
git clone https://github.com/SaranyaMulagani/log-analyzer-api.git
cd log-analyzer-api

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment
cp .env.example .env
# Edit .env — add your Azure OpenAI keys

# 5. Run
uvicorn main:app --reload
```

Visit: **http://localhost:8000/docs**

---

## 🧪 Test with Sample Log

A sample log file `sample_log.txt` is included. Test flow:

1. `POST /analyze/upload` — upload `sample_log.txt`
2. Copy the `session_id` from response
3. `POST /analyze/ask` — ask "What errors occurred?"
4. `POST /analyze/report` — generate full incident report

---

## 📊 Sample Incident Report Output

```json
{
  "session_id": "a1b2c3d4",
  "filename": "app.log",
  "severity_level": "HIGH",
  "error_summary": "Database connection timeouts followed by application crash",
  "root_cause_analysis": "Primary failure: PostgreSQL database became unreachable...",
  "recommended_actions": [
    "Increase database connection pool size",
    "Implement circuit breaker pattern",
    "Add database health monitoring alerts"
  ]
}
```

---

## 👩‍💻 Author

**Mulagani Saranya** — Python Developer | Gen AI Specialist  
Built as part of Gen AI portfolio: github.com/SaranyaMulagani
=======
# log-analyzer-api
>>>>>>> 12450b55fa282405bbd341f33cf35b4d87a4e697

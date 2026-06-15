from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import analyze

app = FastAPI(
    title="Log Analyzer & Incident Report Generator",
    description="""
    Upload log files and get AI-powered incident reports.
    
    ## How it works
    1. Upload a log file (.txt or .log)
    2. The system chunks and embeds the log content
    3. RAG pipeline extracts errors and patterns
    4. Azure OpenAI generates a structured incident report
    
    ## Tech Stack
    - FastAPI + LangChain + Azure OpenAI + ChromaDB
    """,
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Log Analyzer & Incident Report Generator API",
        "docs": "/docs",
        "endpoints": {
            "upload_and_analyze": "POST /analyze/upload",
            "ask_question":       "POST /analyze/ask",
            "get_report":         "POST /analyze/report"
        }
    }


@app.get("/health", tags=["Root"])
def health():
    return {"status": "healthy"}

import uuid
import os
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
import schemas
import rag_engine

router = APIRouter(prefix="/analyze", tags=["Log Analysis"])

# In-memory store: session_id → {filename, chunks, log_text}
# In production use Redis or a database
sessions = {}


@router.post(
    "/upload",
    response_model=schemas.UploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a log file for analysis"
)
async def upload_log_file(file: UploadFile = File(...)):
    """
    Upload a .txt or .log file.
    
    The system will:
    1. Read the file content
    2. Split into chunks
    3. Create embeddings
    4. Store in ChromaDB
    5. Return a session_id to use for queries
    """
    # Validate file type
    if not file.filename.endswith((".txt", ".log")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .txt and .log files are supported"
        )

    # Read file content
    content = await file.read()
    try:
        log_text = content.decode("utf-8")
    except UnicodeDecodeError:
        log_text = content.decode("latin-1")

    if not log_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is empty"
        )

    # Generate unique session ID for this upload
    session_id = str(uuid.uuid4())[:8]

    # Chunk the log text
    chunks = rag_engine.chunk_log_text(log_text)

    # Store in ChromaDB
    rag_engine.store_in_vectordb(chunks, session_id)

    # Save session info
    sessions[session_id] = {
        "filename": file.filename,
        "log_text": log_text,
        "total_chunks": len(chunks)
    }

    return {
        "message":      "Log file uploaded and processed successfully",
        "session_id":   session_id,
        "filename":     file.filename,
        "total_chunks": len(chunks),
        "hint":         f"Use session_id '{session_id}' to ask questions or generate report"
    }


@router.post(
    "/ask",
    response_model=schemas.QuestionResponse,
    summary="Ask a question about the uploaded log"
)
def ask_question(request: schemas.QuestionRequest):
    """
    Ask any question about the uploaded log file.
    
    Example questions:
    - "What errors occurred in the log?"
    - "How many connection timeouts were there?"
    - "What is the most frequent error?"
    - "Which service failed first?"
    
    Requires the session_id from the upload response.
    """
    if request.session_id not in sessions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session '{request.session_id}' not found. Please upload a log file first."
        )

    try:
        answer = rag_engine.ask_question(request.question, request.session_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing question: {str(e)}"
        )

    return {
        "question":   request.question,
        "answer":     answer,
        "session_id": request.session_id
    }


@router.post(
    "/report",
    summary="Generate a full incident report"
)
def generate_report(session_id: str):
    """
    Generate a complete structured incident report for the uploaded log.
    
    The report includes:
    - Error summary
    - Root cause analysis
    - Recommended actions
    - Overall severity level
    
    Requires the session_id from the upload response.
    """
    if session_id not in sessions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Session '{session_id}' not found. Please upload a log file first."
        )

    session = sessions[session_id]

    try:
        report = rag_engine.generate_incident_report(
            log_text=session["log_text"],
            session_id=session_id,
            filename=session["filename"]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating report: {str(e)}"
        )

    return report


@router.get(
    "/sessions",
    summary="List all active sessions"
)
def list_sessions():
    """List all uploaded log file sessions"""
    return {
        "active_sessions": [
            {
                "session_id":   sid,
                "filename":     info["filename"],
                "total_chunks": info["total_chunks"]
            }
            for sid, info in sessions.items()
        ]
    }

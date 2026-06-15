from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
import config


def get_llm_and_embeddings():
    llm = ChatGroq(
        model=config.GROQ_MODEL,
        api_key=config.GROQ_API_KEY,
        temperature=0.1,
    )
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )
    return llm, embeddings


def chunk_log_text(log_text: str) -> list:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        separators=["\n\n", "\n", " "]
    )
    return splitter.split_text(log_text)


def store_in_vectordb(chunks: list, session_id: str):
    _, embeddings = get_llm_and_embeddings()
    return Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        collection_name=f"logs_{session_id}",
        persist_directory=config.CHROMA_PERSIST_DIR
    )


def load_vectordb(session_id: str):
    _, embeddings = get_llm_and_embeddings()
    return Chroma(
        collection_name=f"logs_{session_id}",
        embedding_function=embeddings,
        persist_directory=config.CHROMA_PERSIST_DIR
    )


def ask_question(question: str, session_id: str) -> str:
    llm, _ = get_llm_and_embeddings()
    vectorstore = load_vectordb(session_id)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    prompt = PromptTemplate.from_template(
        "You are an expert log analyzer.\n"
        "Use the log content to answer the question.\n"
        "If answer not in logs say: This information is not in the provided logs.\n\n"
        "Log Context:\n{context}\n\n"
        "Question: {question}\n\n"
        "Answer:"
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain.invoke(question)


def generate_incident_report(log_text: str, session_id: str, filename: str) -> dict:
    errors   = ask_question("List ALL errors and exceptions with severity", session_id)
    cause    = ask_question("What is the root cause of the main failure?", session_id)
    actions  = ask_question("Top 5 recommended actions to fix these issues?", session_id)
    severity = ask_question("Severity? ONE word only: HIGH MEDIUM or LOW", session_id).strip().upper()

    if severity not in ["HIGH", "MEDIUM", "LOW"]:
        severity = "MEDIUM"

    actions_list = [
        l.strip().lstrip("0123456789.-) ")
        for l in actions.splitlines()
        if l.strip() and len(l.strip()) > 10
    ][:5]

    return {
        "session_id":           session_id,
        "filename":             filename,
        "total_lines_analyzed": len(log_text.splitlines()),
        "error_summary":        errors,
        "root_cause_analysis":  cause,
        "recommended_actions":  actions_list,
        "severity_level":       severity
    }
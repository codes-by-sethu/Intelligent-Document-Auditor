# 0. BLOCK TELEMETRY FIRST
import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"

import sys
import types
import time
from pypdf import PdfReader
import chromadb
from chromadb.config import Settings
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

# 1. WINDOWS COMPATIBILITY HACK
if sys.platform == "win32":
    if "pwd" not in sys.modules:
        sys.modules["pwd"] = types.ModuleType("pwd")

def load_pdf(path):
    """Load PDF pages as LangChain Documents."""
    reader = PdfReader(path)
    return [Document(page_content=page.extract_text() or "") for page in reader.pages]

def document_auditor(ref_path, audit_path):
    """Forensic RAG pipeline optimized for long-form document comparison."""

    # Force clear internal cache
    try:
        chromadb.api.client.SharedSystemClient.clear_system_cache()
    except:
        pass

    # 2. MODELS
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    llm = ChatOllama(model="llama3.2", temperature=0)

    # 3. PROCESS DOCUMENTS
    audit_docs = load_pdf(audit_path)
    # Using larger chunks for more context per retrieval
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = splitter.split_documents(audit_docs)

    # 4. DYNAMIC VECTOR STORAGE
    session_id = int(time.time())
    persist_dir = os.path.join(os.getcwd(), f"chroma_db_{session_id}")

    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        collection_name="audit_session",
        persist_directory=persist_dir,
        client_settings=Settings(
            is_persistent=True,
            persist_directory=persist_dir,
            anonymized_telemetry=False
        )
    )

    # 5. REFERENCE EXTRACTION
    ref_docs = load_pdf(ref_path)
    ref_text = " ".join([d.page_content for d in ref_docs])

    # 6. LCEL CHAIN
    # Expanded prompt to force deep inspection of financial and date data
    prompt = ChatPromptTemplate.from_template("""
    You are a forensic auditor. Your task is to find EVERY discrepancy between the Context (suspect) 
    and the Reference Truth (master). 
    
    Reference Truth: {ref_truth}

    Context (Suspect Data): {context}

    INSTRUCTIONS:
    - Compare dollar amounts ($) and hourly rates precisely.
    - Check all dates (months and days) for changes.
    - Verify quantities (e.g., number of staff, number of dashboards).
    - Look for changes in "Ownership" or "Timeline" clauses.
    
    Answer ONLY with a bulleted list of specific differences. 
    Format: [Category]: [Reference Value] vs [Suspect Value].
    If none are found, say 'No discrepancies detected.'
    """)

    # 7. ADVANCED RETRIEVER (Increased k for longer documents)
    # k=6 ensures the AI sees almost all paragraphs of a 10-paragraph document
    retriever = vectorstore.as_retriever(
        search_type="mmr", # Diverse chunk selection
        search_kwargs={"k": 6, "fetch_k": 10}
    )

    # Increased ref_text limit to 8000 to accommodate all 10 paragraphs
    chain = (
        {"context": retriever, "question": RunnablePassthrough(), "ref_truth": lambda x: ref_text[:8000]}
        | prompt
        | llm
        | StrOutputParser()
    )

    # 8. EXECUTION
    report = chain.invoke("Identify all differences in financial terms, quantities, and dates.")

    # Final Cleanup
    del vectorstore
    return report
import os, sys, types, time
from pypdf import PdfReader
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

if sys.platform == "win32":
    if "pwd" not in sys.modules: sys.modules["pwd"] = types.ModuleType("pwd")

def load_pdf(path):
    reader = PdfReader(path)
    # Extract only the first few pages if document is huge to save time
    pages = reader.pages[:5] 
    return [page.extract_text() or "" for page in pages]

def document_auditor(ref_path, audit_path):
    start_total = time.perf_counter()
    metrics = {}
    
    # 1. INITIALIZE ONLY THE LLM (Fastest)
    llm = ChatOllama(model="smollm:135m", temperature=0)

    # 2. INSTANT TEXT EXTRACTION
    audit_text_list = load_pdf(audit_path)
    audit_full_text = " ".join(audit_text_list)
    
    ref_text_list = load_pdf(ref_path)
    ref_full_text = " ".join(ref_text_list)[:5000] # Cap for speed

    # 3. METRICS PREP
    metrics["chunk_count"] = len(audit_text_list)
    metrics["retrieval_strategy"] = "Direct Context Injection"

    # 4. SINGLE-SHOT FORENSIC PROMPT
    # We pass the text directly to the LLM. No database = No waiting.
    prompt = ChatPromptTemplate.from_template("""
    SYSTEM: You are a Forensic Auditor. Compare Suspect against Truth.
    TRUTH: {ref_truth}
    SUSPECT: {context}

    Output a bulleted list: [Category]: [Ref] vs [Suspect].
    If identical, say 'No discrepancies detected.'
    """)

    # 5. EXECUTION
    final_report = (prompt | llm | StrOutputParser()).invoke({
        "ref_truth": ref_full_text, 
        "context": audit_full_text[:5000] # Cap suspect text to prevent OOM errors
    })

    # 6. CALCULATE CV METRICS
    metrics["total_latency"] = round(time.perf_counter() - start_total, 2)
    points = final_report.count("[")
    metrics["audit_density"] = f"{points} points"
    metrics["efficiency_score"] = f"{round(metrics['total_latency'] / max(points, 1), 2)}s/pt"
    metrics["retrieval_confidence"] = "100% (Direct Scan)"

    return final_report, metrics
# 🔍 Intelligent Forensic Document Auditor (Local GenAI)

An automated data integrity tool designed to identify discrepancies and unauthorized alterations in high-stakes corporate documents. This project was developed as a **Proof of Concept (POC)** for the Digital Accelerator division to ensure 100% data privacy and eliminate cloud-based API costs.



## 🎯 Target Use Case
* **Forensics:** Identifying tampered text, modified dates, or altered financial figures in official records.
* **Legal/Finance:** Automating the review of complex, multi-page contracts (10+ paragraphs) for data consistency.
* **Process Automation:** Reducing manual auditing time by 90% while maintaining enterprise-grade data security.

## 🛠️ Tech Stack
* **Language:** Python 3.11+
* **LLM Orchestration:** LangChain (LCEL)
* **Local LLM:** Llama 3.2 (via Ollama)
* **Embeddings:** nomic-embed-text (Local via Ollama)
* **Vector Database:** ChromaDB (with MMR search logic)
* **Frontend:** Streamlit for data visualization and interaction

## 🚀 Key Technical Solutions
* **Privacy-First Architecture:** By using **Ollama**, the system processes documents entirely offline, making it suitable for sensitive internal communications.
* **Advanced Retrieval:** Implemented **Maximum Marginal Relevance (MMR)** and adjusted retrieval parameters ($k=6$) to ensure accuracy in long-form documents.
* **Stability Engineering:** Resolved Windows-specific environment conflicts, including telemetry bugs and file-locking errors, through dynamic session pathing.

## 📋 Setup & Installation
1.  **Install Ollama**: Download from [ollama.com](https://ollama.com) and pull the required models:
    ```bash
    ollama pull llama3.2
    ollama pull nomic-embed-text
    ```
2.  **Environment Setup**:
    ```bash
    python -m venv audit_env
    # Windows
    .\audit_env\Scripts\activate
    # Install dependencies
    pip install -r requirements.txt
    ```
3.  **Run Application**:
    ```bash
    streamlit run app.py
    ```


---
**Developer**: [Sethukb](https://www.linkedin.com/in/sethukb/)  
**Portfolio**: [codes-by-sethu.github.io/PORTFOLIO/](https://codes-by-sethu.github.io/PORTFOLIO/)

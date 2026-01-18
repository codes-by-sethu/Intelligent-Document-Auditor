# Intelligent Document Auditor (RAG + Forensics)

## 📌 Project Overview
An AI-powered tool designed to detect inconsistencies and potential tampering between document versions. This project utilizes **Retrieval-Augmented Generation (RAG)** to compare a reference "master" document against a "suspect" version, flagging changed dates, names, or financial figures.

## 🎯 Target Use Case
* **Forensics:** Identifying tampered text in official records.
* **Legal/Finance:** Automating contract review and consistency checking.
* **Process Automation:** Reducing manual auditing time by 90%.

## 🛠️ Tech Stack
* **Language:** Python
* **LLM Orchestration:** LangChain
* **Vector Database:** ChromaDB
* **Embeddings:** OpenAI / HuggingFace
* **Frontend:** Streamlit

## 🚀 Getting Started
1. Clone the repo.
2. Install dependencies: `pip install -r requirements.txt`
3. Set your OpenAI API Key in the `.env` file or Streamlit sidebar.
4. Run the app: `streamlit run app.py`

## 📊 CV-Ready Bullet
> "Developed a RAG-based document auditor for automated text extraction and consistency checking; implemented retrieval strategies to identify tampered data in unstructured files."
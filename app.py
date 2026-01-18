import streamlit as st
import os
from auditor import document_auditor

st.set_page_config(page_title="Forensic Doc Auditor", layout="wide", page_icon="🔍")

st.title("🔍 Intelligent Document Auditor v2.0 (Offline)")
st.caption("Privacy-First AI Audit Engine Powered by Ollama")

col1, col2 = st.columns(2)
with col1:
    ref = st.file_uploader("1. Reference (Master) PDF", type="pdf")
with col2:
    suspect = st.file_uploader("2. Suspect (Audit) PDF", type="pdf")

if st.button("🚀 Run Forensic Audit", use_container_width=True):
    if ref and suspect:
        try:
            with st.spinner("Local AI is analyzing your documents..."):
                with open("ref.pdf", "wb") as f: f.write(ref.getbuffer())
                with open("suspect.pdf", "wb") as f: f.write(suspect.getbuffer())
                
                report = document_auditor("ref.pdf", "suspect.pdf")
                
                st.success("Analysis Complete")
                st.subheader("📋 Final Audit Report")
                st.info(report)
                st.download_button("Export Report", report, "audit_report.txt")
        except Exception as e:
            st.error(f"Audit Error: {e}")
    else:
        st.warning("Please upload both documents.")
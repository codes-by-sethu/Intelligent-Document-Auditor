# eval_document_auditor.py
TEST_DOCS = {
    "doc1": "This contract expires 2025-12-31. Payment due monthly.",
    "doc2": "Invoice #1234 approved for $5,000. Due date: 2025-01-15.",
    "doc3": "Employee contract starts 2025-02-01. Salary: ₹50,000/month.",
    "doc4": "Lease agreement valid until 2026-06-30. Rent paid quarterly.",
    "doc5": "Receipt for laptop purchase $1,200 on 2025-01-10."
}

# Ground truth labels (you define what "positive" means for your auditor)
TRUE_LABELS = [1, 1, 1, 1, 0]  # 1=compliance issue found, 0=no issue

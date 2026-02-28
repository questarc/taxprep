import streamlit as st
from ui.layout import setup_page
from core.models import BalanceSheet, IncomeStatement, CashFlowStatement
from data.storage import load_model
from data.pdf_export import balance_sheet_pdf, income_statement_pdf, cash_flow_pdf

def main():
    setup_page("Export PDF Package", "📄")

    bs = load_model("balance_sheet", BalanceSheet)
    is_stmt = load_model("income_statement", IncomeStatement)
    cf = load_model("cash_flow", CashFlowStatement)

    if not any([bs, is_stmt, cf]):
        st.info("No statements found. Create at least one statement before exporting.")
        return

    if bs:
        pdf_bytes = balance_sheet_pdf(bs)
        st.download_button(
            "Download Balance Sheet PDF",
            data=pdf_bytes,
            file_name="balance_sheet.pdf",
            mime="application/pdf",
        )

    if is_stmt:
        pdf_bytes = income_statement_pdf(is_stmt)
        st.download_button(
            "Download Income Statement PDF",
            data=pdf_bytes,
            file_name="income_statement.pdf",
            mime="application/pdf",
        )

    if cf:
        pdf_bytes = cash_flow_pdf(cf)
        st.download_button(
            "Download Cash Flow Statement PDF",
            data=pdf_bytes,
            file_name="cash_flow_statement.pdf",
            mime="application/pdf",
        )

if __name__ == "__main__":
    main()

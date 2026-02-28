import streamlit as st
from datetime import date
from ui.layout import setup_page
from core.models import IncomeStatement, IncomeStatementLine, BusinessProfile
from data.storage import save_model, load_model
from data.pdf_export import income_statement_pdf
def _ensure_profile() -> BusinessProfile | None:
    profile = st.session_state.get("business_profile")
    if not profile:
        st.error("No business profile found. Please complete the Business Profile page first.")
        st.stop()
    return profile

def main():
    setup_page("Income Statement", "📈")
    profile = _ensure_profile()

    existing: IncomeStatement | None = load_model("income_statement", IncomeStatement)
    col1, col2 = st.columns(2)
    with col1:
        period_start = st.date_input(
            "Period Start",
            value=getattr(existing, "period_start", profile.tax_year_start),
        )
    with col2:
        period_end = st.date_input(
            "Period End",
            value=getattr(existing, "period_end", profile.tax_year_end),
        )

    st.markdown("### Revenue")
    revenue_rows = st.data_editor(
        [{"label": l.label, "amount": l.amount, "category": l.category}
         for l in (existing.lines if existing else []) if l.category == "revenue"] or
        [{"label": "Sales", "amount": 0.0, "category": "revenue"}],
        num_rows="dynamic",
        key="revenue_editor",
    )

    st.markdown("### Expenses")
    expense_rows = st.data_editor(
        [{"label": l.label, "amount": l.amount, "category": l.category}
         for l in (existing.lines if existing else []) if l.category == "expense"] or
        [{"label": "Rent", "amount": 0.0, "category": "expense"}],
        num_rows="dynamic",
        key="expense_editor",
    )

    if st.button("Save Income Statement", type="primary"):
        lines = [
            IncomeStatementLine(**row) for row in revenue_rows + expense_rows
            if row.get("label")
        ]
        is_stmt = IncomeStatement(
            business=profile,
            period_start=period_start,
            period_end=period_end,
            lines=lines,
        )
        save_model("income_statement", is_stmt)
        st.session_state["income_statement"] = is_stmt
        st.success(f"Income statement saved. Net income: {is_stmt.net_income:,.2f}")
    from data.pdf_export import income_statement_pdf

    if existing or "income_statement" in st.session_state:
        is_obj = existing or st.session_state["income_statement"]
        pdf_bytes = income_statement_pdf(is_obj)
        st.download_button(
            "Download Income Statement PDF",
            data=pdf_bytes,
            file_name=f"{is_obj.business.legal_name.lower().replace(' ', '_')}_income_statement.pdf",
            mime="application/pdf",
        )

if __name__ == "__main__":
    main()

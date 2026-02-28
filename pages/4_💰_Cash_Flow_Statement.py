import streamlit as st
from datetime import date
from ui.layout import setup_page
from core.models import CashFlowStatement, CashFlowSection, BusinessProfile
from data.storage import save_model, load_model

def _ensure_profile() -> BusinessProfile | None:
    profile = st.session_state.get("business_profile")
    if not profile:
        st.error("No business profile found. Please complete the Business Profile page first.")
        st.stop()
    return profile

def _editor(label: str, key: str, rows):
    st.markdown(f"### {label}")
    return st.data_editor(
        rows,
        num_rows="dynamic",
        key=key,
    )

def main():
    setup_page("Cash Flow Statement", "💰")
    profile = _ensure_profile()

    existing: CashFlowStatement | None = load_model("cash_flow", CashFlowStatement)
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

    op_rows = _editor(
        "Operating Activities",
        "cf_operating",
        [{"label": s.label, "amount": s.amount} for s in (existing.operating if existing else [])]
        or [{"label": "Net income", "amount": 0.0}],
    )
    inv_rows = _editor(
        "Investing Activities",
        "cf_investing",
        [{"label": s.label, "amount": s.amount} for s in (existing.investing if existing else [])]
        or [{"label": "Purchase of equipment", "amount": 0.0}],
    )
    fin_rows = _editor(
        "Financing Activities",
        "cf_financing",
        [{"label": s.label, "amount": s.amount} for s in (existing.financing if existing else [])]
        or [{"label": "Owner contributions", "amount": 0.0}],
    )

    if st.button("Save Cash Flow Statement", type="primary"):
        cf = CashFlowStatement(
            business=profile,
            period_start=period_start,
            period_end=period_end,
            operating=[CashFlowSection(**r) for r in op_rows if r.get("label")],
            investing=[CashFlowSection(**r) for r in inv_rows if r.get("label")],
            financing=[CashFlowSection(**r) for r in fin_rows if r.get("label")],
        )
        save_model("cash_flow", cf)
        st.session_state["cash_flow"] = cf
        st.success(f"Cash flow saved. Net change in cash: {cf.net_change_in_cash:,.2f}")

if __name__ == "__main__":
    main()

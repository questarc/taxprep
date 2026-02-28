import streamlit as st
from ui.layout import setup_page
from core.models import BusinessProfile, BalanceSheet, IncomeStatement, CashFlowStatement
from core.state_rules import validate_state_compliance
from data.storage import load_model

def _ensure_profile() -> BusinessProfile | None:
    profile = st.session_state.get("business_profile")
    if not profile:
        st.error("No business profile found. Please complete the Business Profile page first.")
        st.stop()
    return profile

def main():
    setup_page("State Requirements & Checks", "⚖️")
    profile = _ensure_profile()

    bs = load_model("balance_sheet", BalanceSheet)
    is_stmt = load_model("income_statement", IncomeStatement)
    cf = load_model("cash_flow", CashFlowStatement)

    messages = validate_state_compliance(profile, bs, is_stmt, cf)

    st.subheader(f"State: {profile.state}")
    if not messages:
        st.info("No specific state requirements configured yet.")
    else:
        for msg in messages:
            st.markdown(f"- {msg}")

if __name__ == "__main__":
    main()

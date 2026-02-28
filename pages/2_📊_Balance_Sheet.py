import streamlit as st
from datetime import date
from ui.layout import setup_page
from core.models import BalanceSheet, BalanceSheetLine, BusinessProfile
from data.storage import save_model, load_model
from data.pdf_export import balance_sheet_pdf

def _ensure_profile() -> BusinessProfile | None:
    profile = st.session_state.get("business_profile")
    if not profile:
        st.error("No business profile found. Please complete the Business Profile page first.")
        st.stop()
    return profile

def main():
    setup_page("Balance Sheet", "📊")
    profile = _ensure_profile()

    existing: BalanceSheet | None = load_model("balance_sheet", BalanceSheet)
    as_of = st.date_input("As of date", value=getattr(existing, "as_of", date.today()))

    st.markdown("### Assets")
    asset_rows = st.data_editor(
        [{"label": l.label, "amount": l.amount, "category": l.category}
         for l in (existing.lines if existing else []) if "asset" in l.category] or
        [{"label": "Cash", "amount": 0.0, "category": "current_asset"}],
        num_rows="dynamic",
        key="assets_editor",
    )

    st.markdown("### Liabilities & Equity")
    liab_rows = st.data_editor(
        [{"label": l.label, "amount": l.amount, "category": l.category}
         for l in (existing.lines if existing else []) if "asset" not in l.category] or
        [
            {"label": "Accounts Payable", "amount": 0.0, "category": "current_liability"},
            {"label": "Owner's Equity", "amount": 0.0, "category": "equity"},
        ],
        num_rows="dynamic",
        key="liab_editor",
    )

    if st.button("Save Balance Sheet", type="primary"):
        lines = [
            BalanceSheetLine(**row) for row in asset_rows + liab_rows
            if row.get("label")
        ]
        bs = BalanceSheet(business=profile, as_of=as_of, lines=lines)
        save_model("balance_sheet", bs)
        st.session_state["balance_sheet"] = bs
        if bs.is_balanced:
            st.success(f"Balance sheet saved. It balances: Assets = {bs.total_assets:,.2f}, "
                       f"Liabilities + Equity = {(bs.total_liabilities + bs.total_equity):,.2f}")
        else:
            st.warning(f"Saved, but not balanced. Assets: {bs.total_assets:,.2f}, "
                       f"Liabilities + Equity: {(bs.total_liabilities + bs.total_equity):,.2f}")
        from data.pdf_export import balance_sheet_pdf

    if existing or "balance_sheet" in st.session_state:
        bs_obj = existing or st.session_state["balance_sheet"]
        pdf_bytes = balance_sheet_pdf(bs_obj)
        st.download_button(
            "Download Balance Sheet PDF",
            data=pdf_bytes,
            file_name=f"{bs_obj.business.legal_name.lower().replace(' ', '_')}_balance_sheet.pdf",
            mime="application/pdf",
        )

if __name__ == "__main__":
    main()

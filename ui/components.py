from __future__ import annotations
import streamlit as st
from datetime import date
from typing import Tuple
from core.models import BusinessProfile

def business_profile_form(initial: BusinessProfile | None = None) -> BusinessProfile:
    col1, col2 = st.columns(2)
    with col1:
        legal_name = st.text_input("Legal Business Name", value=getattr(initial, "legal_name", ""))
        ein = st.text_input("EIN", value=getattr(initial, "ein", ""))
        state = st.text_input("State (2-letter)", value=getattr(initial, "state", "MA"))
        address = st.text_input("Business Address", value=getattr(initial, "address", ""))
    with col2:
        naics_code = st.text_input("NAICS Code", value=getattr(initial, "naics_code", "") or "")
        accounting_method = st.selectbox(
            "Accounting Method", ["Cash", "Accrual"],
            index=0 if getattr(initial, "accounting_method", "Cash") == "Cash" else 1,
        )
        tax_year_start = st.date_input(
            "Tax Year Start",
            value=getattr(initial, "tax_year_start", date(date.today().year, 1, 1)),
        )
        tax_year_end = st.date_input(
            "Tax Year End",
            value=getattr(initial, "tax_year_end", date(date.today().year, 12, 31)),
        )
    return BusinessProfile(
        legal_name=legal_name,
        ein=ein,
        state=state,
        address=address,
        naics_code=naics_code or None,
        accounting_method=accounting_method,
        tax_year_start=tax_year_start,
        tax_year_end=tax_year_end,
    )

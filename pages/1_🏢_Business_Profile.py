import streamlit as st
from ui.layout import setup_page
from ui.components import business_profile_form
from core.models import BusinessProfile
from data.storage import save_model

def main():
    setup_page("Business Profile", "🏢")
    existing: BusinessProfile | None = st.session_state.get("business_profile")

    with st.form("business_profile_form"):
        profile = business_profile_form(existing)
        submitted = st.form_submit_button("Save Business Profile", type="primary")

    if submitted:
        st.session_state["business_profile"] = profile
        save_model("business_profile", profile)
        st.success("Business profile saved.")

if __name__ == "__main__":
    main()

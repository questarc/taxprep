import streamlit as st
from ui.layout import setup_page
from core.models import BusinessProfile
from data.storage import load_model, save_model

def _ensure_session():
    if "business_profile" not in st.session_state:
        profile = load_model("business_profile", BusinessProfile)
        st.session_state["business_profile"] = profile

def main():
    setup_page("Dashboard", "🧾")
    _ensure_session()

    st.subheader("Welcome")
    st.write("Use the sidebar to navigate: set up your business profile, then build each statement.")

    profile = st.session_state.get("business_profile")
    if profile:
        st.success(f"Active business: **{profile.legal_name}** ({profile.state})")
    else:
        st.info("No business profile yet. Go to **Business Profile** page to get started.")

    st.markdown("### Quick Links")
    st.page_link("pages/1_🏢_Business_Profile.py", label="Set Business Profile", icon="🏢")
    st.page_link("pages/2_📊_Balance_Sheet.py", label="Balance Sheet", icon="📊")
    st.page_link("pages/3_📈_Income_Statement.py", label="Income Statement", icon="📈")
    st.page_link("pages/4_💰_Cash_Flow_Statement.py", label="Cash Flow Statement", icon="💰")
    st.page_link("pages/5_⚖️_State_Requirements_and_Checks.py", label="State Requirements", icon="⚖️")
    st.page_link("pages/6_📄_Export_PDF_Package.py", label="Export PDFs", icon="📄")

if __name__ == "__main__":
    main()

import streamlit as st
from config import CONFIG

def setup_page(title: str, icon: str = "📊") -> None:
    st.set_page_config(page_title=f"{CONFIG.app_name} – {title}", page_icon=icon, layout="wide")
    st.title(f"{icon} {title}")
    st.markdown(f"**{CONFIG.app_name}** · LLC financial statement prep for tax filing.")
    st.divider()

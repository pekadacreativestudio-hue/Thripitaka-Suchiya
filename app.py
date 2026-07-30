from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="ත්‍රිපිටක සූචිය",
    page_icon="☸",
    layout="wide",
)

st.markdown(
    """
<style>
.block-container { padding: 0 !important; max-width: 100% !important; }
#MainMenu, footer { visibility: hidden; }
iframe { display: block; }
</style>
""",
    unsafe_allow_html=True,
)

HTML_PATH = Path(__file__).parent / "assets" / "suchiya_reference.html"
html = HTML_PATH.read_text(encoding="utf-8")

components.html(html, height=1400, scrolling=True)

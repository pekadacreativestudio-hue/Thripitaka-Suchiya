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
.block-container { padding: 2.5rem 0 0 0 !important; max-width: 100% !important; }
#MainMenu, footer { visibility: hidden; }
iframe {
    display: block;
    /* The embedded page uses position:fixed for its modal, which centers
       relative to *this iframe's own box*, not the browser window. If the
       iframe is taller than the visible window, the outer Streamlit page
       has to scroll to reveal the rest of it, and the modal ends up
       centered on a part of the iframe that isn't what's currently on
       screen. Locking the iframe to the actual viewport height (with its
       own internal scrollbar for long content) keeps "centered" meaning
       what the user actually sees.

       The 2.5rem block-container padding above adds a visible gap below
       Streamlit Cloud's own viewer toolbar (Share/star/edit/GitHub) so it
       doesn't crowd our header; the extra rem is subtracted here too so
       the total footprint still fits one viewport with no outer scroll. */
    height: calc(100vh - 7.5rem) !important;
}
</style>
""",
    unsafe_allow_html=True,
)

HTML_PATH = Path(__file__).parent / "assets" / "suchiya_reference.html"
html = HTML_PATH.read_text(encoding="utf-8")

components.html(html, height=900, scrolling=True)

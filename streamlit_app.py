# %%

import streamlit as st

st.set_page_config(
        page_title="SetMore Schedules",
        page_icon="📅",
        layout="wide"
    )

st.navigation([st.Page("setmore/pages/uploader.py", title="Home", default=True), st.Page("setmore/pages/beer_festival.py", title="Beer Festival")], position='hidden').run()

"""Script to upload and process SetMore booking CSV files for different events."""
import streamlit as st

from setmore.processor.beer_festival import SetMoreBeerFestivalProcessor

PROCESSOR = {"Beer Festival": SetMoreBeerFestivalProcessor}

PAGES = {"Home": "setmore/pages/uploader.py", "Beer Festival": "setmore/pages/beer_festival.py"}

st.set_page_config(page_title="SetMore Schedules", page_icon="📅", layout="wide")

# Uploader Section
st.title("📅 SetMore Schedules Uploader")
st.markdown("Upload your SetMore booking CSV file to process and download formatted reports.")
st.session_state.event = st.selectbox("Select Event", options=["Beer Festival"])

## Processing Data
st.session_state.uploaded_file = st.file_uploader("Choose a CSV file", type="csv", help="Upload your SetMore booking data CSV file")

if st.session_state.uploaded_file:
    try:
        processor = PROCESSOR.get(st.session_state.event)
        if processor is None:
            st.error(f"No processor found for event: {st.session_state.event}")

        st.session_state.setmore_data = processor(st.session_state.uploaded_file)
        st.success("File processed successfully!")

        st.switch_page(PAGES.get(st.session_state.event))
    except Exception as e:
        st.error(f"Error processing file: {e!s}")

"""Script for the beer festival bookings overview page."""
import streamlit as st

with st.container(horizontal_alignment="right"):
    if st.button("Upload new data", type="secondary"):
        st.switch_page("pages/uploader.py")

st.title("🍺 Beer Festival Bookings Overview")

date_s = st.session_state.setmore_data.data["_timestamp"].min().strftime("%Y-%m-%d")
date_e = st.session_state.setmore_data.data["_timestamp"].max().strftime("%Y-%m-%d")
st.markdown(f"Dates: {date_s} to {date_e}")

st.header("Bars")
st.session_state.bar_data = st.session_state.setmore_data.bars()
st.subheader("Friday")
st.dataframe(
    st.session_state.bar_data[st.session_state.bar_data["_timestamp"].dt.day_name() == "Tuesday"]
    .drop(columns=["_timestamp"])
    .set_index("Timestamp")
)
st.subheader("Saturday")
st.dataframe(
    st.session_state.bar_data[st.session_state.bar_data["_timestamp"].dt.day_name() == "Saturday"]
    .drop(columns=["_timestamp"])
    .set_index("Timestamp")
)

st.header("BBQ")
st.session_state.bbq_data = st.session_state.setmore_data.bbq()
st.subheader("Friday")
st.dataframe(
    st.session_state.bbq_data[st.session_state.bbq_data["_timestamp"].dt.day_name() == "Friday"]
    .drop(columns=["_timestamp"])
    .set_index("Timestamp")
)
st.subheader("Saturday")
st.dataframe(
    st.session_state.bbq_data[st.session_state.bbq_data["_timestamp"].dt.day_name() == "Saturday"]
    .drop(columns=["_timestamp"])
    .set_index("Timestamp")
)

st.header("T-shirts")
st.dataframe(st.session_state.setmore_data.shirt_size_summary(), width="content")

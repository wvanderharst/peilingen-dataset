import streamlit as st


st.title("Voting Power")
uploaded_file = st.file_uploader("Upload an article", type=("txt", "md"))

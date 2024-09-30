import streamlit as st


st.title("First page")
uploaded_file = st.file_uploader("Upload an article", type=("txt", "md"))

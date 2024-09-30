import streamlit as st
import anthropic


st.title("First page")
uploaded_file = st.file_uploader("Upload an article", type=("txt", "md"))

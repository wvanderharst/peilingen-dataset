import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/wvanderharst/peilingen-dataset/refs/heads/main/data/partygov.csv")
    return df


df = load_data()
st.write("Op deze pagina kun je ontdekken welke individuele partij het meest overeenkomt met het beleid van de huidige of potentiële coalitie.")

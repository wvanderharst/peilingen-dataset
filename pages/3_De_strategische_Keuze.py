import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/wvanderharst/peilingen-dataset/refs/heads/main/data/partygov.csv")
    return df


df = load_data()
st.write('Op deze pagina krijg je inzicht in de strategische benadering van stemmen: hoe je niet alleen kiest op basis van de partij die het meest overeenkomt met jouw opvattingen, maar vooral op een manier die de kans vergroot dat het kabinet jouw wensen en idealen weerspiegelt. Of in ieder geval, zoveel mogelijk')

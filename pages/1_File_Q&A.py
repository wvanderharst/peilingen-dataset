import altair as alt
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.title("Meest voorkomende combinates")

@st.cache_data
def load_data():
    df = pd.read_csv("data/coalitions.csv")
    return df


df = load_data()

df['reger'] = df['reger'].str.replace('(', '').str.replace(')', '').str.replace(',', '').str.replace("'", '')

st.dataframe(
    df['reger'].value_counts())
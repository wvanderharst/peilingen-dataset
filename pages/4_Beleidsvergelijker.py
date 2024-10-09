import streamlit as st
import pandas as pd
import ast

@st.cache_data
def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/wvanderharst/peilingen-dataset/refs/heads/main/data/distances.csv")
    return df
@st.cache_data
def load_data2():
    df = pd.read_csv("https://raw.githubusercontent.com/wvanderharst/peilingen-dataset/refs/heads/main/data/partygov.csv")
    return df
df = load_data()
df3 = load_data2()

def contains_all(long_list, short_list):
    return all(item in long_list for item in short_list)

def convert_string_to_list(s):
    return ast.literal_eval(s)


df["Key"] = df["Key"].apply(convert_string_to_list)


# Show a multiselect widget with the genres using `st.multiselect`.
partij = st.multiselect(
    "Partij",
    df3.Partij.unique(),
    ["PVV"],
)
df = df[df['Key'].apply(lambda x: contains_all(x, partij))]
st.write(df)

st.write("Op deze pagina kun je ontdekken welke individuele partij het meest overeenkomt met het beleid van de huidige of potentiële coalitie.")

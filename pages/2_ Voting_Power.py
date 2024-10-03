import altair as alt
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import ast
import itertools



def all_in_list(short_list, long_list):
    return set(short_list).issubset(set(long_list))

def convert_string_to_list(s):
    return ast.literal_eval(s)

def contains_all(long_list, short_list):
    return all(item in long_list for item in short_list)

def load_data2():
    df = pd.read_csv("data/partygov.csv")
    return df

def load_data3():
    df = pd.read_csv("data/elections.csv")
    return df

length = load_data3()

df3 = load_data2()

# Show a multiselect widget with the genres using `st.multiselect`.
partij = st.selectbox(
    "Partij",
    df3.Partij.unique())
df = pd.read_csv(f'data_conditional/{partij}.csv')

allparties = set(df3["Partij"])


df['reger'] = df['reger'].apply(convert_string_to_list)

st.dataframe(
    df['reger'].value_counts())


st.write(len(length))

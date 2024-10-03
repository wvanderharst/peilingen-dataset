import altair as alt
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import ast
import itertools

st.title("Meest voorkomende combinates")

@st.cache_data
def load_data():
    df = pd.read_csv("data/coalitions.csv")
    return df

def load_data2():
    df = pd.read_csv("data/partygov.csv")
    return df

def load_data3():
    df = pd.read_csv("data/partygovmultiple.csv")
    return df



def all_in_list(short_list, long_list):
    return set(short_list).issubset(set(long_list))

def convert_string_to_list(s):
    return ast.literal_eval(s)

def contains_all(long_list, short_list):
    return all(item in long_list for item in short_list)


df = load_data()
df_multiple = load_data3()
#df2['reger'] = df2['reger'].str.replace('(', '').str.replace(')', '').str.replace(',', '').str.replace("'", '')

df4 = pd.read_csv("data/partygov.csv")

allparties = set(df4["Partij"])


df['reger'] = df['reger'].apply(convert_string_to_list)
df_multiple["Key"] = df_multiple["Key"].apply(convert_string_to_list)
st.dataframe(
    df['reger'].value_counts())




df3 = load_data2()

# Show a multiselect widget with the genres using `st.multiselect`.
partij = st.multiselect(
    "Partij",
    df3.Partij.unique(),
    ["PVV"],
)



df_multiple = df_multiple.sort_values(by='Value', ascending=False)

# Reset the index if desired
#df_multiple = df_multiple.reset_index(drop=True, inplace=True)

df_multiple =df_multiple[df_multiple['Key'].apply(lambda x: contains_all(x, partij))]

st.dataframe(
    df_multiple)





df_filtered = df3[(df3["Partij"].isin(partij)) ]
df_filtered2 = df_filtered[["Partij","3"]].reset_index()
#if len(df_filtered2.Partij.unique())>1:
#    df_filtered2.loc['total']= df_filtered2.sum()

# Display the data as a table using `st.dataframe`.
st.dataframe(
    df_filtered2
)

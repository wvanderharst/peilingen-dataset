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


@st.cache_data
def load_data3():
    df = pd.read_csv("https://raw.githubusercontent.com/wvanderharst/peilingen-dataset/refs/heads/main/data/elections.csv")
    return df
@st.cache_data
def load_data4():
    df = pd.read_csv("https://raw.githubusercontent.com/wvanderharst/peilingen-dataset/refs/heads/main/data/piel.csv")
    return df


st.title("Jouw Stem, Jouw Impact")
st.write("Op deze pagina ontdek je de impact van jouw stem op de politieke toekomst van ons land. Elke stem telt, en in een gefragmenteerd partijensysteem zoals het onze, kan jouw keuze de samenstelling van de regering bepalen. Hier krijg je inzicht in hoe verschillende stemgedragingen kunnen leiden tot uiteenlopende coalities en beleidsrichtingen. Het model geeft jouw stem een impact van vijf Zetels")


length = load_data3()
lengthN = len(length.columns)-2

df4 = load_data4()

# Show a multiselect widget with the genres using `st.multiselect`.
partij = st.selectbox(
    "Partij",
    df4.Partij.unique())
partij1 = partij.replace('/', '')

df = pd.read_csv(f'https://raw.githubusercontent.com/wvanderharst/peilingen-dataset/refs/heads/main/data_conditional/{partij1}.csv')
df2 = pd.read_csv(f'https://raw.githubusercontent.com/wvanderharst/peilingen-dataset/refs/heads/main/data_conditional_low/{partij1}.csv')


allparties = set(df4["Partij"])


df['reger'] = df['reger'].apply(convert_string_to_list)
df2['reger'] = df2['reger'].apply(convert_string_to_list)


df34= df[df['reger'].apply(lambda x: partij in x)]
df35= df2[df2['reger'].apply(lambda x: partij in x)]




st.dataframe(
    df['reger'].value_counts()/len(df['reger']))

noemer1 = df['reger'].value_counts().sum()
teller1 = df34['reger'].value_counts().sum()
num = teller1/noemer1

noemer2 = df2['reger'].value_counts().sum()
teller2 = df35['reger'].value_counts().sum()
num2 = teller2/noemer2



#df8 = (df['reger'].value_counts()/len(df['reger'])).sum()
#df34 = (df34['reger'].value_counts()/len(df34['reger'])).sum()
labels = 'Coaltitie', 'Oppositie'
sizes = [num, 1-num ]
explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig1, ax1 = plt.subplots()


ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
    shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title("Zwevende kiezer stemt op " + partij)
st.pyplot(fig1)

labels = 'Coaltitie', 'Oppositie'
sizes = [num2, 1-num2 ]
explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')

fig2, ax2 = plt.subplots()


ax2.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
    shadow=True, startangle=90)
ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title(partij)
st.pyplot(fig2)


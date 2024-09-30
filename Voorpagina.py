import altair as alt
import pandas as pd
import streamlit as st

# Show the page title and description.
st.set_page_config(page_title="Peilingen")

st.title("Peilingen")
st.write(
    """
    In Nederland wordt gekeken naar peilingen van 
    individuele partijen, terwijl we een land van
      coalties leven. Op mijn website maak ik duidelijk wat de coalitie tendesen zijn.
    """
)


# Load the data from a CSV. We're caching this so it doesn't reload every time the app
# reruns (e.g. if the user interacts with the widgets).

@st.cache_data
def load_data():
    df = pd.read_csv("data\partygov.csv")
    return df


df = load_data()

# Show a multiselect widget with the genres using `st.multiselect`.
partij = st.multiselect(
    "Partij",
    df.Partij.unique(),
    ["PVV"],
)


# Filter the dataframe based on the widget input and reshape it.
df_filtered = df[(df["Partij"].isin(partij)) ]
df_filtered2 = df_filtered[["Partij","Percentage","Zetels"]]
if len(df_filtered2.Partij.unique())>1:
    df_filtered2.loc['total']= df_filtered2.sum()

# Display the data as a table using `st.dataframe`.
st.dataframe(
    df_filtered2
)

st.bar_chart(df_filtered2,x="Partij",y="Zetels")


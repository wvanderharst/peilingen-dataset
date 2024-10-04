import altair as alt
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt




# Show the page title and description.
st.set_page_config(page_title="Peilingen")
st.title("Peilingen")
st.write(
    """
    In een gefragmenteerd partijensysteem, zoals we dat in Nederland zien, is het belangrijk om 
    niet alleen te kijken naar de peilingen van individuele partijen, maar vooral naar de waarschijnlijkheden 
    van mogelijke coalities. Dit komt omdat de politieke realiteit vaak wordt gekenmerkt door meerdere partijen 
    die samen moeten werken om een regering te vormen.
    Peilingen geven ons inzicht in de steun voor afzonderlijke partijen, maar ze zeggen weinig over hoe deze partijen 
    zich tot elkaar verhouden en welke combinaties mogelijk zijn. In een systeem met veel partijen kunnen de voorkeuren 
    van kiezers snel verschuiven, waardoor de kansen op samenwerking en het vormen van een meerderheidscoalitie steeds 
    relevanter worden.
    Door de focus te verleggen naar coalitievorming, kunnen we beter begrijpen welke partijen bereid zijn om samen te werken, 
    welke ideologische overeenkomsten er zijn en hoe de politieke dynamiek eruitziet. Dit biedt niet alleen een realistischer 
    beeld van de politieke toekomst, maar kan ook de stabiliteit van de regering ten goede komen.
    In dit licht wordt het duidelijk dat het analyseren van coalitiewaarschijnlijkheden ons helpt om een bredere en meer samenhangende 
    kijk op het politieke landschap te ontwikkelen. Hierdoor kunnen kiezers en analisten niet alleen anticiperen op de uitkomsten van 
    verkiezingen, maar ook op de beleidsvorming en de richting van het bestuur na de verkiezingen.
    """
)


# Load the data from a CSV. We're caching this so it doesn't reload every time the app
# reruns (e.g. if the user interacts with the widgets).

@st.cache_data
def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/wvanderharst/peilingen-dataset/refs/heads/main/data/partygov.csv")
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
df_filtered2 = df_filtered[["Partij","3"]].reset_index()
#if len(df_filtered2.Partij.unique())>1:
#    df_filtered2.loc['total']= df_filtered2.sum()

# Display the data as a table using `st.dataframe`.
st.dataframe(
    df_filtered2
)

st.bar_chart(df_filtered2,x="Partij",y="3")

st.write(df_filtered2["Partij"].tolist())

for i in range(len(df_filtered2["3"])):
    labels = 'Coaltitie', 'Oppositie'
    sizes = [df_filtered2["3"][i], 100 - df_filtered2["3"][i] ]
    explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()


    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title(df_filtered2["Partij"][i])
    st.pyplot(fig1)

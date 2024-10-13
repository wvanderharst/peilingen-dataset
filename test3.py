import pandas as pd
import ast


def load_data():
    df = pd.read_excel("https://peilingwijzer.tomlouwerse.nl/resources/Cijfers_Peilingwijzer.xlsx")
    return df

def seats(parties,df):
    count = 0
    for i in range(0,len(df)):
        if df["Partij"][i] in parties:
            count += df["Zetels"][i]
    return count

df = load_data()

df.to_csv("data\piel2.csv")

def compare_csv(file1, file2):
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    return df1.equals(df2)

file1 = "data\piel.csv"
file2 = "data\piel2.csv"


def convert_string_to_list(s):
    return ast.literal_eval(s)

def load_data3():
    df = pd.read_csv("data/distances.csv")
    return df



if compare_csv(file1, file2):
    distances = load_data3()

else:
    distances = load_data3()
    # Specify the columns you want to keep
    columns_to_keep = ['Partij', 'Zetels']

    # Create a new DataFrame with only the specified columns
    df1 = df[columns_to_keep]

    #for i in range(len(distances["Key1"])):
    #    distances["Seats"] = 
    distances['Key'] = distances['Key'].apply(convert_string_to_list)


    distances["Seats"] = distances['Key'].apply(lambda x: seats(x, df1))
    distances = distances[distances['Seats'] >= 35].reset_index(drop=True)

    distances.to_csv("data/distance_use.csv")
    df.to_csv("data\piel.csv")





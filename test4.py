import pandas as pd
import ast
import numpy as np
import itertools

def load_data():
    df = pd.read_csv("data/Politiek2023.csv")
    return df


df = load_data()

df.to_csv("data\politiek1.csv")

def convert_string_to_list(s):
    return ast.literal_eval(s)

def load_data3():
    df = pd.read_csv("data/distances.csv")
    return df

distances = load_data3()
distances = distances.reset_index(drop=True)
distances.loc[1,"Key"]

# Create a new DataFrame with only the specified columns

#for i in range(len(distances["Key1"])):
#    distances["Seats"] = 
distances['Key'] = distances['Key'].apply(convert_string_to_list)


coordinate_columns = [col for col in df.columns if col != 'Partij']


results = []

distances['Closest'] = ""


for m in range(len(distances['Key'])):
    i = distances.loc[m,"Key"]
    stable = df
    subset = df[df['Partij'].isin(i)]
    average_row = subset.mean(numeric_only=True)
    average_row['partijen'] = i  # Add the combination to the results

    # Ensure average_row is a numpy array for distance calculations
    average_values = average_row[coordinate_columns].values + 0.000001

    # Find the closest row in the original DataFrame
    # Find the closest row in the original DataFrame manually
    distances2 = []

    for index, row in stable.iterrows():
        distance3 = np.sqrt(np.sum((row[coordinate_columns].values - average_values) ** 2))
        distances2.append(distance3)
    
    closest_row_index = np.argmin(distances2)
    closest_row = stable.iloc[closest_row_index]
    
    distances.loc[m,"Closest"]= closest_row['Partij']



distances.to_csv("data/distances.csv")





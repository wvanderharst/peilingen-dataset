import pandas as pd


def load_data():
    df = pd.read_excel("https://peilingwijzer.tomlouwerse.nl/resources/Cijfers_Peilingwijzer.xlsx")
    return df

df = load_data()

df.to_csv("data\piel.csv")

def load_data2():
    df = pd.read_csv("data/elections.csv")
    return df

def load_data3():
    df = pd.read_csv("data/coalitions.csv")
    return df


df2 = load_data2()

df2 = df2.iloc[:, 1:]

# Specify the columns you want to keep
columns_to_keep = ['Partij', 'Zetels']

# Create a new DataFrame with only the specified columns
df1 = df[columns_to_keep]

for index, row in df1.iterrows():
    partij = row['Partij'].replace('/', '')
    zetels = row['Zetels']
    
    # Filter df2 for the current partij
    filtered_df = df2[df2['Partij'] == partij]
    
    # Determine the threshold
    threshold = zetels + 5
    filtered2 = filtered_df.iloc[:, 1:]


    # Keep only the columns where any value is >= threshold (excluding 'Partij' column)
    columns_to_keep = filtered2.columns[(filtered_df.iloc[:, 1:] >= threshold).any(axis=0)]
    
    # Create a filtered DataFrame with only the desired columns
    final_df = filtered_df[['Partij'] + list(columns_to_keep)]  

    final_list = final_df.columns[1:].tolist()
    final_list = list(map(int, final_list))
    df3 = load_data3()
    filtered_df3 = df3[df3.index.isin(final_list)]

    # Save to CSV, naming the file according to the partij
    filtered_df3.to_csv(f'data_conditional/{partij}.csv', index=False)

    #print(f'Saved {partij}.csv with filtered data.')



import pandas as pd
import numpy as np
import itertools
import time
## funcations 



#functions


def load_data():
    df = pd.read_excel("https://peilingwijzer.tomlouwerse.nl/resources/Cijfers_Peilingwijzer.xlsx")
    return df

def tablecreator(table,df):
    cols = list(df.columns.values) 
    for k in range(1,len(cols),2):
        cols1 = cols[k]
        cols2 = cols[k+1]
        for i in range(0,len(df)):
            party1 = df["Partij"][i]
            for j in range(0,len(df)):
                party2 = df["Partij"][j]
                table[party1][party2] +=  ((df[cols1][i] -
                                           df[cols1][j])**2 +
                                          (df[cols2][i] - 
                                           df[cols2][j])**2)**0.5
    return table


def distance(parties,table):
    #discribes the amount of distance in a coalition normalized for amount of lines but with (1+(len(parties)**1,5/25))) correction
    totaldistance = 0
    for i in range(0,len(parties)):
        for j in range(0,len(parties)):
            party1 = parties[i]
            party2 = parties[j] 
            totaldistance += table[party1][party2]**2
    return totaldistance / ((len(parties)**2 +len(parties))/2) * (1+(len(parties)**2.4/25))

def seats(parties,df):
    count = 0
    for i in range(0,len(df)):
        if df["Partij"][i] in parties:
            count += df["Zetels"][i]
    return count

def findalldistances(allparties,table):
    pairs_dict = {}
    #for L in range(len(allparties) + 1):
    for L in range(1,12):
        for subset in itertools.combinations(allparties, L):
            mogregering = list(subset)
            dist = distance(mogregering,table)
            pairs_dict[subset] = dist
    
    # Sort by values
    df_distance = pd.DataFrame(list(pairs_dict.items()), columns=['Key', 'Value'])

    # Sort the DataFrame by 'Key'
    df_distance = df_distance.sort_values(by='Value')




    return df_distance

def linear_mapping(x):
    if x < 20:
        return 0  # Optional: handle inputs less than 20
    elif x > 45:
        return 1  # Optional: handle inputs greater than 45
    else:
        return (x / 25) - 0.8

def probabilistic_output(probability):
    if not (0 <= probability <= 1):
        raise ValueError("Probability must be between 0 and 1.")
    
    return 1 if random.random() < probability else 0

def possiblecombinations(df_distance,table,df):
    regering = ""
    secondregering = ""
    thirdregering = ""
    count = 0
    for i in range(len(df_distance)):
        mogregering = df_distance.loc[i,"Key"] 
        mogregering = superpartyhate(mogregering)
        mapped = linear_mapping(seats(["PVV"],df))
        probabilistic_output(mapped)
        if probabilistic_output(mapped) == 1:
            mogregering = partyhate(mogregering)
        if seats(mogregering,df) > 75:
            count = count + 1 
            dist = df_distance.loc[i,"Value"] 
            if count == 1 : 
                regering = mogregering
                totaldistance = dist
            elif count == 2: 
                secondregering = mogregering
                seconddistance = dist
            elif count == 3:
                thirdregering = mogregering
                thirddistance = dist

                return [regering, secondregering, thirdregering,totaldistance,seconddistance,thirddistance]   
    return [regering, secondregering, thirdregering,totaldistance,seconddistance,thirddistance]

def partyhate(parties):
    if "PVV" in parties:
        if "VVD" in parties:           
            parties = []
        elif "NSC" in parties:           
            parties = []
    return parties 

def superpartyhate(parties):
    if "PVV" in parties:
        if "CDA" in parties:           
            parties = []
        elif "D66" in parties:           
            parties = []
        elif "GL/PvdA" in parties:           
            parties = []
        elif "Denk" in parties:           
            parties = []
    if "FVD" in parties:
        if "CDA" in parties:           
            parties = []
        elif "D66" in parties:           
            parties = []
        elif "GL/PvdA" in parties:           
            parties = []
        elif "Denk" in parties:           
            parties = []
                
    if "BBB" in parties:
        if "PvdD" in parties:           
            parties = []
    return parties 



def montecarloelection(df):
    df9 = df[["Partij" , "Zetels"]]
    for i in range(0,len((df9))):
        #name = df["Partij"][i]
        #CAT = categorizevariance(name,dataframe)
        CAT = 2
        df9.loc[i, 'Zetels'] = df9.loc[i, 'Zetels'] + np.random.normal(0,( 0.15 * CAT  * df9.loc[i, 'Zetels'])) 
        if np.random.normal(0,1) > 2:
            df9.loc[i, 'Zetels'] = df9.loc[i, 'Zetels'] + 5
        if df9.loc[i, 'Zetels'] < 0:
            df9.loc[i, 'Zetels'] = 0
        elif df9.loc[i, 'Zetels'] > 50:
            df9.loc[i, 'Zetels'] = 50
    data = 150 * df9["Zetels"]/sum(df9["Zetels"])
    for i in range(0,len((df9["Zetels"]))):
        df9.loc[i, 'Zetels'] = round(data[i])
    
    while sum(df9["Zetels"]) < 150:
        i= np.random.randint(0, len(df9["Zetels"]))
        df9.loc[i, 'Zetels'] += 1
    while sum(df9["Zetels"]) > 150:
        i= np.random.randint(0, len(df9["Zetels"]))
        if df9.loc[i, 'Zetels']>1:
            df9.loc[i, 'Zetels'] += -1  
    return df9


#load data
df = pd.read_excel(".data\Politiek.xlsx")

#with new distance formula or new matrix
checking = 7


if checking == 8:
    print("Ja1")
    df2 = load_data()
    df3 = df.merge(df2, how='outer', on='Partij')

    df3 = df3.fillna(0)
    allparties = set(df3["Partij"])

    df4 = df3.iloc[:, :-8]

    table = pd.DataFrame()
    table = pd.DataFrame(0.0,columns= df4["Partij"],index=df4["Partij"])

    table2 = tablecreator(table,df4)
    findalldistances(allparties,table)
    df_distance = findalldistances(allparties,table)
    df_distance.to_csv("data\distances.csv")

df_distance = pd.read_csv(".data\distances.csv")

df2 = load_data()
df3 = df.merge(df2, how='outer', on='Partij')

df3 = df3.fillna(0)

df4 = df3.iloc[:, :-8]

table = pd.DataFrame()
table = pd.DataFrame(0.0,columns= df4["Partij"],index=df4["Partij"])

table2 = tablecreator(table,df4)

#check

#mainscript

N =  100
P= 5
allparties = set(df3["Partij"])

df11 = pd.DataFrame()
man = pd.DataFrame(np.zeros((N,6)),columns=["reger","reger2","reger3","dis1","dis2","dis3"] )

for i in range(0,N):
    start_time = time.time()

    df7 = montecarloelection(df3)
    note = possiblecombinations(df_distance,table2,df7)
    man.loc[i,"reger"]= note[0]
    man.loc[i,"reger2"]= note[1]
    man.loc[i,"reger3"]= note[2]
    man.loc[i,"dis1"]= note[3]
    man.loc[i,"dis2"]= note[4]
    man.loc[i,"dis3"]= note[5]
    df7 = df7.rename(columns={"Zetels": i})
    if i == 0:
        df11 = pd.DataFrame(df7)
    else:
        df11 = df11.merge(pd.DataFrame(df7), on='Partij')
    


man.to_csv("data\coalitions.csv")
df11.to_csv("data\elections.csv")



ratio1 = man['reger'].value_counts()/N
ratio2 = man['reger2'].value_counts()/N
ratio3 = man['reger3'].value_counts()/N



ratio1 =  ratio1.rename_axis('bar').reset_index()
ratio2 =  ratio2.rename_axis('bar').reset_index()
ratio3 =  ratio3.rename_axis('bar').reset_index()



full = pd.merge(ratio1,ratio2,on = "bar", how = "outer")
full = pd.merge(full,ratio3,on = "bar", how = "outer")

full = full.fillna(0)


partygov = pd.DataFrame(np.zeros((4,len(allparties))),columns=list(allparties)
                         )

for j in allparties:
    for i in range(0,len(full)):
        string = full["bar"][i]
        my_list = [item.strip().strip("'") for item in string[1:-1].split(',')]
        if j in my_list:
            
            partygov[j][0] += full["count_x"][i]
            partygov[j][1] +=  full["count_y"][i]
            partygov[j][2] +=  full["count"][i]

    partygov[j][3] = (0.60 * partygov[j][0] + 0.30 * partygov[j][1] + 0.1 * partygov[j][2]) * 100

partygov = partygov.T
partygov = partygov.reset_index()
partygov.rename(columns={'index': 'Partij'}, inplace=True)

partygov.to_csv("data\partygov.csv")

def (allparties,table):
    #for L in range(len(allparties) + 1):
    for L in range(1,4):
        for subset in itertools.combinations(allparties, L):
            

def findalldistances(allparties,table):
    pairs_dict = {}
    #for L in range(len(allparties) + 1):
    for L in range(1,12):
        for subset in itertools.combinations(allparties, L):
            mogregering = list(subset)
            pairs_dict[subset] = dist
    
    # Sort by values
    df_distance = pd.DataFrame(list(pairs_dict.items()), columns=['Key', 'Value'])

    # Sort the DataFrame by 'Key'
    df_distance = df_distance.sort_values(by='Value')
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
    totaldistance = 0
    for i in range(0,len(parties)):
        for j in range(0,len(parties)):
            party1 = parties[i]
            party2 = parties[j] 
            totaldistance += table[party1][party2]**2
    return totaldistance / ((len(parties)**2 +len(parties))/2) * (1+(len(parties)/50))

def seats(parties,df):
    count = 0
    for i in range(0,len(df)):
        if df["Partij"][i] in parties:
            count += df["Zetels"][i]
    return count

def findalldistances(allparties,table):
    pairs_dict = {}
    #for L in range(len(allparties) + 1):
    for L in range(1,5):
        for subset in itertools.combinations(allparties, L):
            mogregering = list(subset)
            dist = distance(mogregering,table)
            pairs_dict[subset] = dist
    
    # Sort by values
    df_distance = pd.DataFrame(list(pairs_dict.items()), columns=['Key', 'Value'])

    # Sort the DataFrame by 'Key'
    df_distance = df_distance.sort_values(by='Value')




    return df_distance


def possiblecombinations(allparties,table,df,P):
    totaldistance = 10000000
    seconddistance = 10000000
    thirddistance = 10000000
    regering = ""
    secondregering = ""
    thirdregering = ""
    populism = np.random.normal(0,1) 
    checking = False
    for L in range(len(allparties) + 1):
        for subset in itertools.combinations(allparties, L):
            mogregering = list(subset)

            mogregering = superpartyhate(mogregering)
            if  populism > 0:
                mogregering = partyhate(mogregering)
            if len(mogregering) > P:
                if checking:
                    return [regering, secondregering, thirdregering,totaldistance,seconddistance,thirddistance]
                P = P + 1 
            if seats(mogregering,df) > 75:
                dist = distance(mogregering,table)
                if dist < totaldistance: 
                    thirdregering = secondregering
                    secondregering = regering
                    regering = mogregering
                    
                    thirddistance = seconddistance
                    seconddistance = totaldistance
                    totaldistance = dist

                elif dist < seconddistance:
                    
                    thirdregering = secondregering
                    secondregering = mogregering

                    thirddistance = seconddistance
                    seconddistance = dist
                elif dist <thirddistance:
                    thirdregering = mogregering
                    thirddistance = dist
                    checking = True
                       
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
df = pd.read_excel("data\Politiek.xlsx")
df_check = pd.read_excel("Data\politiek - Stable.xlsx")

if df.equals(df_check):
    trip  = 8
else:
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

breakpoint



df2 = load_data()
df3 = df.merge(df2, how='outer', on='Partij')

df3 = df3.fillna(0)

df4 = df3.iloc[:, :-8]

table = pd.DataFrame()
table = pd.DataFrame(0.0,columns= df4["Partij"],index=df4["Partij"])

table2 = tablecreator(table,df4)



#check




#mainscript





N =  3
P= 5
allparties = set(df3["Partij"])

df11 = pd.DataFrame()
man = pd.DataFrame(np.zeros((N,6)),columns=["reger","reger2","reger3","dis1","dis2","dis3"] )

for i in range(0,N):
    df7 = montecarloelection(df3)
    note = possiblecombinations(allparties,table2,df7,P)
    man.loc[i,"reger"]= ", ".join(note[0])
    man.loc[i,"reger2"]= ", ".join(note[1])
    man.loc[i,"reger3"]= ", ".join(note[2])
    man.loc[i,"dis1"]= note[3]
    man.loc[i,"dis2"]= note[4]
    man.loc[i,"dis3"]= note[5]
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

ratio1.to_csv("test2.csv")


full = pd.merge(ratio1,ratio2,on = "bar", how = "outer")
full = pd.merge(full,ratio3,on = "bar", how = "outer")

full.to_csv("test1.csv")


full["prefer"] = 200.0




for i in range(0,len(full)):
    string = full.loc[i,"bar"]
    li = list(string.split(", "))
    full.loc[i,"prefer"] = distance(li,table)
full = full.fillna(0)

partygov = pd.DataFrame(np.zeros((4,len(allparties))),columns=list(allparties)
                         )
full.to_csv("test2.csv")

for j in allparties:
    for i in range(0,len(full)):
        string = full["bar"][i]
        li = list(string.split(", "))
        if j in li:
            partygov[j][0] += 100 * full["count_x"][i]
            partygov[j][1] += 100 * full["count_y"][i]
            partygov[j][2] += 100 * full["count"][i]

    partygov[j] = partygov[j]/100
    partygov[j][3] = (0.60 * partygov[j][0] + 0.30 * partygov[j][1] + 0.1 * partygov[j][2])

partygov.to_csv("data\partygov.csv")

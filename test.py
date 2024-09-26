import pandas as pd
from xlwings import view
import numpy as np
import itertools
import time


df = pd.read_excel("politiek.xlsx")


def load_data():
    df = pd.read_excel("https://peilingwijzer.tomlouwerse.nl/resources/Cijfers_Peilingwijzer.xlsx")
    return df


df2 = load_data()
df3 = df.merge(df2, how='outer', on='Partij')

df3 = df3.fillna(0)

df4 = df3.iloc[:, :-8]

table = pd.DataFrame()
table = pd.DataFrame(0.0,columns= df4["Partij"],index=df4["Partij"])

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

table2 = tablecreator(table,df4)

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

def possiblecombinations(allparties,table,df,P):
    totaldistance = 10000000
    seconddistance = 10000000
    thirddistance = 10000000
    regering = ""
    secondregering = ""
    thirdregering = ""
    stuff = allparties
    populism = np.random.normal(0,1) 
    checking = False
    for L in range(len(stuff) + 1):
        for subset in itertools.combinations(stuff, L):
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

N =  1000
P= 5
allparties = set(df3["Partij"])

df11 = []
man = pd.DataFrame(np.zeros((N,6)),columns=["reger","reger2","reger3","dis1","dis2","dis3"] )
for i in range(0,N):
    df7 = montecarloelection(df3)
    note = possiblecombinations(allparties,table,df7,P)
    man.loc[i,"reger"]= ", ".join(note[0])
    man.loc[i,"reger2"]= ", ".join(note[1])
    man.loc[i,"reger3"]= ", ".join(note[2])
    man.loc[i,"dis1"]= note[3]
    man.loc[i,"dis2"]= note[4]
    man.loc[i,"dis3"]= note[5]
    df11 = [df11, df7]

man.to_csv("your_preferred_name.csv")

   
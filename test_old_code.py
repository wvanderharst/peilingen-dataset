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
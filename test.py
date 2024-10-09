import pandas as pd
import numpy as np
import itertools
import time
import random
import subprocess
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

def count_instances(long_list, short_list):
    return all(item in long_list for item in short_list)


def findallworkingstogether(allparties,df,number,N):
    pairs_dict = {}
    #for L in range(len(allparties) + 1):
    for L in range(1,number):
        for subset in itertools.combinations(allparties, L):
            df['all_present'] = df['reger'].apply(lambda x: count_instances(x, subset))

            # Count how many times all instances in the short list are present
            total_count = df['all_present'].sum()


            pairs_dict[subset] = total_count/N
    return pairs_dict




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
        elif "Volt" in parties:           
            parties = []                          
    if "BBB" in parties:
        if "PvdD" in parties:           
            parties = []
    return parties 

def copula_simulation(df3,n_samples):
    parties = df3['Partij'].tolist()

    correlation_matrix =  pd.read_csv("data\Correlation_matrix.csv", index_col=0)
    correlation_matrix = pd.DataFrame(correlation_matrix, index=parties, columns=parties)
    correlation_matrix.fillna(0, inplace=True)

    #TEST EMPTY MATRIX
    #for i in range(len(parties)):
    #      for j in range(len(parties)):
    #        correlation_matrix.iat[i, j] = 0

    for i in range(len(parties)):
        correlation_matrix.iat[i, i] = 1

    # Step 2: Calculate standard deviations based on the current Zetels
    std_devs = np.maximum((df3['Zetels'] * 0.3).to_numpy(),1) # Scaling factor

    # Step 3: Set means to the current seat estimates
    mean = df3['Zetels'].values  # Use current seat estimates as means

    # Number of samples to generate

    # Step 4: Generate samples from a multivariate normal distribution
    covariance = np.diag(std_devs) @ correlation_matrix.to_numpy() @ np.diag(std_devs)
    #print(covariance)

    samples = np.random.multivariate_normal(mean, covariance, size=n_samples)
    #Adjustment to correct for non gaussian
    adjustments = np.where(np.random.rand(n_samples, samples.shape[1]) > 0.975, 5, 0)
    samples += adjustments    
    # Step 5: Prepare a DataFrame to store all simulations
    simulation_results = pd.DataFrame(samples, columns=df3['Partij'])

    # Step 6: Allocate Zetels for each simulation
    predicted_Zetels_list = []

    for sim in range(n_samples):    
        # Get the current simulation's votes
        current_votes = samples[sim]

        # Proportional allocation of Zetels (150 total Zetels)
        total_votes = np.sum(current_votes)
        seat_allocation = (current_votes / total_votes) * 150  # Total of 150 Zetels

        seat_allocation = np.maximum(seat_allocation, 0)

        # Round to get integer seat allocation
        seat_allocation = np.round(seat_allocation).astype(int)



        # Correct the seat allocations
        total_allocated = np.sum(seat_allocation)

        # Adjust if total allocated is not equal to 150
        while total_allocated != 150:
            if total_allocated < 150:
                # Increment the Partij with the highest average vote
                idx = np.argmax(current_votes)  # Find Partij with the highest vote
                seat_allocation[idx] += 1  # Increment seat
            elif total_allocated > 150:
             # Decrement the Partij with the lowest allocated Zetels
                idx = np.argmax(seat_allocation)  # Find Partij with the least Zetels
                seat_allocation[idx] -= 1  # Decrement seat

            total_allocated = np.sum(seat_allocation)  # Recalculate total allocated Zetels

    # Store the corrected seat allocation
        predicted_Zetels_list.append(seat_allocation)

    # Convert the list to a DataFrame
    predicted_Zetels_df = pd.DataFrame(predicted_Zetels_list, columns=df3['Partij'])


    predicted_Zetels_df.T.to_csv("data/elections.csv")
    return predicted_Zetels_df.T.reset_index()



#load data
df = pd.read_excel("data\Politiek.xlsx")

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
    subprocess.run(['python', 'test4.py'])

subprocess.run(['python', 'test3.py'])

df_distance = pd.read_csv("data\distance_use.csv")


df2 = load_data()
df3 = df.merge(df2, how='outer', on='Partij')

df3 = df3.fillna(0)

df4 = df3.iloc[:, :-8]

table = pd.DataFrame()
table = pd.DataFrame(0.0,columns= df4["Partij"],index=df4["Partij"])

table2 = tablecreator(table,df4)

#check

#mainscript

N = 10
P= 5
allparties = set(df3["Partij"])

df11 = pd.DataFrame()
man = pd.DataFrame(np.zeros((N,6)),columns=["reger","reger2","reger3","dis1","dis2","dis3"] )


df7 = copula_simulation(df3,N)

for col in df7.columns[1:]:
    df77 = df7[['Partij', col]].rename(columns={col: 'Zetels'})

    note = possiblecombinations(df_distance,table2,df77)
    man.loc[col,"reger"]= note[0]
    man.loc[col,"reger2"]= note[1]
    man.loc[col,"reger3"]= note[2]
    man.loc[col,"dis1"]= note[3]
    man.loc[col,"dis2"]= note[4]
    man.loc[col,"dis3"]= note[5]
    


man.to_csv("data\coalitions.csv")




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


number = 5
dictor = findallworkingstogether(allparties,man,number,N)

df_multiple = pd.DataFrame(list(dictor.items()), columns=['Key', 'Value'])

df_multiple.to_csv("data\partygovmultiple.csv")

subprocess.run(['python', 'test2.py'])

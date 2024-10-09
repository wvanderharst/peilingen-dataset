import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt

# Sample DataFrame with Partij names and current seat estimates
def load_data():
    df = pd.read_excel("https://peilingwijzer.tomlouwerse.nl/resources/Cijfers_Peilingwijzer.xlsx")
    return df

df = pd.read_excel("data\Politiek.xlsx")
df2 = load_data()
df3 = df.merge(df2, how='outer', on='Partij')

df3 = df3.fillna(0)


df3 = df3[["Partij" , "Zetels"]]

# Step 1: Define the correlation matrix
# (Replace this with your actual correlation matrix)

def Copula_simulation(df3,n_samples):
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
    n_samples = 100

    # Step 4: Generate samples from a multivariate normal distribution
    covariance = np.diag(std_devs) @ correlation_matrix.to_numpy() @ np.diag(std_devs)
    #print(covariance)

    samples = np.random.multivariate_normal(mean, covariance, size=n_samples)

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
    return predicted_Zetels_df


# Step 3: Calculate implied correlation matrix
# simulated_covariance = np.cov(samples, rowvar=False)
#implied_correlation = np.zeros_like(simulated_covariance)
# for i in range(simulated_covariance.shape[0]):
#    for j in range(simulated_covariance.shape[1]):
#        if simulated_covariance[i, i] > 0 and simulated_covariance[j, j] > 0:
#            implied_correlation[i, j] = simulated_covariance[i, j] / np.sqrt(simulated_covariance[i, i] * simulated_covariance[j, j])
#        else:
#            implied_correlation[i, j] = 0  # Handle cases where variance is zero

# Convert to DataFrame for better readability




# Step 7: Visualization (optional)
# Take the mean seat allocation over all simulations for a summary
#mean_Zetels = predicted_Zetels_df.mean().round().astype(int)

#plt.figure(figsize=(12, 6))
#plt.bar(mean_Zetels.index, mean_Zetels.values, color='blue', alpha=0.7)
#plt.title('Mean Predicted Seat Allocation Over Simulations')
#plt.xlabel('Parties')
#plt.ylabel('Number of Zetels')
#plt.xticks(rotation=45)
#plt.show()

## Optional: Print results
#print(predicted_Zetels_df)  # All individual simulations
#print("Mean Zetels Allocation:\n", mean_Zetels)
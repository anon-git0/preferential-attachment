import random
import time
import matplotlib.pyplot as plt
import numpy as np

start_time = time.time() 

maxN = 10000
recording_precision = 1000 # A result is recorded after each multiple of this many time steps.

"""
DEFINE THE MODEL.
E.g. in rock-paper-scissors model, the types are given by
0 = rock, 1 = paper, 2 = scissors.
The type1_wins list gives parent type pairs such that the first beats the second.
In this case that is [0,0],[1,1],[2,2],[0,2],[1,0],[2,1].
(In the case of a tie, it does not matter which is considered the winner.)

G_degrees stores the total degrees of each type.
e.g. if the initial graph is a triangle with one vertex of each type, it is [2,2,2].
"""
type1_wins = [[0,0],[1,1],[2,2],[0,2],[1,0],[2,1]]
G_degrees = [2,2,2]

results = [] # Initialise a list for storing the proportions of each type over time.
for i in range(len(G_degrees)):
    results.append([G_degrees[i]/sum(G_degrees)]) # Add an entry to the results with the initial proportions of each type.

"""
CHOOSING A PARENT
Each time the new vertex chooses a parent, it chooses by preferential attachment.
Hence, the probability it will attach to a vertex of a certain type is the proportion
(total degree of all vertices of that type)/(total degree of the entire graph).
"""

def pick_parent(degrees):
    R = random.randint(0,sum(G_degrees)-1) # random integer between 0 and the total degree of the graph minus one.
    # We will count through G_degrees from left to right (binning) and wherever this random number falls,
    # that type will be the parent type.
    
    k = 0 # The type of the parent vertex. We start with 0 and count up until we reach the right type.
    total = 0
    done = 0

    while done == 0:
        if R < G_degrees[k] + total:
            done = 1
        else:
            total = total + G_degrees[k]
            k = k+1
    """
    EXAMPLE:
    G_degrees = [10,6,12]. R will be a random integer between 0 and 27 inclusive.
    If R is anything from 0 to 9, type 0 will be chosen (probability 10/28).
    If R is anything from 10 to 15, type 1 will be chosen (probability 6/28).
    Otherwise, R is 16 or greater, type 2 will be chosen (probability 12/28).
    The probability that each type is chosen is that type's total degree (G_degrees[i]) divided by sum(G_degrees).
    """

    return k

for q in range(maxN):
    parent_1 = pick_parent(G_degrees) # Choose two parent types by preferential attachment.
    parent_2 = pick_parent(G_degrees)

    # Increase degrees of parent vertices.
    G_degrees[parent_1] = G_degrees[parent_1] + 1 # The two parent vertices gain a child, so their degrees increase by 1.
    G_degrees[parent_2] = G_degrees[parent_2] + 1

    # Add new vertex.
    parent_types = [parent_1, parent_2]
    if parent_types in type1_wins: # If this pair of types is in type1_wins, it means the first vertex wins.
        G_degrees[parent_1] = G_degrees[parent_1] + 2
    else:
        G_degrees[parent_2] = G_degrees[parent_2] + 2 # Whichever is the winning type, the new vertex takes that type, and has a degree of 2, so 2 is added to the total degree for that type.

    # Update results.
    if q % recording_precision == 0: # Only record if the time step is a multiple of recording_precision (there is no need to record at every step, this would be wasteful).
        total = sum(G_degrees)
        for i in range(len(results)):
            results[i].append(G_degrees[i] / total) # Add an entry to the results with the initial proportions of each type.

end_time = time.time()

time_taken = end_time - start_time # Print the time taken, to inform how much time a longer simulation might take.
print("The time taken (in seconds) is ",time_taken)

"""
GRAPHING
"""
# Labels for the types.
labels = ['rock', 'paper', 'scissors']

time_steps = [recording_precision * (i + 1) for i in range(len(results[0]))]
# Set the x values for the x axis. (0*recording_precision, 1*recording_precision, 2*recording_precision, ...)

# Plot each list in the results against the x values.
for i, result in enumerate(results):
    plt.plot(time_steps, result, label=labels[i])

# We set the x axis to a log scale, because oscillations are evenly spaced on a log-graph (based on mathematical work).
plt.xscale('log')

# Add labels and title
plt.xlabel('Time steps')
plt.ylabel('Proportion of type')
plt.title('Results for rock-paper-scissors m=2 preferential attachment') # Can be set to a suitable title for the model.

powers_of_ten = [10**i for i in range(3, int(np.log10(max(time_steps))) + 1)]
plt.xticks(powers_of_ten, [f'{int(tick):,}' for tick in powers_of_ten])
# Set ticks to be powers of 10 (e.g., 1000, 10000, 100000). The x axis looks neater this way.

plt.savefig("rps_attachment_results.pdf") # Optional. Save the results.
plt.legend()
plt.show()


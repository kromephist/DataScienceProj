from match_ids_request import get_match_ids
from rounds_efficacy import calculate_efficacy
from clustering import perform_clustering
from neural_networks import train_neural_network
from plotting import *

# Get the match ids for a specific tournament code
tournament_code = "VC2022"
match_ids = get_match_ids(tournament_code)

# Calculate the efficacy data for each match
efficacy_data = calculate_efficacy(match_ids)

# Perform clustering on the efficacy data
num_clusters = 3
cluster_labels = perform_clustering(efficacy_data, num_clusters)

# Train a neural network on the efficacy data
model, history = train_neural_network(efficacy_data, cluster_labels)

# Display the GUI window with buttons to show the clustering and neural network results
display_plotting_gui(cluster_labels, history)
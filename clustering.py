import json
import pandas as pd
from sklearn.cluster import KMeans

def cluster_matches(match_ids, input_file):
    # Load the data
    with open(input_file) as f:
        data = json.load(f)
    
    # Create a dataframe from the data
    df = pd.DataFrame(data)
    
    # Filter the dataframe to only include the matches in match_ids
    df = df[df['match_id'].isin(match_ids)]
    
    # Create a new dataframe with the efficacy values
    efficacy_df = pd.DataFrame(columns=['save_eff', 'eco_eff', 'buy_eff'])
    for match_id in match_ids:
        save_eff = df[df['match_id'] == match_id]['save_eff'].mean()
        eco_eff = df[df['match_id'] == match_id]['eco_eff'].mean()
        buy_eff = df[df['match_id'] == match_id]['buy_eff'].mean()
        efficacy_df = efficacy_df.append({'save_eff': save_eff, 'eco_eff': eco_eff, 'buy_eff': buy_eff}, ignore_index=True)
    
    # Perform clustering
    kmeans = KMeans(n_clusters=3, random_state=0).fit(efficacy_df)
    cluster_labels = kmeans.labels_
    efficacy_df['cluster'] = cluster_labels
    
    # Return the cluster labels
    return list(efficacy_df['cluster'])

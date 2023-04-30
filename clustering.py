import json
import pandas as pd
from sklearn.cluster import KMeans

def cluster_matches(efficacy_data, num_clusters):
    # Create a dataframe from the efficacy data
    df = pd.DataFrame(efficacy_data, columns=['save_eff', 'eco_eff', 'buy_eff'])
    
    # Perform clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(df)
    cluster_labels = kmeans.labels_
    
    # Return the cluster labels
    return list(cluster_labels)


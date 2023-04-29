import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

def neural_networks(match_id, round_type):
    # load the efficacy data for the match
    file_name = f"{match_id}_{round_type}.json"
    try:
        df = pd.read_json(file_name)
    except:
        print(f"No data for {match_id} {round_type} round")
        return

    # select the relevant features for training the model
    features = ['team_round', 'team_money', 'team_half', 'enemy_round', 'enemy_money', 'enemy_half']
    X = df[features]
    y = df['round_type']

    # split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # train a neural network model
    model = MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=1000, random_state=42)
    model.fit(X_train, y_train)

    # evaluate the model on the test set
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Accuracy score for {match_id} {round_type} round: {acc:.2f}")

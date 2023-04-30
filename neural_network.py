import tensorflow as tf
from tensorflow import keras
from keras import layers
import numpy as np

def train_neural_network(efficacy_data, cluster_labels):
    """
    Given a list of efficacy data and their corresponding cluster labels,
    trains a neural network to predict the cluster labels based on the efficacy data.
    Returns the trained model and training history.
    """
    # Convert the efficacy data and cluster labels to numpy arrays
    efficacy_data = np.array(efficacy_data)
    cluster_labels = np.array(cluster_labels)

    # Create the neural network architecture
    model = keras.Sequential(
        [
            layers.Dense(16, activation="relu", input_shape=(3,)),
            layers.Dense(8, activation="relu"),
            layers.Dense(3),
        ]
    )

    # Compile the model
    model.compile(loss='mse', optimizer='adam')

    # Train the model
    history = model.fit(efficacy_data, cluster_labels, epochs=100, batch_size=10)

    return model, history.history

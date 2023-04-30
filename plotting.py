import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk

def plot_cluster_histogram(cluster_labels):
    """
    Given a list of cluster labels, displays a histogram of the clusters
    """
    # Count the number of matches in each cluster
    counts = [0, 0, 0]
    for label in cluster_labels:
        counts[label] += 1

    # Plot the histogram
    fig, ax = plt.subplots()
    ax.bar([0, 1, 2], counts, align='center', alpha=0.5)
    ax.set_xticks([0, 1, 2])
    ax.set_xticklabels(['Cluster 1', 'Cluster 2', 'Cluster 3'])
    ax.set_ylabel('Number of Matches')
    ax.set_title('Cluster Histogram')
    plt.show()

def plot_training_history(history):
    """
    Given a keras history object, displays a plot of the training and validation loss over time
    """
    fig, ax = plt.subplots()
    ax.plot(history.history['loss'], label='Training Loss')
    ax.plot(history.history['val_loss'], label='Validation Loss')
    ax.set_xlabel('Epoch')
    ax.set_ylabel('Loss')
    ax.set_title('Training History')
    ax.legend()
    plt.show()

def display_plotting_gui(cluster_labels, history):
    """
    Given a list of cluster labels and a keras history object, displays a GUI with buttons to show the
    cluster histogram and training history
    """
    # Create the tkinter GUI window
    root = tk.Tk()
    root.title("Valorant Analytics")

    # Create the figure objects for the plots
    cluster_fig = plt.figure(figsize=(4, 4))
    plot_cluster_histogram(cluster_labels)
    cluster_canvas = FigureCanvasTkAgg(cluster_fig, master=root)
    cluster_canvas.get_tk_widget().grid(row=0, column=0)

    training_fig = plt.figure(figsize=(4, 4))
    plot_training_history(history)
    training_canvas = FigureCanvasTkAgg(training_fig, master=root)
    training_canvas.get_tk_widget().grid(row=0, column=1)

    # Create the "Close" button
    close_button = tk.Button(root, text="Close", command=root.quit)
    close_button.grid(row=1, column=0, columnspan=2)

    # Run the tkinter event loop
    tk.mainloop()

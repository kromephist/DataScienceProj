import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns

# Load the Anime.csv and Rating.csv files
anime_df = pd.read_csv("anime.csv")
rating_df = pd.read_csv("rating.csv")

# Merge the two dataframes on the anime_id column
merged_df = pd.merge(anime_df, rating_df, on="anime_id", suffixes=("", "_user"))

# Drop rows with missing values in the rating_user column
cleaned_df = merged_df.dropna(subset=["rating_user"])

# Convert genre column into a list of strings
cleaned_df["genre"] = cleaned_df["genre"].str.split(",")

# Flatten the list of genres into individual rows
cleaned_df = cleaned_df.explode("genre")

# Group the data by genre and calculate the mean rating and total members
genre_df = cleaned_df.groupby("genre").agg({"rating_user": "mean", "members": "sum"}).reset_index()

# Perform KMeans clustering on the genre_df data
kmeans = KMeans(n_clusters=3, n_init=10)
genre_df["cluster"] = kmeans.fit_predict(genre_df[["rating_user", "members"]])

# Perform linear regression on the genre_df data
X = genre_df[["rating_user"]]
y = genre_df["members"]
reg = LinearRegression().fit(X, y)
genre_df["predicted_members"] = reg.predict(X)

# Visualize the data with a scatter plot
fig, ax = plt.subplots(figsize=(10, 8))
scatter = ax.scatter(genre_df["rating_user"], genre_df["members"], c=genre_df["cluster"])
ax.set_xlabel("Mean Rating")
ax.set_ylabel("Total Members")
ax.set_title("Anime Genres by Mean Rating and Total Members")
ax.grid(True)

# Add a legend for the scatter plot
legend1 = ax.legend(*scatter.legend_elements(),
                    loc="upper right", title="Clusters")
ax.add_artist(legend1)

# Save the scatter plot
fig.savefig("genre_scatter.png")

# Generate a wordcloud of the genres based on mean rating
wordcloud = WordCloud(background_color="white").generate_from_frequencies(genre_df.set_index("genre")["rating_user"])
plt.figure(figsize=(10, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Wordcloud of Anime Genres by Mean Rating")
plt.savefig("genre_wordcloud_rating.png")

# Generate a wordcloud of the genres based on total members
wordcloud = WordCloud(background_color="white").generate_from_frequencies(genre_df.set_index("genre")["members"])
plt.figure(figsize=(10, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.title("Wordcloud of Anime Genres by Total Members")
plt.savefig("genre_wordcloud_members.png")

# create a dictionary of anime names and their corresponding number of members
anime_dict = dict(zip(cleaned_df['name'], cleaned_df['members']))

# create a word cloud from the anime dictionary
wordcloud = WordCloud(width=800, height=800, background_color='white', max_words=50).generate_from_frequencies(anime_dict)

# plot the word cloud
plt.figure(figsize=(8, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.savefig('anime_wordcloud.png')

# Get top 5 genres by number of anime
# Create a dictionary to store mean ratings for each genre
genre_rating_dict = {}

# Iterate over each row in the cleaned dataframe
for index, row in cleaned_df.iterrows():
    # Split the genres for the anime
    genres = row["genre"]
    # Iterate over each genre and update the rating in the dictionary
    for genre in genres:
        if genre not in genre_rating_dict:
            genre_rating_dict[genre] = {"sum": row["rating_user"], "count": 1}
        else:
            genre_rating_dict[genre]["sum"] += row["rating_user"]
            genre_rating_dict[genre]["count"] += 1

# Create a new dictionary to store merged genres and their ratings
merged_genre_rating_dict = {}

# Iterate over the original dictionary and merge genres with similar ratings
for genre, rating_info in genre_rating_dict.items():
    mean_rating = rating_info["sum"] / rating_info["count"]
    if mean_rating not in merged_genre_rating_dict:
        merged_genre_rating_dict[mean_rating] = [genre]
    else:
        merged_genre_rating_dict[mean_rating].append(genre)

# Create a new dictionary to store the mean ratings for the merged genres
merged_genre_mean_rating_dict = {}

# Iterate over the merged genre dictionary and calculate the mean rating for each merged genre
for mean_rating, genres in merged_genre_rating_dict.items():
    merged_genre_mean_rating_dict[" / ".join(genres)] = mean_rating

# Create a sorted list of the merged genres by mean rating
sorted_merged_genres = sorted(merged_genre_mean_rating_dict, key=merged_genre_mean_rating_dict.get, reverse=True)

# Create a bar graph of the mean ratings for the merged genres
fig, ax = plt.subplots(figsize=(12, 8))
ax.bar(sorted_merged_genres, [merged_genre_mean_rating_dict[genre] for genre in sorted_merged_genres])
ax.set_xlabel("Genre")
ax.set_ylabel("Mean Rating")
ax.set_title("Anime Genres by Mean Rating")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

# Import libraries
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load the ratings data
ratings = pd.read_csv("ratings.csv")

# Pivot the ratings data to get a user-item matrix
user_item = ratings.pivot(index="userId", columns="movieId", values="rating")

# Fill the missing values with zeros
user_item = user_item.fillna(0)

# Calculate the cosine similarity between users
user_sim = cosine_similarity(user_item)

# Create a dataframe of user similarities
user_sim_df = pd.DataFrame(user_sim, index=user_item.index, columns=user_item.index)

# Define a function to get the top n similar users for a given user
def get_similar_users(user_id, n):
  # Sort the user similarities in descending order
  sorted_user_sim = user_sim_df[user_id].sort_values(ascending=False)
  # Exclude the user itself
  sorted_user_sim = sorted_user_sim[sorted_user_sim.index != user_id]
  # Return the top n similar users
  return sorted_user_sim.head(n)

# Define a function to get the recommendations for a given user
def get_recommendations(user_id, n):
  # Get the top n similar users for the user
  similar_users = get_similar_users(user_id, n)
  # Get the items rated by the similar users
  similar_users_items = user_item[user_item.index.isin(similar_users.index)]
  # Get the mean ratings of the items by the similar users
  mean_ratings = similar_users_items.mean()
  # Get the items not rated by the user
  unrated_items = user_item.loc[user_id][user_item.loc[user_id] == 0].index
  # Filter the mean ratings by the unrated items
  mean_ratings = mean_ratings[mean_ratings.index.isin(unrated_items)]
  # Sort the mean ratings in descending order
  sorted_mean_ratings = mean_ratings.sort_values(ascending=False)
  # Return the top n recommendations
  return sorted_mean_ratings.head(n)

# Test the functions
print(get_similar_users(1, 5))
print(get_recommendations(1, 5))